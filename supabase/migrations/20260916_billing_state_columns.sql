-- Billing state on profiles, written only by the Stripe webhook (service role).
--
-- Before this, the only billing fact we stored was profiles.plan. That is not enough to
-- run a subscription business honestly: the app could not tell a student when the trial
-- ends or when the first charge lands, and nothing held the Stripe customer id, so there
-- was no way to open the Stripe billing portal and no way to cancel in the product.
--
-- None of these columns appear in the column-level grants from
-- 20260916_harden_plan_column_and_rpc_surface.sql, so anon and authenticated cannot write
-- them. The webhook runs as service_role and bypasses that. Read is still governed by the
-- existing "own row" RLS select policy, which is what lets the Account page show status.
alter table public.profiles
  add column if not exists stripe_customer_id     text,
  add column if not exists stripe_subscription_id text,
  -- Mirrors Stripe's subscription.status: trialing | active | past_due | canceled.
  -- 'none' (or null) means the account has never subscribed.
  add column if not exists plan_status            text,
  add column if not exists trial_end              timestamptz,
  add column if not exists current_period_end     timestamptz,
  add column if not exists cancel_at_period_end   boolean not null default false;

-- One Stripe customer per account. Checkout passes customer_email, so Stripe would
-- otherwise mint a fresh customer on every checkout and a student could restart the free
-- trial indefinitely by subscribing again.
create unique index if not exists profiles_stripe_customer_id_key
  on public.profiles (stripe_customer_id)
  where stripe_customer_id is not null;

comment on column public.profiles.plan_status is
  'Stripe subscription status. plan holds the tier (free/plus/pro); this holds whether it is trialing, active, past_due or canceled.';
