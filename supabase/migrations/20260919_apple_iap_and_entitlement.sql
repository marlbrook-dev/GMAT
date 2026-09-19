-- Applied 2026-09-19. Apple in-app purchase alongside Stripe, and the entitlement layer
-- that makes two payment sources safe.
--
-- The important change is not the Apple table. It is that profiles.plan stops being the
-- answer to "what has this person paid for". Today the Stripe webhook writes that column
-- and the app reads it, which works precisely because there is exactly one processor. Add
-- a second and that column becomes a race: whichever webhook fired last wins, and a user
-- who subscribed on iOS gets downgraded the next time a Stripe event lands on their row.
--
-- So plan stays exactly as it is, owned by Stripe and untouched by anything here, and a
-- function derives the effective entitlement from every source. Nothing about the
-- existing Stripe path changes, which is deliberate: it is live and taking money.
--
-- Tested by src/sql/smoke_entitlement.sql, which rolls itself back.

create type public.billing_source as enum ('stripe', 'apple', 'google', 'comp');

create table if not exists public.apple_subscriptions (
  -- Apple's identity for a subscription across renewals, upgrades and resubscribes. Not
  -- the transaction id, which changes every renewal and would create a new row a month.
  original_transaction_id text primary key,
  user_id        uuid references auth.users(id) on delete set null,
  product_id     text not null,
  tier           text not null check (tier in ('plus', 'pro')),
  status         text not null check (status in
                   ('active','trialing','grace','billing_retry','expired','revoked','refunded')),
  expires_at     timestamptz,
  auto_renew     boolean,
  is_trial       boolean default false,
  -- Sandbox and production share nothing. A sandbox receipt must never grant production
  -- access, and Apple's reviewers test in sandbox, so both have to work side by side.
  environment    text not null default 'Production' check (environment in ('Sandbox','Production')),
  -- Apple does not order notifications any more than Stripe does, so every write carries
  -- the signed date it came from and an older one is discarded rather than applied.
  last_signed_ms bigint,
  raw            jsonb,
  created_at     timestamptz not null default now(),
  updated_at     timestamptz not null default now()
);

create index if not exists apple_subs_user_idx on public.apple_subscriptions (user_id);
create index if not exists apple_subs_status_idx on public.apple_subscriptions (status, expires_at);

-- Nobody reads this table directly from a client. The entitlement function is the only
-- interface, and it is security definer.
alter table public.apple_subscriptions enable row level security;
revoke all on public.apple_subscriptions from public, anon, authenticated;

-- What a person is actually entitled to, from every source at once.
--
-- The rule is the highest tier any active source grants. Not the most recent, which would
-- let an expired Apple row beat a live Stripe one, and not the first found, which would
-- depend on join order.
create or replace function public.entitlement(p_user uuid)
returns table (plan text, source public.billing_source, expires_at timestamptz,
               managed_by text, double_billed boolean)
language plpgsql stable security definer set search_path = public, pg_temp as $$
declare
  v_stripe_plan text := 'free';
  v_stripe_end timestamptz;
  v_apple_plan text := 'free';
  v_apple_end timestamptz;
  v_apple_env text;
  rank_of int;
begin
  -- Stripe, read from the columns its webhook already maintains. Unchanged semantics:
  -- trialing, active and past_due all keep access, which is what the app does today.
  select coalesce(p.plan, 'free'), p.current_period_end
    into v_stripe_plan, v_stripe_end
  from public.profiles p
  where p.id = p_user
    and coalesce(p.plan_status, '') in ('trialing', 'active', 'past_due');
  if v_stripe_plan is null then v_stripe_plan := 'free'; end if;

  -- Apple. grace and billing_retry keep access: Apple is still trying to charge, and
  -- cutting someone off mid retry is how you turn a failed card into a cancellation.
  select s.tier, s.expires_at, s.environment
    into v_apple_plan, v_apple_end, v_apple_env
  from public.apple_subscriptions s
  where s.user_id = p_user
    and s.status in ('active', 'trialing', 'grace', 'billing_retry')
    and (s.expires_at is null or s.expires_at > now())
  order by case s.tier when 'pro' then 2 when 'plus' then 1 else 0 end desc,
           s.expires_at desc nulls last
  limit 1;
  if v_apple_plan is null then v_apple_plan := 'free'; end if;

  rank_of := case when v_stripe_plan = 'pro' then 2 when v_stripe_plan = 'plus' then 1 else 0 end;

  if (case when v_apple_plan = 'pro' then 2 when v_apple_plan = 'plus' then 1 else 0 end) > rank_of then
    return query select v_apple_plan, 'apple'::public.billing_source, v_apple_end,
      'apple'::text,
      -- Both paying is a fact the person is entitled to know, not something to absorb
      -- quietly. The Account page surfaces it and offers to sort it out.
      (rank_of > 0);
  elsif rank_of > 0 then
    return query select v_stripe_plan, 'stripe'::public.billing_source, v_stripe_end,
      'stripe'::text, (v_apple_plan <> 'free');
  else
    return query select 'free'::text, 'stripe'::public.billing_source, null::timestamptz,
      'none'::text, false;
  end if;
end $$;

create or replace function public.my_entitlement()
returns table (plan text, source public.billing_source, expires_at timestamptz,
               managed_by text, double_billed boolean)
language sql stable security definer set search_path = public, pg_temp as $$
  select * from public.entitlement(auth.uid());
$$;

revoke all on function public.entitlement(uuid) from public, anon, authenticated;
revoke all on function public.my_entitlement() from public, anon;
grant execute on function public.my_entitlement() to authenticated;

-- Linking a purchase to an account. The app sends the originalTransactionId it got from
-- StoreKit; the edge function has already verified and stored the row. This only claims
-- an unclaimed row, so one person cannot attach themselves to another's subscription.
create or replace function public.claim_apple_subscription(p_original_transaction_id text)
returns table (plan text, claimed boolean)
language plpgsql security definer set search_path = public, pg_temp as $$
declare
  v_uid uuid := auth.uid();
  v_owner uuid;
  v_tier text;
begin
  if v_uid is null then
    raise exception 'sign in required' using errcode = '28000';
  end if;
  select s.user_id, s.tier into v_owner, v_tier
  from public.apple_subscriptions s
  where s.original_transaction_id = p_original_transaction_id;

  if v_tier is null then
    -- The notification has not arrived yet. Not an error: StoreKit is often faster than
    -- the server notification, so the client retries rather than showing a failure.
    return query select 'free'::text, false;
  elsif v_owner is null then
    update public.apple_subscriptions
       set user_id = v_uid, updated_at = now()
     where original_transaction_id = p_original_transaction_id;
    return query select v_tier, true;
  elsif v_owner = v_uid then
    return query select v_tier, true;
  else
    -- Already owned by somebody else. Family Sharing and resold devices both produce
    -- this, and silently reassigning would hand one person another's subscription.
    raise exception 'that subscription is already attached to a different account'
      using errcode = '42501';
  end if;
end $$;

revoke all on function public.claim_apple_subscription(text) from public, anon;
grant execute on function public.claim_apple_subscription(text) to authenticated;
