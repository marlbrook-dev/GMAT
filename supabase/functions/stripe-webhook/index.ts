// Stripe webhook: keeps profiles in sync with subscription state.
// Deployed with verify_jwt=false; authentication is Stripe's signature check instead
// (STRIPE_WEBHOOK_SECRET). Point a Stripe webhook endpoint at this function for events:
// checkout.session.completed, customer.subscription.updated, customer.subscription.deleted.
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
        // place trial_end and the renewal date exist, and the Account page shows both.
        const sub = subId ? await stripe.subscriptions.retrieve(subId) : null;
        await writeProfile(uid, sub ? subPatch(sub) : {
          plan: s.metadata?.plan ?? "plus",
          plan_status: "active",
          stripe_customer_id: typeof s.customer === "string" ? s.customer : s.customer?.id ?? null,
        });
      }
    } else if (event.type === "customer.subscription.deleted") {
      const sub = event.data.object as Stripe.Subscription;
      const uid = await userIdFor(sub);
      if (uid) {
        await writeProfile(uid, {
          plan: "free",
          plan_status: "canceled",
          trial_end: null,
          current_period_end: null,
          cancel_at_period_end: false,
        });
      }
    } else if (event.type === "customer.subscription.updated") {
      const sub = event.data.object as Stripe.Subscription;
      const uid = await userIdFor(sub);
      if (uid) await writeProfile(uid, subPatch(sub));
    }
  } catch (e) {
    // Return 500 so Stripe retries. Swallowing the error would leave a paying customer
    // on the free plan with no second chance.
    console.error("webhook handler failed", event.type, String(e));
    return new Response(JSON.stringify({ error: "handler failed" }), { status: 500 });
  }
  return new Response(JSON.stringify({ received: true }), { headers: { "Content-Type": "application/json" } });
});
