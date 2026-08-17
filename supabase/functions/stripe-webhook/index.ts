// Stripe webhook: keeps profiles.plan in sync with subscription state.
// Deployed with verify_jwt=false; authentication is Stripe's signature check instead
// (STRIPE_WEBHOOK_SECRET). Point a Stripe webhook endpoint at this function for events:
// checkout.session.completed, customer.subscription.updated, customer.subscription.deleted.
import Stripe from "npm:stripe@17";
import { createClient } from "jsr:@supabase/supabase-js@2";

const stripe = new Stripe(Deno.env.get("STRIPE_SECRET_KEY") ?? "", { apiVersion: "2024-06-20" });
const secret = Deno.env.get("STRIPE_WEBHOOK_SECRET") ?? "";
const admin = createClient(Deno.env.get("SUPABASE_URL")!, Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!);

async function setPlan(userId: string, plan: string) {
  await admin.from("profiles").update({ plan }).eq("id", userId);
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
  if (event.type === "checkout.session.completed") {
    const s = event.data.object as Stripe.Checkout.Session;
    const uid = s.client_reference_id ?? s.metadata?.user_id;
    const plan = s.metadata?.plan ?? "plus";
    if (uid && s.payment_status === "paid") await setPlan(uid, plan);
  } else if (event.type === "customer.subscription.deleted") {
    const sub = event.data.object as Stripe.Subscription;
    if (sub.metadata?.user_id) await setPlan(sub.metadata.user_id, "free");
  } else if (event.type === "customer.subscription.updated") {
    const sub = event.data.object as Stripe.Subscription;
    if (sub.metadata?.user_id) {
      const active = ["active", "trialing"].includes(sub.status);
      await setPlan(sub.metadata.user_id, active ? (sub.metadata?.plan ?? "plus") : "free");
    }
  }
  return new Response(JSON.stringify({ received: true }), { headers: { "Content-Type": "application/json" } });
});
