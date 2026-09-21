-- The funnel, readable. Sessions are the denominator rather than pageviews, because
-- "how many people got this far" is the question; a session that reloads the trainer
-- four times is still one person who opened it.
create or replace function public.admin_funnel(days int default 30)
returns table (
  step text,
  label text,
  sessions bigint,
  share_of_visits numeric,
  share_of_previous numeric
)
language plpgsql
security definer
set search_path = public
as $$
declare
  win interval := make_interval(days => greatest(1, least(coalesce(days, 30), 400)));
  total bigint;
begin
  if not public.is_admin() then
    raise exception 'admin only';
  end if;

  select count(distinct sid) into total
  from site_events where ts > now() - win;

  return query
  with reached as (
    select s.step, count(distinct s.sid) as n
    from site_events s
    where s.ts > now() - win and s.step is not null
    group by s.step
  ),
  steps(step, label, ord) as (
    values
      ('app_open',        'Opened a trainer',        1),
      ('first_answer',    'Answered a question',     2),
      ('round_done',      'Finished a round',        3),
      ('account_created', 'Asked for a sign-in link',4),
      ('trial_started',   'Opened checkout',         5)
  ),
  rows as (
    select st.step, st.label, st.ord, coalesce(r.n, 0) as n
    from steps st left join reached r on r.step = st.step
  )
  select x.step, x.label, x.n,
         case when total > 0 then round(100.0 * x.n / total, 1) end,
         case when lag(x.n) over (order by x.ord) > 0
              then round(100.0 * x.n / lag(x.n) over (order by x.ord), 1) end
  from rows x order by x.ord;
end;
$$;

revoke all on function public.admin_funnel(int) from public, anon, authenticated;
grant execute on function public.admin_funnel(int) to authenticated;
