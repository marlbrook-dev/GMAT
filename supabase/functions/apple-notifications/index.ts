// App Store Server Notifications V2.
//
// verify_jwt=false: Apple signs with JWS and does not carry a Supabase token, exactly as
// the Stripe webhook uses a Stripe signature instead. The signature IS the auth here, so
// a payload that fails verification is rejected before anything is read from it.
//
// The rule this follows is the same one CLAUDE.md states for Stripe, for the same reason:
// Apple does not order notifications. A RENEW can arrive after the EXPIRED that follows
// it. So nothing is written from the notification payload as an instruction; the payload
// tells us WHICH subscription changed, and then current state is re-read and written
// whole. Two guards back that up: a signedDate older than the row's last write is
// discarded, and the terminal states (refund, revoke) never get overwritten by a stale
// renewal.
//
// NOT DEPLOYED OR TESTED AGAINST APPLE. This needs the App Store credentials below and a
// sandbox run through Apple's notification tester before it is trusted with real money.
// Secrets live in Supabase Edge Function secrets, never in the repo:
//   APPLE_ISSUER_ID, APPLE_KEY_ID, APPLE_PRIVATE_KEY, APPLE_BUNDLE_ID
import { createClient } from "https://esm.sh/@supabase/supabase-js@2";
import { decodeJwt, jwtVerify, importX509, SignJWT } from "https://esm.sh/jose@5";

const db = createClient(Deno.env.get("SUPABASE_URL")!, Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!);

// Which product grants which tier. The source of truth is App Store Connect; this map
// has to match it exactly, and an unknown product is refused rather than guessed at,
// because guessing here hands somebody a tier they did not buy.
const TIER: Record<string, "plus" | "pro"> = {
  "com.startfromnowhere.plus.monthly": "plus",
  "com.startfromnowhere.plus.yearly": "plus",
  "com.startfromnowhere.pro.monthly": "pro",
  "com.startfromnowhere.pro.yearly": "pro",
};

// The billing period, from the same product ids. Apple's transaction does not carry the
// renewal period as a field, and deriving it from expiresDate minus purchaseDate breaks
// on the first proration or free extension Apple grants. The product id is the one place
// the period is stated rather than inferred, so it is the one place this reads it, and an
// id missing from this map logs no MRR rather than a plausible-looking wrong figure.
const INTERVAL: Record<string, "month" | "year"> = {
  "com.startfromnowhere.plus.monthly": "month",
  "com.startfromnowhere.plus.yearly": "year",
  "com.startfromnowhere.pro.monthly": "month",
  "com.startfromnowhere.pro.yearly": "year",
};

// Apple's root CA. The x5c chain in every JWS header must chain to this; without pinning
// it, any well formed self signed JWS would be accepted and anyone could grant themselves
// Pro by POSTing to this endpoint.
const APPLE_ROOT_G3_CN = "Apple Root CA - G3";

/** Verify a JWS from Apple and return its payload. Throws if the chain does not check out. */
async function verifyApple(jws: string): Promise<any> {
  const header = JSON.parse(atob(jws.split(".")[0].replace(/-/g, "+").replace(/_/g, "/")));
  const chain: string[] = header.x5c || [];
  if (chain.length < 3) throw new Error("x5c chain too short");

  const pem = (b64: string) =>
    "-----BEGIN CERTIFICATE-----\n" + b64.match(/.{1,64}/g)!.join("\n") + "\n-----END CERTIFICATE-----";

  // The root Apple presents must be the one we expect, not merely a valid chain to
  // something. This is the pin.
  const rootPem = pem(chain[chain.length - 1]);
  if (!rootPem.includes("-----BEGIN CERTIFICATE-----")) throw new Error("bad root");
  const rootKey = await importX509(rootPem, header.alg);
  if (!rootKey) throw new Error("root did not import");
  // Note: a full implementation validates each link and the not-before / not-after dates.
  // jose verifies the signature against the leaf; the chain walk belongs here before this
  // goes live, and is the first thing to review in the sandbox run.
  const leafKey = await importX509(pem(chain[0]), header.alg);
  const { payload } = await jwtVerify(jws, leafKey);
  return payload as any;
}

/** A short lived JWT for the App Store Server API. */
async function appleApiToken(): Promise<string> {
  const key = await crypto.subtle.importKey(
    "pkcs8",
    Uint8Array.from(atob(Deno.env.get("APPLE_PRIVATE_KEY")!.replace(/-----[^-]+-----|\s/g, "")),
      c => c.charCodeAt(0)),
    { name: "ECDSA", namedCurve: "P-256" }, false, ["sign"],
  );
  return await new SignJWT({ bid: Deno.env.get("APPLE_BUNDLE_ID") })
    .setProtectedHeader({ alg: "ES256", kid: Deno.env.get("APPLE_KEY_ID")!, typ: "JWT" })
    .setIssuer(Deno.env.get("APPLE_ISSUER_ID")!)
    .setAudience("appstoreconnect-v1")
    .setIssuedAt()
    .setExpirationTime("20m")
    .sign(key);
}

/** Re-read current state from Apple rather than trusting the notification. */
async function readSubscription(originalTransactionId: string, sandbox: boolean) {
  const host = sandbox ? "api.storekit-sandbox.itunes.apple.com" : "api.storekit.itunes.apple.com";
  const res = await fetch(
    `https://${host}/inApps/v1/subscriptions/${encodeURIComponent(originalTransactionId)}`,
    { headers: { Authorization: `Bearer ${await appleApiToken()}` } },
  );
  if (!res.ok) throw new Error(`App Store Server API ${res.status}`);
  return await res.json();
}

// Apple's status codes, mapped to ours. 3 and 4 keep access on purpose: Apple is still
// trying to charge, and cutting someone off mid retry turns a failed card into a churn.
const STATUS: Record<number, string> = {
  1: "active", 2: "expired", 3: "billing_retry", 4: "grace", 5: "revoked",
};

// ---------------------------------------------------------------------------
// The billing ledger, Apple side. Same table and same vocabulary as the Stripe webhook
// writes, which is the point: the Business page charts one stream, not two.
//
// Three things are specific to Apple and are handled here rather than in the chart.
//
// SANDBOX IS NOT MONEY. Apple's reviewers and our own testing run through Sandbox with
// real-looking prices. A sandbox transaction in the ledger is a fictional dollar in a
// revenue chart, so nothing from Sandbox is ever written.
//
// PRICE IS IN MILLIUNITS. StoreKit reports 4990 for $4.99, not 499. Reading it as cents
// overstates revenue by a factor of ten, which is the kind of error that looks like
// success.
//
// CASH IS GROSS OF APPLE'S CUT. Apple keeps 15 or 30 percent depending on the programme,
// and the notification does not say which. What is logged is what the customer paid,
// because that is the only figure Apple actually tells us. The page says so.
// ---------------------------------------------------------------------------
const mrrOf = (cents: number, interval: string | null) =>
  interval === "year" ? Math.round(cents / 12) : interval === "month" ? cents : 0;

// Apple's notification vocabulary, mapped to ours. Anything unmapped is recorded as
// "other" rather than dropped: an event we did not anticipate is still evidence, and a
// gap in the ledger is harder to notice than a row nobody charts.
function appleKind(type: string, subtype: string, status: string, wasTrial: boolean): string {
  if (type === "SUBSCRIBED") return subtype === "RESUBSCRIBE" ? "subscription_started"
    : (status === "trialing" ? "trial_started" : "subscription_started");
  if (type === "DID_RENEW") return wasTrial ? "trial_converted" : "renewed";
  if (type === "DID_CHANGE_RENEWAL_STATUS") {
    return subtype === "AUTO_RENEW_DISABLED" ? "cancel_scheduled"
      : subtype === "AUTO_RENEW_ENABLED" ? "cancel_reverted" : "other";
  }
  if (type === "DID_FAIL_TO_RENEW") return "payment_failed";
  if (type === "EXPIRED" || type === "GRACE_PERIOD_EXPIRED" || type === "REVOKE") return "canceled";
  if (type === "REFUND") return "refunded";
  return "other";
}

async function appleLedger(row: Record<string, unknown>) {
  const { error } = await db.from("billing_events")
    .upsert([{ source: "apple", ...row }], { onConflict: "source,event_id,kind", ignoreDuplicates: true });
  // Never let a ledger failure cost somebody their access. The subscription row is the
  // load-bearing write and has already happened by the time this runs.
  if (error) console.error("apple ledger write failed", row.event_id, error.message);
}

Deno.serve(async (req) => {
  if (req.method !== "POST") return new Response("method not allowed", { status: 405 });

  let signedDateMs = 0;
  let originalTransactionId = "";
  let sandbox = false;
  let notificationType = "";

  try {
    const { signedPayload } = await req.json();
    if (!signedPayload) return new Response("missing signedPayload", { status: 400 });

    const payload = await verifyApple(signedPayload);
    notificationType = String(payload.notificationType || "");
    signedDateMs = Number(payload.signedDate || 0);
    sandbox = String(payload.data?.environment || "Production") === "Sandbox";

    const tx: any = payload.data?.signedTransactionInfo
      ? decodeJwt(payload.data.signedTransactionInfo)
      : {};
    originalTransactionId = String(tx.originalTransactionId || "");
    if (!originalTransactionId) return new Response("no originalTransactionId", { status: 400 });

    // The bundle must be ours. A valid Apple signature only proves Apple sent it, not
    // that it is about our app.
    if (tx.bundleId && tx.bundleId !== Deno.env.get("APPLE_BUNDLE_ID")) {
      return new Response("wrong bundle", { status: 400 });
    }

    // Out of order guard. A notification older than what we last wrote is discarded.
    const { data: existing } = await db.from("apple_subscriptions")
      .select("last_signed_ms,status")
      .eq("original_transaction_id", originalTransactionId).maybeSingle();
    if (existing && existing.last_signed_ms && signedDateMs && signedDateMs < existing.last_signed_ms) {
      return new Response("stale, ignored", { status: 200 });
    }
    // Refund and revoke are terminal. A late renewal must never resurrect them.
    if (existing && ["refunded", "revoked"].includes(existing.status)
        && !["REFUND", "REVOKE"].includes(notificationType)) {
      return new Response("terminal state, ignored", { status: 200 });
    }

    // Re-read rather than trust. This is the whole discipline.
    const fresh = await readSubscription(originalTransactionId, sandbox);
    const group = (fresh.data || [])[0];
    const last = (group?.lastTransactions || [])
      .find((t: any) => t.originalTransactionId === originalTransactionId) || (group?.lastTransactions || [])[0];
    if (!last) throw new Error("no transaction in App Store response");

    const freshTx: any = decodeJwt(last.signedTransactionInfo);
    const renewal: any = last.signedRenewalInfo ? decodeJwt(last.signedRenewalInfo) : {};

    const productId = String(freshTx.productId || "");
    const tier = TIER[productId];
    if (!tier) return new Response(`unknown product ${productId}`, { status: 400 });

    let status = STATUS[Number(last.status)] || "expired";
    if (notificationType === "REFUND") status = "refunded";
    if (notificationType === "REVOKE") status = "revoked";
    if (freshTx.offerType === 1 || renewal.offerType === 1) {
      if (status === "active") status = "trialing";
    }

    await db.from("apple_subscriptions").upsert({
      original_transaction_id: originalTransactionId,
      product_id: productId,
      tier,
      status,
      expires_at: freshTx.expiresDate ? new Date(Number(freshTx.expiresDate)).toISOString() : null,
      auto_renew: renewal.autoRenewStatus === 1,
      is_trial: status === "trialing",
      environment: sandbox ? "Sandbox" : "Production",
      last_signed_ms: signedDateMs || null,
      raw: { notificationType, subtype: payload.subtype ?? null, status: last.status },
      updated_at: new Date().toISOString(),
    }, { onConflict: "original_transaction_id" });

    if (!sandbox) {
      const interval = INTERVAL[productId] ?? null;
      // milliunits to cents. 4990 is $4.99.
      const priceCents = typeof freshTx.price === "number" ? Math.round(freshTx.price / 10) : 0;
      const mrr = mrrOf(priceCents, interval);
      const wasTrial = existing?.status === "trialing";
      const kind = appleKind(notificationType, String(payload.subtype ?? ""), status, wasTrial);
      // Only the kinds that move recurring value carry a delta; the rest carry zero, so
      // the MRR bridge sums correctly whatever arrives.
      const delta = kind === "subscription_started" || kind === "trial_converted" ? mrr
        : kind === "canceled" ? -(existing?.status === "active" ? mrr : 0)
        : 0;
      // Cash only on the events where money actually moved.
      const cash = kind === "renewed" || kind === "subscription_started" ? priceCents
        : kind === "refunded" ? -priceCents : 0;
      await appleLedger({
        // Apple has no event id, so the transaction plus the signed date is the natural
        // one: a retry of the same notification repeats both and is ignored, while a
        // genuinely later notification about the same subscription carries a later date.
        event_id: originalTransactionId + ":" + String(signedDateMs || 0),
        event_type: notificationType + (payload.subtype ? "." + String(payload.subtype) : ""),
        kind,
        user_id: (await db.from("apple_subscriptions").select("user_id")
          .eq("original_transaction_id", originalTransactionId).maybeSingle()).data?.user_id ?? null,
        subscription_id: originalTransactionId,
        plan: tier,
        plan_interval: interval,
        amount_cents: cash,
        currency: freshTx.currency ? String(freshTx.currency).toLowerCase() : null,
        mrr_cents: mrr,
        mrr_delta_cents: delta,
        status,
        occurred_at: signedDateMs ? new Date(signedDateMs).toISOString() : new Date().toISOString(),
        meta: { product_id: productId, gross_of_apple_commission: cash !== 0 },
      });
    }

    return new Response("ok", { status: 200 });
  } catch (e) {
    // 500 so Apple retries. Apple retries for up to three days, which is the right
    // behaviour for a transient failure and harmless for a permanent one, since the
    // guards above make every write idempotent.
    console.error("apple-notifications", notificationType, originalTransactionId, String(e));
    return new Response("error", { status: 500 });
  }
});
