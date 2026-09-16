-- MRR needs to know what each subscriber actually pays. plan holds the tier (plus/pro) but
-- not whether they are on the monthly or the annual price, so revenue could only ever be
-- guessed from a headcount times a hardcoded rate. These two columns come straight off the
-- Stripe subscription item, so the number is the real one.
--
-- Service-role only, like every other billing column: they are absent from the column
-- grants in 20260916_harden_plan_column_and_rpc_surface.sql, so no browser session can
-- write them.
alter table public.profiles
  add column if not exists plan_interval     text,     -- 'month' | 'year', from price.recurring.interval
  add column if not exists plan_amount_cents integer;  -- price.unit_amount, in the price's currency

comment on column public.profiles.plan_amount_cents is
  'Stripe price.unit_amount for the active subscription. Divide by 12 for annual when computing MRR.';

-- Revenue and subscription health. Aggregates only, no row ever leaves this function, and
-- it refuses anyone who is not an admin, exactly like the other admin_* RPCs.
create or replace function public.admin_revenue()
returns jsonb
language plpgsql
stable
security definer
set search_path to 'public'
as $function$
declare result jsonb;
begin
  if not is_admin() then raise exception 'admin only'; end if;
  select jsonb_build_object(
    'generated_at', now(),

    -- Where every account currently stands. plan_status is null for anyone who has never
    -- subscribed, which is most accounts, so it is folded into 'never'.
    'status_mix', (select coalesce(jsonb_object_agg(st, n), '{}'::jsonb)
      from (select coalesce(plan_status, 'never') as st, count(*) as n from profiles group by 1) t),

    -- Money actually committed today: annual normalised to a monthly figure.
    'mrr_cents', (select coalesce(sum(case when plan_interval = 'year'
                                           then plan_amount_cents / 12.0
                                           else plan_amount_cents end), 0)::bigint
      from profiles where plan_status = 'active' and plan_amount_cents is not null),

    -- What converts if nobody in a trial cancels. Kept separate from MRR on purpose:
    -- counting trials as revenue is how a dashboard starts lying to its owner.
    'trial_mrr_cents', (select coalesce(sum(case when plan_interval = 'year'
                                                 then plan_amount_cents / 12.0
                                                 else plan_amount_cents end), 0)::bigint
      from profiles where plan_status = 'trialing' and plan_amount_cents is not null),

    'paying', (select count(*) from profiles where plan_status = 'active'),
    'trialing', (select count(*) from profiles where plan_status = 'trialing'),
    'past_due', (select count(*) from profiles where plan_status = 'past_due'),

    -- Already asked to leave but still inside the paid period. These are the accounts a
    -- human could still win back, which is the whole reason to surface them.
    'cancelling', (select count(*) from profiles
      where cancel_at_period_end and plan_status in ('active','trialing')),

    'plan_mix', (select coalesce(jsonb_object_agg(k, n), '{}'::jsonb)
      from (select coalesce(plan,'free') || ' ' || coalesce(plan_interval,'-') as k, count(*) as n
            from profiles where plan_status in ('active','trialing') group by 1) t),

    -- The next two weeks of money, by day: trials about to convert and renewals about to
    -- charge. This is the one view that tells you what is about to happen rather than what
    -- already did.
    'trials_ending', (select coalesce(jsonb_agg(jsonb_build_object(
          'd', d, 'n', n, 'cents', cents, 'cancelling', cancelling) order by d), '[]'::jsonb)
      from (select trial_end::date as d, count(*) as n,
                   coalesce(sum(plan_amount_cents),0)::bigint as cents,
                   count(*) filter (where cancel_at_period_end) as cancelling
            from profiles
            where plan_status = 'trialing' and trial_end between now() and now() + interval '14 days'
            group by 1) t),

    'renewals_due', (select coalesce(jsonb_agg(jsonb_build_object(
          'd', d, 'n', n, 'cents', cents, 'cancelling', cancelling) order by d), '[]'::jsonb)
      from (select current_period_end::date as d, count(*) as n,
                   coalesce(sum(plan_amount_cents),0)::bigint as cents,
                   count(*) filter (where cancel_at_period_end) as cancelling
            from profiles
            where plan_status = 'active' and current_period_end between now() and now() + interval '14 days'
            group by 1) t),

    -- Free to paid, on current state. Honest about what it is: a snapshot ratio, not a
    -- cohort conversion rate, because nothing records when a trial started yet.
    'accounts_total', (select count(*) from profiles),
    'ever_subscribed', (select count(*) from profiles where plan_status is not null)
  ) into result;
  return result;
end;
$function$;

revoke execute on function public.admin_revenue() from public;
grant  execute on function public.admin_revenue() to authenticated;
