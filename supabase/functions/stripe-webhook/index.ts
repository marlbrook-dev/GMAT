// Stripe webhook: keeps profiles in sync with subscription state.
// Deployed with verify_jwt=false; authentication is Stripe's signature check instead
// (STRIPE_WEBHOOK_SECRET). Point a Stripe webhook endpoint at this function for events:
// checkout.session.completed, customer.subscription.created, customer.subscription.updated,
// customer.subscription.deleted, invoice.paid, invoice.payment_failed, charge.refunded.
// The first four keep profiles in sync; all seven feed the billing_events ledger that
// admin_business() reads. An event type this file does not name falls through to a 200,
// so enabling more of them in Stripe is safe and enabling fewer only loses history.
import Stripe from "npm:stripe@17";
import { createClient } from "jsr:@supabase/supabase-js@2";

const stripe = new Stripe(Deno.env.get("STRIPE_SECRET_KEY") ?? "", { apiVersion: "2024-06-20" });
const secret = Deno.env.get("STRIPE_WEBHOOK_SECRET") ?? "";
const admin = createClient(Deno.env.get("SUPABASE_URL")!, Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!);

const iso = (unix: number | null | undefined) =>
  typeof unix === "number" ? new Date(unix * 1000).toISOString() : null;

// Every column below is service-role only: 20260916_harden_plan_column_and_rpc_surface.sql
// leaves them out of the column grants, so no browser session can forge a plan.
async function writeProfile(userId: string, patch: Record<string, unknown>) {
  const { error } = await admin.from("profiles").update(patch).eq("id", userId);
  if (error) console.error("profile update failed", userId, error.message);
}

// ---------------------------------------------------------------------------
// The billing ledger.
//
// profiles holds what an account pays RIGHT NOW and is overwritten on every event, so the
// moment somebody cancels the evidence they ever paid is gone. That is fine for gating
// access and useless for running a business: it cannot answer how much new revenue
// arrived, how much left, what share of trials convert, or what came back out as refunds.
// Every handler below therefore appends the facts it just learned to billing_events, which
// is append-only and never overwritten. See 20260921_billing_events_ledger.sql.
//
// Writing the ledger must never be able to break the thing that keeps a paying customer's
// access working. So a ledger failure is logged and swallowed: the profile write above is
// the load-bearing one, and it has already happened by the time we get here.
// ---------------------------------------------------------------------------

type LedgerRow = {
  event_id: string;
  event_type: string;
  kind: string;
  user_id?: string | null;
  subscription_id?: string | null;
  plan?: string | null;
  plan_interval?: string | null;
  amount_cents?: number;
  currency?: string | null;
  mrr_cents?: number;
  mrr_delta_cents?: number;
  status?: string | null;
  occurred_at: string;
  meta?: Record<string, unknown>;
};

// The same rule as public.mrr_of in the migration. Two copies of one definition is a
// drift risk, so it is written here exactly as it is written there, and the smoke test
// checks a monthly, an annual and a null against both.
function mrrOf(cents: number | null | undefined, interval: string | null | undefined): number {
  if (typeof cents !== "number") return 0;
  if (interval === "year") return Math.round(cents / 12);
  if (interval === "week") return Math.round(cents * 52 / 12);
  if (interval === "day") return Math.round(cents * 365 / 12);
  return cents;
}

async function ledger(rows: LedgerRow[]) {
  if (!rows.length) return;
  const payload = rows.map((r) => ({
    source: "stripe",
    amount_cents: 0,
    mrr_cents: 0,
    mrr_delta_cents: 0,
    meta: {},
    ...r,
  }));
  // Stripe retries, and a retry is the same fact arriving twice rather than two facts.
  // ignoreDuplicates leans on unique (source, event_id, kind) and on the partial unique
  // index that allows a subscription exactly one start, one conversion and one end however
  // many event types announce it.
  const { error } = await admin
    .from("billing_events")
    .upsert(payload, { onConflict: "source,event_id,kind", ignoreDuplicates: true });
  if (error) console.error("ledger write failed", rows[0]?.event_id, error.message);
}

// What we believed about this account before the event landed. Needed for exactly one
// reason: an MRR movement is a difference, and a difference needs both sides. Without the
// prior row an upgrade looks identical to a new subscription.
async function priorState(userId: string | null) {
  if (!userId) return null;
  const { data } = await admin
    .from("profiles")
    .select("plan, plan_status, plan_interval, plan_amount_cents, cancel_at_period_end")
    .eq("id", userId)
    .maybeSingle();
  return data ?? null;
}

async function userIdForCustomer(customer: string | null): Promise<string | null> {
  if (!customer) return null;
  const { data } = await admin.from("profiles").select("id").eq("stripe_customer_id", customer).maybeSingle();
  return data?.id ?? null;
}

const idOf = (v: unknown): string | null =>
  typeof v === "string" ? v : (v && typeof v === "object" && "id" in (v as Record<string, unknown>)
    ? String((v as { id: unknown }).id) : null);

const atOf = (event: Stripe.Event) => new Date(event.created * 1000).toISOString();

// The subscription carries our user_id in metadata, but metadata can be absent on a
// subscription that was not created by our checkout (a Stripe dashboard edit, a recovered
// subscription). Falling back to the customer id keeps those in sync instead of silently
// dropping them, which is why checkout stores stripe_customer_id in the first place.
async function userIdFor(sub: Stripe.Subscription): Promise<string | null> {
  const fromMeta = sub.metadata?.user_id;
  if (fromMeta) return fromMeta;
  const customer = typeof sub.customer === "string" ? sub.customer : sub.customer?.id;
  if (!customer) return null;
  const { data } = await admin.from("profiles").select("id").eq("stripe_customer_id", customer).maybeSingle();
  return data?.id ?? null;
}

// Stripe does not guarantee the order webhook events arrive in. A subscription.deleted
// landing after a subscription.updated would resurrect a cancelled plan; the reverse would
// downgrade a paying customer. Writing the event payload is therefore never safe. Re-read
// the subscription and write what Stripe says it is right now, which is correct whatever
// order the events turned up in and costs one API call on an event we already handle.
//
// If the re-read fails, fall back to the payload rather than dropping the event: stale
// state beats no state, and the handler throwing would make Stripe retry anyway.
async function currentSub(sub: Stripe.Subscription): Promise<Stripe.Subscription> {
  try {
    return await stripe.subscriptions.retrieve(sub.id);
  } catch (e) {
    console.error("subscription re-read failed, using event payload", sub.id, String(e));
    return sub;
  }
}

// Pinned to API version 2024-06-20, where current_period_end sits on the subscription.
// Stripe moved it onto subscription items in 2025 versions; if you bump apiVersion above,
// this is the line that needs to change.
function subPatch(sub: Stripe.Subscription) {
  const active = sub.status === "active" || sub.status === "trialing";
  // What this subscriber actually pays. Without the interval, revenue can only be a
  // headcount times a hardcoded rate, which stops being true the first time a price moves.
  const price = sub.items?.data?.[0]?.price;
  return {
    plan: active ? (sub.metadata?.plan ?? "plus") : "free",
    plan_status: sub.status,
    stripe_subscription_id: sub.id,
    stripe_customer_id: typeof sub.customer === "string" ? sub.customer : sub.customer?.id ?? null,
    trial_end: iso(sub.trial_end),
    current_period_end: iso(sub.current_period_end),
    cancel_at_period_end: !!sub.cancel_at_period_end,
    plan_interval: price?.recurring?.interval ?? null,
    plan_amount_cents: typeof price?.unit_amount === "number" ? price.unit_amount : null,
  };
}

Deno.serve(async (req: Request) => {
  const sig = req.headers.get("stripe-signature");
  const body = await req.text();
  let event: Stripe.Event;
  try {
    event = await stripe.webhooks.constructEventAsync(body, sig!, secret);
  } catch {
    return new Response("Bad signature", { status: 400 });
  }
  try {
    if (event.type === "checkout.session.completed") {
      const s = event.data.object as Stripe.Checkout.Session;
      const uid = s.client_reference_id ?? s.metadata?.user_id;
      // A session that starts a free trial settles as "no_payment_required", not "paid".
      // Checking only for "paid" would leave every trialing subscriber on the free plan.
      const settled = s.payment_status === "paid" || s.payment_status === "no_payment_required";
      if (uid && s.status === "complete" && settled) {
        const subId = typeof s.subscription === "string" ? s.subscription : s.subscription?.id;
        // Read the subscription back rather than trusting the session: it is the only
        // place trial_end, the renewal date and the price live, and the Account page and
        // the revenue view need all three.
        const sub = subId ? await stripe.subscriptions.retrieve(subId) : null;
        await writeProfile(uid, sub ? subPatch(sub) : {
          plan: s.metadata?.plan ?? "plus",
          plan_status: "active",
          stripe_customer_id: typeof s.customer === "string" ? s.customer : s.customer?.id ?? null,
        });
        // Checkout and customer.subscription.created BOTH announce a new subscription,
        // with different event ids. Logging from both is how new MRR gets counted twice,
        // so both write the same kind against the same subscription id and the partial
        // unique index keeps whichever arrives first. Neither is reliably first, which is
        // exactly why the database decides rather than the code.
        if (sub) {
          const patch = subPatch(sub);
          const trialing = sub.status === "trialing";
          const mrr = mrrOf(patch.plan_amount_cents, patch.plan_interval);
          await ledger([{
            event_id: event.id, event_type: event.type,
            kind: trialing ? "trial_started" : "subscription_started",
            user_id: uid, subscription_id: sub.id,
            plan: sub.metadata?.plan ?? null, plan_interval: patch.plan_interval,
            currency: sub.items?.data?.[0]?.price?.currency ?? null,
            mrr_cents: mrr,
            // A trial is worth nothing until it converts. Counting it as revenue on the
            // day it starts is how a dashboard starts lying to its owner.
            mrr_delta_cents: trialing ? 0 : mrr,
            status: sub.status, occurred_at: atOf(event),
            meta: { via: "checkout" },
          }]);
        }
      }
    } else if (event.type === "customer.subscription.created") {
      const sub = await currentSub(event.data.object as Stripe.Subscription);
      const uid = await userIdFor(sub);
      if (uid) {
        await writeProfile(uid, subPatch(sub));
        const patch = subPatch(sub);
        const trialing = sub.status === "trialing";
        const mrr = mrrOf(patch.plan_amount_cents, patch.plan_interval);
        await ledger([{
          event_id: event.id, event_type: event.type,
          kind: trialing ? "trial_started" : "subscription_started",
          user_id: uid, subscription_id: sub.id,
          plan: sub.metadata?.plan ?? null, plan_interval: patch.plan_interval,
          currency: sub.items?.data?.[0]?.price?.currency ?? null,
          mrr_cents: mrr, mrr_delta_cents: trialing ? 0 : mrr,
          status: sub.status, occurred_at: atOf(event),
        }]);
      }
    } else if (event.type === "customer.subscription.deleted") {
      const raw = event.data.object as Stripe.Subscription;
      const sub = await currentSub(raw);
      const uid = await userIdFor(sub);
      const prior = await priorState(uid);
      // A delete can be overtaken by a later update only if the subscription actually came
      // back, which currentSub would show. Trust the re-read over the event payload.
      if (uid && sub.status !== "active" && sub.status !== "trialing") {
        await writeProfile(uid, {
          plan: "free",
          plan_status: "canceled",
          trial_end: null,
          current_period_end: null,
          cancel_at_period_end: false,
          plan_interval: null,
          plan_amount_cents: null,
        });
        // What churned is what they were paying before this event, which is the only
        // place that number still exists: the profile write above has just erased it.
        // A trial that lapsed was never revenue, so it churns zero MRR and shows up in
        // the cohort table instead.
        const wasPaying = prior?.plan_status === "active";
        const lost = wasPaying ? mrrOf(prior?.plan_amount_cents ?? null, prior?.plan_interval ?? null) : 0;
        await ledger([{
          event_id: event.id, event_type: event.type, kind: "canceled",
          user_id: uid, subscription_id: sub.id,
          plan: prior?.plan ?? null, plan_interval: prior?.plan_interval ?? null,
          currency: sub.items?.data?.[0]?.price?.currency ?? null,
          mrr_cents: lost, mrr_delta_cents: -lost,
          status: sub.status, occurred_at: atOf(event),
          meta: { was: prior?.plan_status ?? null },
        }]);
      } else if (uid) {
        await writeProfile(uid, subPatch(sub));
      }
    } else if (event.type === "customer.subscription.updated") {
      const sub = await currentSub(event.data.object as Stripe.Subscription);
      const uid = await userIdFor(sub);
      const prior = await priorState(uid);
      if (uid) {
        const patch = subPatch(sub);
        await writeProfile(uid, patch);

        // One Stripe event can carry several of our facts. A subscription.updated that
        // converts a trial AND schedules a cancellation is two things that happened, and
        // collapsing them into one row loses whichever we decided mattered less. The kind
        // is part of the uniqueness key precisely so a single event can write more than
        // one row without colliding with itself.
        const rows: LedgerRow[] = [];
        const base = {
          event_id: event.id, event_type: event.type,
          user_id: uid, subscription_id: sub.id,
          plan: sub.metadata?.plan ?? patch.plan, plan_interval: patch.plan_interval,
          currency: sub.items?.data?.[0]?.price?.currency ?? null,
          status: sub.status, occurred_at: atOf(event),
        };
        const nowMrr = mrrOf(patch.plan_amount_cents, patch.plan_interval);
        const wasMrr = mrrOf(prior?.plan_amount_cents ?? null, prior?.plan_interval ?? null);

        if (prior?.plan_status === "trialing" && sub.status === "active") {
          rows.push({ ...base, kind: "trial_converted", mrr_cents: nowMrr, mrr_delta_cents: nowMrr });
        } else if (prior?.plan_status === "active" && sub.status === "active" && nowMrr !== wasMrr) {
          rows.push({
            ...base, kind: nowMrr > wasMrr ? "upgraded" : "downgraded",
            mrr_cents: nowMrr, mrr_delta_cents: nowMrr - wasMrr,
            meta: { from_cents: wasMrr, to_cents: nowMrr },
          });
        }
        if (sub.status === "past_due" && prior?.plan_status !== "past_due") {
          rows.push({ ...base, kind: "past_due", mrr_cents: nowMrr });
        }
        // Intent to leave is the earliest churn signal there is, and it arrives days or
        // weeks before the cancellation does. Recording it separately is what makes a
        // save attempt possible at all.
        if (!prior?.cancel_at_period_end && patch.cancel_at_period_end) {
          rows.push({ ...base, kind: "cancel_scheduled", mrr_cents: nowMrr });
        } else if (prior?.cancel_at_period_end && !patch.cancel_at_period_end) {
          rows.push({ ...base, kind: "cancel_reverted", mrr_cents: nowMrr });
        }
        await ledger(rows);
      }
    } else if (event.type === "invoice.paid") {
      // Cash, as opposed to recurring value. An annual invoice is $99.99 of cash on one
      // day and $8.33 of MRR every month, and a dashboard that adds those together is
      // wrong in both directions, so they are separate columns and this writes only cash.
      const inv = event.data.object as Stripe.Invoice;
      const uid = await userIdForCustomer(idOf(inv.customer));
      const cycle = inv.billing_reason === "subscription_cycle";
      await ledger([{
        event_id: event.id, event_type: event.type,
        // Only a renewal counts as a renewal. The first invoice of a subscription is also
        // invoice.paid, and calling it one would double-count every new subscriber as a
        // returning one. It still carries its cash, which is the point.
        kind: cycle ? "renewed" : "other",
        user_id: uid, subscription_id: idOf((inv as unknown as { subscription?: unknown }).subscription),
        amount_cents: typeof inv.amount_paid === "number" ? inv.amount_paid : 0,
        currency: inv.currency ?? null,
        status: inv.status ?? null, occurred_at: atOf(event),
        meta: { billing_reason: inv.billing_reason ?? null },
      }]);
    } else if (event.type === "invoice.payment_failed") {
      const inv = event.data.object as Stripe.Invoice;
      const uid = await userIdForCustomer(idOf(inv.customer));
      await ledger([{
        event_id: event.id, event_type: event.type, kind: "payment_failed",
        user_id: uid, subscription_id: idOf((inv as unknown as { subscription?: unknown }).subscription),
        // No money moved, so no cash. A failed payment is a warning, not a transaction.
        amount_cents: 0, currency: inv.currency ?? null,
        status: inv.status ?? null, occurred_at: atOf(event),
        meta: { attempt: inv.attempt_count ?? null },
      }]);
    } else if (event.type === "charge.refunded") {
      const ch = event.data.object as Stripe.Charge;
      const uid = await userIdForCustomer(idOf(ch.customer));
      // charge.amount_refunded is CUMULATIVE. On a second partial refund it reports the
      // running total, so recording it would count the first refund twice. The refunds
      // list is newest first, so the most recent entry is what this event is about;
      // amount_refunded is the fallback for the ordinary case of a single full refund.
      const latest = ch.refunds?.data?.[0]?.amount;
      const amount = typeof latest === "number" ? latest : (ch.amount_refunded ?? 0);
      await ledger([{
        event_id: event.id, event_type: event.type, kind: "refunded",
        user_id: uid,
        // Refunds are negative cash. Storing them as a positive number in a separate
        // column is how a net revenue figure ends up accidentally gross.
        amount_cents: -Math.abs(amount), currency: ch.currency ?? null,
        status: ch.status ?? null, occurred_at: atOf(event),
        meta: { cumulative_cents: ch.amount_refunded ?? null, partial: ch.refunded !== true },
      }]);
    }
  } catch (e) {
    // Return 500 so Stripe retries. Swallowing the error would leave a paying customer
    // on the free plan with no second chance.
    console.error("webhook handler failed", event.type, String(e));
    return new Response(JSON.stringify({ error: "handler failed" }), { status: 500 });
  }
  return new Response(JSON.stringify({ received: true }), { headers: { "Content-Type": "application/json" } });
});
