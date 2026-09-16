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

Four edge functions are deployed; sources live in `supabase/functions/`.

| Function | Auth | What it does |
|---|---|---|
| `create-checkout-session` | JWT | Opens Stripe Checkout for a plan. |
| `stripe-webhook` | Stripe signature (`verify_jwt=false`) | Writes plan and billing state onto `profiles`. |
| `cancel-subscription` | JWT | Sets `cancel_at_period_end` on the caller's own subscription. Also resumes with `{resume:true}`. |
| `create-portal-session` | JWT | Opens the Stripe billing portal for invoices and card changes. |

**Cancelling deliberately does not go through the billing portal.** The portal needs a
portal configuration on the Stripe account and there is none yet, so a subscriber would be
unable to cancel at all. `cancel-subscription` needs nothing but `STRIPE_SECRET_KEY`, and
the portal reports plainly when it is not configured. Neither function ever takes a
subscription or customer id from the request body: both read it from the caller's own
RLS-scoped `profiles` row, so the JWT alone decides whose subscription is touched.

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
3. **Activate the Stripe billing portal.** Stripe > Settings > Billing > Customer portal
   > Activate. The account has zero portal configurations today, so Manage Billing returns
   a 503 explaining it is off. Cancelling is unaffected. The API key available to tooling
   here cannot create the configuration, so this is a dashboard click.
4. **Create the `billing@startfromnowhere.com` mailbox.** Terms, Privacy and the pricing
   page all point at it. The domain's mail is routed to a cPanel host
   (`MX -> _dc-mx.feb1e7357ba1.startfromnowhere.com` -> `162.241.217.51`, SPF
   `include:websitewelcome.com`), so the mailbox is created there, or by moving the domain
   to Cloudflare Email Routing and forwarding to the owner's inbox. Worth confirming
   `legal@`, `privacy@` and `editors@` actually deliver while you are in there; they are
   already published on the site and nothing here can verify them.
5. **Enable leaked-password protection** (Authentication > Policies). The app signs in with
   magic links rather than passwords, so this is precautionary, but it is a free toggle.
6. **Legal review.** `terms.html` and `privacy.html` now describe the trial, renewal,
   one-click cancellation, the 72-hour refund window and Stripe as processor, and they no
   longer carry a "draft template" label because they are the operative terms for real
   transactions. They still have not been reviewed by counsel. That is the last open item
   before charging at any volume.

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

## Advisor findings and the PUBLIC grant trap (2026-09-16)

`revoke execute on function f() from anon, authenticated` **does not stop anon calling
`f()`**. Postgres grants EXECUTE on every new function to `PUBLIC`, and `anon` inherits it;
revoking a role's own grant leaves the `PUBLIC` grant in place. The tell is a leading
`=X/postgres` in `pg_proc.proacl`. An earlier migration made exactly this mistake, and
checking the per-role grants afterwards looked clean, because the per-role grants *were*
clean. `20260916_revoke_public_execute_and_rls_initplan.sql` revokes from `PUBLIC` and the
advisor count for anon-callable SECURITY DEFINER functions went from 11 to 1.

Nothing was exploitable through that gap: the five trigger functions return `trigger`,
which PostgREST will not expose and Postgres refuses to call directly, and every `admin_*`
function opens with `if not is_admin() then raise exception 'admin only'`.

**Findings that remain, and are intentional:**

- `is_admin()` is callable by anon and authenticated. The app calls it to decide whether to
  show the Admin tab. It reads `auth.jwt()` and returns false for anyone not on the admin
  list, so an anonymous call learns nothing.
- The six `admin_*` RPCs are callable by authenticated. They have to be: that is how an
  admin calls them. Each one checks `is_admin()` server-side first.

Performance items fixed in the same migration: every `auth.uid()` inside an RLS policy is
now `(select auth.uid())` so it is evaluated once per statement rather than once per row,
and the three unindexed foreign keys (`forum_posts.user_id`, `forum_threads.user_id`,
`sessions.user_id`) have covering indexes. Left alone: five unused indexes (too early to
call them dead) and the two overlapping SELECT policies on `profiles` (merging them is a
micro-optimisation on a table this size and touches access control, so it is not worth the
risk today).

## Validating billing changes

`node src/smoke_billing.js` (with `CHROMIUM_PATH` and `NODE_PATH` set, see the file header)
drives the built app in headless Chromium and asserts that the free tier renders no
checkout control signed out or signed in, that the Account card states the next money event
correctly in all six subscription states, and that Cancel Plan appears whenever there is
something to cancel. Run it alongside `python3 src/build.py` and `cd src && node test.js`
after touching anything in the billing path.
