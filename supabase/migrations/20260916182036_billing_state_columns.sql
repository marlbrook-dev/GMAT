alter table public.profiles
  add column if not exists stripe_customer_id     text,
  add column if not exists stripe_subscription_id text,
  add column if not exists plan_status            text,
  add column if not exists trial_end              timestamptz,
  add column if not exists current_period_end     timestamptz,
  add column if not exists cancel_at_period_end   boolean not null default false;

create unique index if not exists profiles_stripe_customer_id_key
  on public.profiles (stripe_customer_id)
  where stripe_customer_id is not null;

comment on column public.profiles.plan_status is
  'Stripe subscription status. plan holds the tier (free/plus/pro); this holds whether it is trialing, active, past_due or canceled.';
