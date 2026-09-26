-- Applied 2026-09-21. The billing event log, and the business view built on it.
--
-- WHY THIS EXISTS. Everything the Revenue tab shows today is read off profiles, which
-- holds one row per account describing what that account is paying RIGHT NOW. That is a
-- snapshot, and a snapshot cannot answer the four questions a subscription business
-- actually runs on: how much new revenue arrived this month, how much of it left again,
-- what share of trials convert, and what came back out as refunds. profiles is overwritten
-- on every webhook, so the moment a subscriber cancels the evidence they ever paid is
-- gone. The Revenue tab says as much in its own footnotes: "a true trial-to-paid rate
-- needs a billing event log. That is worth building before the first real cohort." This
-- is that log.
--
-- WHAT IT IS NOT. It is not a general audit trail and it is not a copy of Stripe. Stripe
-- is the ledger of record and always will be; this is an append-only stream of the few
-- facts a dashboard needs, normalised across Stripe and Apple so a chart does not have to
-- learn two vocabularies. Nothing reads it except an admin RPC.
--
-- THE LOG STARTS TODAY. It cannot be backfilled from profiles, because profiles no longer
-- remembers. Every figure derived from it is therefore "since the log began", and
-- admin_business returns log.first_at so the page can say so rather than implying the
-- numbers cover all time. Backfilling from the Stripe API is possible later and is a
-- separate job; guessing at it here would be the exact kind of number that looks right
-- and is wrong.

create table if not exists public.billing_events (
  id               bigserial primary key,
  source           public.billing_source not null,

  -- The provider's own id for the event that produced this row. Stripe and Apple both
  -- retry, so every write is an upsert keyed on this: a retry is the same fact arriving
  -- twice, not two facts.
  event_id         text not null,
  -- The provider's type string, kept verbatim for debugging. Never charted.
  event_type       text not null,

  -- Our normalised verb. A chart reads this, not event_type, so adding a processor does
  -- not mean teaching every query a new vocabulary.
  kind             text not null check (kind in (
                     'trial_started','trial_converted','subscription_started','renewed',
                     'payment_failed','past_due','cancel_scheduled','cancel_reverted',
                     'canceled','refunded','upgraded','downgraded','other')),

  user_id          uuid references auth.users(id) on delete set null,
  subscription_id  text,
  plan             text,
  plan_interval    text,

  -- Cash that actually moved, positive for a charge and negative for a refund. Zero for a
  -- state change, which is most rows. Keeping cash and recurring value in separate columns
  -- is the whole point: an annual charge of $99.99 is one cash event and $8.33 of MRR, and
  -- a dashboard that adds those together is lying in both directions.
  amount_cents     bigint not null default 0,
  currency         text,

  -- What this subscription was worth per month at the moment of the event, and how much
  -- that figure moved. The deltas sum to the MRR bridge: new plus expansion minus
  -- contraction minus churn. A trial contributes 0 to the delta until it converts,
  -- because counting a trial as revenue is how a dashboard starts lying to its owner.
  mrr_cents        bigint not null default 0,
  mrr_delta_cents  bigint not null default 0,

  status           text,
  occurred_at      timestamptz not null,
  meta             jsonb not null default '{}'::jsonb,
  created_at       timestamptz not null default now(),

  -- One provider event can produce more than one of our facts (a subscription.updated
  -- that both converts a trial and schedules a cancellation), so the kind is part of the
  -- key rather than the event alone.
  unique (source, event_id, kind)
);

-- A subscription starts once, converts once and ends once, whatever combination of event
-- types the provider uses to say so. Stripe announces a new subscription through both
-- checkout.session.completed and customer.subscription.created, with different event ids;
-- without this index that is one subscriber counted as two, and new MRR doubled.
create unique index if not exists billing_events_once_idx
  on public.billing_events (source, subscription_id, kind)
  where subscription_id is not null
    and kind in ('trial_started','trial_converted','subscription_started','canceled');

create index if not exists billing_events_at_idx   on public.billing_events (occurred_at desc);
create index if not exists billing_events_kind_idx on public.billing_events (kind, occurred_at desc);
create index if not exists billing_events_user_idx on public.billing_events (user_id, occurred_at desc);
create index if not exists billing_events_sub_idx  on public.billing_events (subscription_id);

alter table public.billing_events enable row level security;

-- No policies at all, and that is the intent: RLS with no policy denies every client. The
-- edge functions write with the service role, which bypasses RLS; admins read through
-- admin_business, which is security definer. Revoking from PUBLIC as well as the two roles
-- matters, because a grant held by PUBLIC survives revoking it from anon and authenticated
-- (look for a leading =X/postgres in the acl).
revoke all on public.billing_events from public, anon, authenticated;
revoke all on sequence public.billing_events_id_seq from public, anon, authenticated;

comment on table public.billing_events is
  'Append-only billing ledger normalised across Stripe and Apple. Written only by the '
  'payment edge functions with the service role; read only through admin_business(). '
  'Cash (amount_cents) and recurring value (mrr_cents, mrr_delta_cents) are separate '
  'columns on purpose. The log begins the day it was deployed and is never backfilled '
  'with estimates.';

-- One definition of monthly value, used by the log and by the snapshot, so the two cannot
-- drift. An annual price is twelfths; anything else is taken at face value.
create or replace function public.mrr_of(p_amount_cents bigint, p_interval text)
returns bigint language sql immutable as $$
  select case
    when p_amount_cents is null then 0
    when p_interval = 'year'  then round(p_amount_cents / 12.0)::bigint
    when p_interval = 'week'  then round(p_amount_cents * 52 / 12.0)::bigint
    when p_interval = 'day'   then round(p_amount_cents * 365 / 12.0)::bigint
    else p_amount_cents
  end;
$$;
revoke all on function public.mrr_of(bigint, text) from public, anon, authenticated;

-- ---------------------------------------------------------------------------
-- admin_business: one read for the whole business page.
--
-- Deliberately one RPC rather than six. The page shows a single moment, and six round
-- trips can disagree with each other: the tile says 11 paying and the chart says 12
-- because a webhook landed between them. One statement, one snapshot, one story.
-- ---------------------------------------------------------------------------
create or replace function public.admin_business(p_days integer default 90)
returns jsonb
language plpgsql
stable
security definer
set search_path to 'public'
as $function$
declare
  d    integer := greatest(1, least(coalesce(p_days, 90), 365));
  t0   timestamptz := date_trunc('day', now()) - make_interval(days => d - 1);
  res  jsonb;
begin
  if not is_admin() then raise exception 'admin only'; end if;

  select jsonb_build_object(
    'generated_at', now(),
    'days', d,
    'since', t0,

    -- How much of the window the log can actually speak for. The page prints this rather
    -- than assuming the log has always existed.
    'log', (select jsonb_build_object(
        'events', count(*),
        'first_at', min(occurred_at),
        'last_at',  max(occurred_at),
        'covers_window', coalesce(min(occurred_at) <= t0, false))
      from billing_events),

    -- The snapshot half: what is true right now, read off profiles exactly as the Revenue
    -- tab reads it, so the two pages can never show different MRR.
    'snapshot', (select jsonb_build_object(
        'mrr_cents', coalesce(sum(mrr_of(plan_amount_cents, plan_interval))
                       filter (where plan_status = 'active'), 0),
        'trial_mrr_cents', coalesce(sum(mrr_of(plan_amount_cents, plan_interval))
                       filter (where plan_status = 'trialing'), 0),
        'paying',     count(*) filter (where plan_status = 'active'),
        'trialing',   count(*) filter (where plan_status = 'trialing'),
        'past_due',   count(*) filter (where plan_status = 'past_due'),
        'cancelling', count(*) filter (where cancel_at_period_end
                                         and plan_status in ('active','trialing')),
        'accounts_total', count(*),
        'ever_subscribed', count(*) filter (where plan_status is not null))
      from profiles),

    -- The MRR bridge, per day. Every column is a sum of mrr_delta_cents over one kind, so
    -- new + expansion - contraction - churn is net by construction and cannot be off by a
    -- rounding rule applied in one place and not another.
    'movement', (select coalesce(jsonb_agg(jsonb_build_object(
          'd', g.day::date, 'new_cents', x.new_cents, 'expansion_cents', x.exp_cents,
          'contraction_cents', x.con_cents, 'churned_cents', x.churn_cents,
          'net_cents', x.new_cents + x.exp_cents - x.con_cents - x.churn_cents) order by g.day), '[]'::jsonb)
      from generate_series(t0::date, now()::date, interval '1 day') g(day)
      cross join lateral (
        select
          coalesce(sum(mrr_delta_cents) filter (where kind in ('subscription_started','trial_converted')), 0) as new_cents,
          coalesce(sum(mrr_delta_cents) filter (where kind = 'upgraded'), 0) as exp_cents,
          coalesce(-sum(mrr_delta_cents) filter (where kind = 'downgraded'), 0) as con_cents,
          coalesce(-sum(mrr_delta_cents) filter (where kind = 'canceled'), 0) as churn_cents
        from billing_events b where b.occurred_at::date = g.day::date) x),

    -- Cash, per day. Charges and refunds kept apart: netting them hides the month where a
    -- fifth of revenue came back.
    'cash', (select coalesce(jsonb_agg(jsonb_build_object(
          'd', g.day::date, 'charged_cents', x.charged, 'refunded_cents', x.refunded,
          'net_cents', x.charged - x.refunded, 'charges', x.n_charge, 'refunds', x.n_refund) order by g.day), '[]'::jsonb)
      from generate_series(t0::date, now()::date, interval '1 day') g(day)
      cross join lateral (
        select coalesce(sum(amount_cents) filter (where amount_cents > 0), 0) as charged,
               coalesce(-sum(amount_cents) filter (where amount_cents < 0), 0) as refunded,
               count(*) filter (where amount_cents > 0) as n_charge,
               count(*) filter (where kind = 'refunded') as n_refund
        from billing_events b where b.occurred_at::date = g.day::date) x),

    -- Window totals, the numbers that go on tiles.
    'window', (select jsonb_build_object(
        'new_mrr_cents',         coalesce(sum(mrr_delta_cents) filter (where kind in ('subscription_started','trial_converted')), 0),
        'expansion_mrr_cents',   coalesce(sum(mrr_delta_cents) filter (where kind = 'upgraded'), 0),
        'contraction_mrr_cents', coalesce(-sum(mrr_delta_cents) filter (where kind = 'downgraded'), 0),
        'churned_mrr_cents',     coalesce(-sum(mrr_delta_cents) filter (where kind = 'canceled'), 0),
        'charged_cents',         coalesce(sum(amount_cents) filter (where amount_cents > 0), 0),
        'refunded_cents',        coalesce(-sum(amount_cents) filter (where amount_cents < 0), 0),
        'refunds',               count(*) filter (where kind = 'refunded'),
        'failed_payments',       count(*) filter (where kind = 'payment_failed'),
        'trials_started',        count(*) filter (where kind = 'trial_started'),
        'trials_converted',      count(*) filter (where kind = 'trial_converted'),
        'subscriptions_started', count(*) filter (where kind = 'subscription_started'),
        'cancellations',         count(*) filter (where kind = 'canceled'),
        'renewals',              count(*) filter (where kind = 'renewed'))
      from billing_events where occurred_at >= t0),

    -- Trial cohorts by the week the trial STARTED, which is the only grouping that gives
    -- an honest conversion rate. Grouping conversions by the week they converted flatters
    -- a growing month and punishes a shrinking one.
    --
    -- A cohort that has not finished trialing yet is reported as pending rather than
    -- folded into the rate, and conv_pct is null until it is decided. A 0% that only means
    -- "not yet" is worse than a blank.
    'trial_cohorts', (select coalesce(jsonb_agg(jsonb_build_object(
          'w', w, 'started', started, 'converted', converted,
          'lapsed', lapsed, 'pending', started - converted - lapsed,
          'conv_pct', case when (converted + lapsed) > 0
                           then round(converted * 100.0 / (converted + lapsed), 1) end) order by w), '[]'::jsonb)
      from (
        select date_trunc('week', t.occurred_at)::date as w,
               count(*) as started,
               count(*) filter (where exists (select 1 from billing_events c
                 where c.subscription_id = t.subscription_id and c.source = t.source
                   and c.kind = 'trial_converted')) as converted,
               count(*) filter (where not exists (select 1 from billing_events c
                 where c.subscription_id = t.subscription_id and c.source = t.source
                   and c.kind = 'trial_converted')
                 and exists (select 1 from billing_events x
                 where x.subscription_id = t.subscription_id and x.source = t.source
                   and x.kind = 'canceled')) as lapsed
        from billing_events t
        where t.kind = 'trial_started' and t.occurred_at >= t0 and t.subscription_id is not null
        group by 1) c),

    -- Who cancelled and what it cost, most recent first. A churn number without the rows
    -- behind it is a number nobody can act on.
    'recent_churn', (select coalesce(jsonb_agg(jsonb_build_object(
          'at', occurred_at, 'plan', plan, 'interval', plan_interval,
          'mrr_cents', mrr_cents, 'source', source) order by occurred_at desc), '[]'::jsonb)
      from (select * from billing_events where kind = 'canceled' and occurred_at >= t0
            order by occurred_at desc limit 25) z),

    -- Money that came back out, with the same treatment.
    'recent_refunds', (select coalesce(jsonb_agg(jsonb_build_object(
          'at', occurred_at, 'cents', -amount_cents, 'plan', plan, 'source', source) order by occurred_at desc), '[]'::jsonb)
      from (select * from billing_events where kind = 'refunded' and occurred_at >= t0
            order by occurred_at desc limit 25) z),

    -- Where the money comes from. Two processors now, and the split is the thing that
    -- decides whether Apple's cut is worth arguing about.
    'by_source', (select coalesce(jsonb_object_agg(source, n), '{}'::jsonb)
      from (select source, count(*) as n from billing_events
            where occurred_at >= t0 group by 1) s)
  ) into res;

  return res;
end;
$function$;

revoke all on function public.admin_business(integer) from public, anon, authenticated;
grant execute on function public.admin_business(integer) to authenticated;
