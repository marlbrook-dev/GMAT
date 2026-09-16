# Supabase (Phase 3)

Project: `meridian-prep` (ref ftsqwbzhkzuudogkvoqa, us-east-1, Free plan) in marlbrook-dev's Org. URL https://ftsqwbzhkzuudogkvoqa.supabase.co. The app embeds the publishable key (safe for browsers; Row Level Security protects data).

Applied migration `meridian_prep_core`: profiles (state_blob jsonb, plan, consent_at, trigger auto-creates row on signup), attempts, events, sessions, RLS policies, `item_stats` view (per-question correct rate and median time for content review).

## One-time settings Hunter must do in the Supabase dashboard (Authentication > URL Configuration)
- Site URL: your Cloudflare Pages URL, e.g. https://gmat-xxxx.pages.dev/app/
- Redirect URLs: add https://gmat-xxxx.pages.dev/** (and your custom domain later)
Magic-link sign-in will not complete until this is set. Optional: Authentication > Providers > Google (needs a Google Cloud OAuth client).

## How sync works in the app
Anonymous use stores everything in localStorage, under a key that names the exam so the two trainers on this origin never read each other's progress. After sign-in, the app pulls `profiles.state_blob`; if the account has more answers than this device, the account wins (device copy stays until overwritten).

**Known limit, multi-exam.** `profiles.state_blob` holds one state per user, while `attempts`, `skill_ratings` and `review_queue` are keyed by `(user_id, exam)`. With two trainers live, a student who practices both would otherwise have the second app overwrite the first exam's blob. The app refuses that write and tells the student on the Account page that cross-device sync for the second exam is unavailable; device storage still holds it and nothing is lost. The fix is `supabase/migrations/PROPOSED_exam_states.sql`, which is written but deliberately not applied: it changes the owner's live project and needs his go-ahead. Every answer also inserts a row into `attempts`, product events go to `events`, and the full state is upserted 2.5 s after each change. Delete my data wipes attempts, events, sessions and the blob.

## Stripe Checkout (live account configured; secrets outstanding)

Edge functions `create-checkout-session` (JWT-protected) and `stripe-webhook`
(Stripe-signature-protected) are deployed to this project; sources live in
`supabase/functions/`.

### Already created in the live Stripe account (`acct_1UGMl23VQZ93CQqj`, Start from Nowhere)

| Env var | Price | Stripe price ID |
|---|---|---|
| `STRIPE_PRICE_PLUS_MONTHLY` | $4.99 / month | `price_1UGMyq3VQZ93CQqjt5peOrP0` |
| `STRIPE_PRICE_PLUS_ANNUAL` | $49.99 / year | `price_1UGMyw3VQZ93CQqjK1k3uSzo` |
| `STRIPE_PRICE_PRO_MONTHLY` | $9.99 / month | `price_1UGMyz3VQZ93CQqjCQMENicC` |
| `STRIPE_PRICE_PRO_ANNUAL` | $99.99 / year | `price_1UGMz43VQZ93CQqj75nFhzSg` |

Products: Plus `prod_VGuoI1nGL4DRgl`, Pro `prod_VGuoenEOHuMme6`. Annual is priced at
ten months of the monthly rate, so roughly two months free; change the annual prices in
Stripe if you want a different ratio.

Webhook endpoint `we_1UGMz83VQZ93CQqjDEmO5iMj` is created and enabled, pointing at
`https://ftsqwbzhkzuudogkvoqa.supabase.co/functions/v1/stripe-webhook` for
`checkout.session.completed`, `customer.subscription.updated` and
`customer.subscription.deleted`.

### What is still required before a single charge can succeed

Only the account owner can do these; they cannot be done from the repo.

1. **Set the Edge Function secrets** (Supabase dashboard > Edge Functions > Secrets, or
   `supabase secrets set`): `STRIPE_SECRET_KEY`, `STRIPE_WEBHOOK_SECRET`, the four
   price IDs above, and `SITE_URL=https://startfromnowhere.com`. Optionally
   `STRIPE_TRIAL_DAYS` (defaults to 7; set `0` to sell with no trial).
   The signing secret is on the endpoint's page under Stripe > Developers > Webhooks.
   Never commit either secret.
2. **Confirm the account can actually take charges.** This account had no products,
   prices or webhooks before this pass, which suggests onboarding may be incomplete.
   Check Stripe > Settings that charges and payouts are enabled and a bank account is
   attached, or money will authorize and never settle.
3. **Legal.** Stripe requires visible terms and a refund policy. `terms.html` and
   `privacy.html` exist but have not had counsel review, and neither yet describes the
   trial, the renewal terms or how to cancel. Fix that before charging anyone.

### The free trial

`create-checkout-session` sets `trial_period_days` (7 by default) and
`payment_method_collection: "always"`, so Stripe takes the card up front, charges
nothing during the trial, and converts automatically unless the student cancels.

Note for anyone changing the webhook: a checkout session that starts a trial settles as
`payment_status: "no_payment_required"`, **not** `"paid"`. The handler accepts both. An
earlier version checked only for `"paid"` and would have left every trialing subscriber
stuck on the free plan.

### Two flags, deliberately separate (`src/app_template.html`)

- `PAYMENTS_LIVE` (now `true`) shows the plan buttons and runs Checkout. Safe on its
  own: a missing secret just means the button reports that checkout could not open.
- `FREE_LIMITS_LIVE` (still `false`) turns on the free-tier caps of 10 questions a day
  and 1 mock section a month. That flag takes something away from people already using
  the trainer, and the Account page has been promising early users generous
  grandfathering, so it is a separate decision. Turning it on without deciding what
  grandfathering means would break that promise.

Flow: app calls `create-checkout-session` with the signed-in user's JWT > Stripe-hosted
checkout > webhook sets `profiles.plan`. Card data never touches our code. Cancel and
downgrade should later move to the Stripe Customer Portal; today a student who wants to
cancel has to email, which is a gap worth closing early.

## Admin + BI + CRM (applied)

Migrations `admin_bi` and `partner_crm` are live. Admin access = email in `app_admins`
(seeded: hroberts@winthropcapital.com). `is_admin()` gates everything server-side; the app
shows the Admin tab only after `rpc('is_admin')` returns true. BI reads a single
`admin_bi()` RPC (aggregates only); the Partners CRM uses `crm_contacts`/`crm_notes`
with admin-only RLS. Add an admin: `insert into app_admins(email) values ('...');`
Preview the dashboard layout with sample data at `/app/#admin-preview` (no real data).
