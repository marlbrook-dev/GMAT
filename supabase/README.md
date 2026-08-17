# Supabase (Phase 3)

Project: `meridian-prep` (ref ftsqwbzhkzuudogkvoqa, us-east-1, Free plan) in marlbrook-dev's Org. URL https://ftsqwbzhkzuudogkvoqa.supabase.co. The app embeds the publishable key (safe for browsers; Row Level Security protects data).

Applied migration `meridian_prep_core`: profiles (state_blob jsonb, plan, consent_at, trigger auto-creates row on signup), attempts, events, sessions, RLS policies, `item_stats` view (per-question correct rate and median time for content review).

## One-time settings Hunter must do in the Supabase dashboard (Authentication > URL Configuration)
- Site URL: your Cloudflare Pages URL, e.g. https://gmat-xxxx.pages.dev/app/
- Redirect URLs: add https://gmat-xxxx.pages.dev/** (and your custom domain later)
Magic-link sign-in will not complete until this is set. Optional: Authentication > Providers > Google (needs a Google Cloud OAuth client).

## How sync works in the app
Anonymous use stores everything in localStorage. After sign-in, the app pulls `profiles.state_blob`; if the account has more answers than this device, the account wins (device copy stays until overwritten). Every answer also inserts a row into `attempts`, product events go to `events`, and the full state is upserted 2.5 s after each change. Delete my data wipes attempts, events, sessions and the blob.

## Stripe Checkout (scaffolded, not yet live)

Edge functions `create-checkout-session` (JWT-protected) and `stripe-webhook` (Stripe-signature-protected) are deployed to this project; sources live in `supabase/functions/`. The app's plan buttons stay "Coming soon" until `PAYMENTS_LIVE` is flipped to `true` in `src/app_template.html`.

To go live:
1. In Stripe: create a product with three recurring prices ($19.99 monthly, $44.99 quarterly, $119.99 annual). Copy the three price IDs.
2. In Stripe > Developers > Webhooks: add endpoint `https://ftsqwbzhkzuudogkvoqa.supabase.co/functions/v1/stripe-webhook` with events `checkout.session.completed`, `customer.subscription.updated`, `customer.subscription.deleted`. Copy the signing secret.
3. Supabase dashboard > Edge Functions > Secrets (or `supabase secrets set`): `STRIPE_SECRET_KEY`, `STRIPE_WEBHOOK_SECRET`, `STRIPE_PRICE_MONTHLY`, `STRIPE_PRICE_QUARTERLY`, `STRIPE_PRICE_ANNUAL`, `SITE_URL` (https://startfromnowhere.com).
4. Flip `PAYMENTS_LIVE` to `true`, rebuild, deploy.
5. Legal first: Stripe requires visible terms and a refund policy; have counsel review `terms.html` and `privacy.html` before charging anyone.

Flow: app calls `create-checkout-session` with the signed-in user's JWT > Stripe-hosted checkout > webhook sets `profiles.plan`. Card data never touches our code. Cancel/downgrade later adds the Stripe Customer Portal.

## Admin + BI + CRM (applied)

Migrations `admin_bi` and `partner_crm` are live. Admin access = email in `app_admins`
(seeded: hroberts@winthropcapital.com). `is_admin()` gates everything server-side; the app
shows the Admin tab only after `rpc('is_admin')` returns true. BI reads a single
`admin_bi()` RPC (aggregates only); the Partners CRM uses `crm_contacts`/`crm_notes`
with admin-only RLS. Add an admin: `insert into app_admins(email) values ('...');`
Preview the dashboard layout with sample data at `/app/#admin-preview` (no real data).
