// Opens the Stripe billing portal for the signed-in user, so cancelling, switching plans
// and updating a card all happen on Stripe's pages and never touch our code.
//
// This exists because terms.html and the pricing page promise "cancel anytime from your
// account". Without it that promise was false: the only way out was to email us, which is
// exactly the pattern card networks and consumer regulators treat as a dark pattern.
//
// Secrets (supabase/README.md): STRIPE_SECRET_KEY, SITE_URL.
import Stripe from "npm:stripe@17";
import { createClient } from "jsr:@supabase/supabase-js@2";

const stripe = new Stripe(Deno.env.get("STRIPE_SECRET_KEY") ?? "", { apiVersion: "2024-06-20" });
const SITE = Deno.env.get("SITE_URL") ?? "https://startfromnowhere.com";
const SUPPORT = Deno.env.get("SUPPORT_EMAIL") ?? "billing@startfromnowhere.com";
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

    // RLS limits this select to the caller's own row, so the JWT alone decides whose
    // billing portal opens. Never take a customer id from the request body.
    const { data: profile } = await supabase
      .from("profiles").select("stripe_customer_id").eq("id", user.id).maybeSingle();

    let customer = profile?.stripe_customer_id ?? null;
    if (!customer && user.email) {
      // Fallback for anyone who subscribed before we stored the customer id.
      const found = await stripe.customers.list({ email: user.email, limit: 1 });
      customer = found.data[0]?.id ?? null;
    }
    if (!customer) return json({ error: "No subscription found for this account." }, 404);

    try {
      const session = await stripe.billingPortal.sessions.create({
        customer,
        return_url: `${SITE}/app/#account`,
      });
      return json({ url: session.url });
    } catch (e) {
      // The portal needs a configuration to exist on the Stripe account, and it does not
      // until someone activates it in Stripe > Settings > Billing > Customer portal. Say
      // so plainly instead of throwing a generic 500: "something went wrong" would read as
      // a stall to someone trying to manage their money. Cancelling does not come through
      // here at all (see cancel-subscription), so nobody is ever trapped by this.
      const msg = String(e);
      if (/configuration/i.test(msg)) {
        return json({
          error: "Invoices and card changes are not switched on yet. You can still cancel with the Cancel Plan button, or email " + SUPPORT + " for anything else.",
          reason: "portal_not_configured",
        }, 503);
      }
      throw e;
    }
  } catch (e) {
    return json({ error: String(e) }, 500);
  }
});
