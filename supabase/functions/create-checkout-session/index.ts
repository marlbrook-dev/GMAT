// Creates a Stripe Checkout session for a signed-in user. Card data never touches our code:
// the browser is redirected to Stripe-hosted checkout. Requires secrets (supabase/README.md):
// STRIPE_SECRET_KEY, STRIPE_PRICE_MONTHLY, STRIPE_PRICE_QUARTERLY, STRIPE_PRICE_ANNUAL, SITE_URL.
import Stripe from "npm:stripe@17";
import { createClient } from "jsr:@supabase/supabase-js@2";

const stripe = new Stripe(Deno.env.get("STRIPE_SECRET_KEY") ?? "", { apiVersion: "2024-06-20" });
const PRICES: Record<string, string | undefined> = {
  monthly: Deno.env.get("STRIPE_PRICE_MONTHLY"),
  quarterly: Deno.env.get("STRIPE_PRICE_QUARTERLY"),
  annual: Deno.env.get("STRIPE_PRICE_ANNUAL"),
};
const SITE = Deno.env.get("SITE_URL") ?? "https://startfromnowhere.com";
const cors = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Headers": "authorization, x-client-info, apikey, content-type",
};

Deno.serve(async (req: Request) => {
  if (req.method === "OPTIONS") return new Response("ok", { headers: cors });
  try {
    const supabase = createClient(
      Deno.env.get("SUPABASE_URL")!,
      Deno.env.get("SUPABASE_ANON_KEY")!,
      { global: { headers: { Authorization: req.headers.get("Authorization")! } } },
    );
    const { data: { user } } = await supabase.auth.getUser();
    if (!user) return new Response(JSON.stringify({ error: "Not signed in" }), { status: 401, headers: cors });
    const { plan } = await req.json();
    const price = PRICES[plan];
    if (!price) return new Response(JSON.stringify({ error: "Unknown plan or Stripe not configured" }), { status: 400, headers: cors });
    const session = await stripe.checkout.sessions.create({
      mode: "subscription",
      line_items: [{ price, quantity: 1 }],
      customer_email: user.email ?? undefined,
      client_reference_id: user.id,
      metadata: { user_id: user.id, plan },
      subscription_data: { metadata: { user_id: user.id, plan } },
      success_url: `${SITE}/app/?checkout=success`,
      cancel_url: `${SITE}/app/?checkout=cancelled`,
      allow_promotion_codes: true,
    });
    return new Response(JSON.stringify({ url: session.url }), { headers: { ...cors, "Content-Type": "application/json" } });
  } catch (e) {
    return new Response(JSON.stringify({ error: String(e) }), { status: 500, headers: cors });
  }
});
