// Self-serve cancel and resume, straight against the Stripe API.
//
// Why this exists separately from create-portal-session: the billing portal needs a portal
// configuration on the Stripe account, and until someone activates it the portal cannot
// open at all. Cancelling is the one thing a subscriber must never be unable to do, so it
// gets a path that needs nothing but STRIPE_SECRET_KEY. The portal stays as the richer
// surface for invoices, card changes and plan switches.
//
// Cancelling sets cancel_at_period_end, which is what the Terms promise: no further
// charges, and access continues to the end of the period already paid for. During a trial
// that means the trial simply runs out and no charge is ever taken.
//
// Secrets (supabase/README.md): STRIPE_SECRET_KEY.
import Stripe from "npm:stripe@17";
import { createClient } from "jsr:@supabase/supabase-js@2";

const stripe = new Stripe(Deno.env.get("STRIPE_SECRET_KEY") ?? "", { apiVersion: "2024-06-20" });
const cors = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Headers": "authorization, x-client-info, apikey, content-type",
};
const json = (body: unknown, status = 200) =>
  new Response(JSON.stringify(body), { status, headers: { ...cors, "Content-Type": "application/json" } });

Deno.serve(async (req: Request) => {
  if (req.method === "OPTIONS") return new Response("ok", { headers: cors });
  try {
    const supabase = createClient(
      Deno.env.get("SUPABASE_URL")!,
      Deno.env.get("SUPABASE_ANON_KEY")!,
      { global: { headers: { Authorization: req.headers.get("Authorization")! } } },
    );
    const { data: { user } } = await supabase.auth.getUser();
    if (!user) return json({ error: "Not signed in" }, 401);

    const body = await req.json().catch(() => ({}));
    const resume = body?.resume === true;

    // The subscription id comes from the caller's own profile row, never from the request
    // body. RLS scopes this select to that row, so the JWT alone decides whose
    // subscription can be touched.
    const { data: profile } = await supabase
      .from("profiles").select("stripe_subscription_id, stripe_customer_id").eq("id", user.id).maybeSingle();

    let subId = profile?.stripe_subscription_id ?? null;
    if (!subId && profile?.stripe_customer_id) {
      // Fallback for a row written before we stored the subscription id.
      const list = await stripe.subscriptions.list({ customer: profile.stripe_customer_id, status: "all", limit: 10 });
      subId = list.data.find((s) => s.status === "active" || s.status === "trialing" || s.status === "past_due")?.id ?? null;
    }
    if (!subId) return json({ error: "No active subscription on this account." }, 404);

    const sub = await stripe.subscriptions.update(subId, { cancel_at_period_end: !resume });

    // Mirror it immediately so the page can say the right thing without waiting on the
    // webhook. The webhook is still the source of truth and will confirm within seconds.
    const service = createClient(Deno.env.get("SUPABASE_URL")!, Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!);
    await service.from("profiles")
      .update({ cancel_at_period_end: !resume, plan_status: sub.status })
      .eq("id", user.id);

    return json({
      ok: true,
      cancel_at_period_end: !resume,
      status: sub.status,
      // Callers show this date: during a trial it is the trial end, otherwise the paid
      // period end. Either way it is the day access stops.
      access_until: typeof sub.current_period_end === "number"
        ? new Date(sub.current_period_end * 1000).toISOString()
        : null,
    });
  } catch (e) {
    return json({ error: String(e) }, 500);
  }
});
