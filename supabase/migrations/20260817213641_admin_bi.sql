-- Admin allowlist + BI aggregates. The dashboard reads ONLY via admin_bi();
-- raw tables keep per-user RLS. Admins are emails in app_admins.
create table if not exists app_admins (email text primary key, added_at timestamptz default now());
alter table app_admins enable row level security;
insert into app_admins(email) values ('hroberts@winthropcapital.com') on conflict do nothing;

create or replace function is_admin() returns boolean
language sql stable security definer set search_path = public as $$
  select exists(select 1 from app_admins where lower(email) = lower(coalesce(auth.jwt()->>'email','')));
$$;
revoke all on function is_admin() from public;
grant execute on function is_admin() to authenticated, anon;

drop policy if exists "admins read admin list" on app_admins;
create policy "admins read admin list" on app_admins for select using (is_admin());

create or replace function admin_bi() returns jsonb
language plpgsql stable security definer set search_path = public as $$
declare result jsonb;
begin
  if not is_admin() then raise exception 'admin only'; end if;
  select jsonb_build_object(
    'generated_at', now(),
    'users_total', (select count(*) from profiles),
    'users_new_7d', (select count(*) from profiles where created_at > now() - interval '7 days'),
    'users_active_7d', (select count(distinct user_id) from events where ts > now() - interval '7 days' and user_id is not null),
    'users_paid', (select count(*) from profiles where plan is distinct from 'free'),
    'plan_mix', (select coalesce(jsonb_object_agg(plan, n), '{}'::jsonb) from (select coalesce(plan,'free') as plan, count(*) as n from profiles group by 1) t),
    'attempts_total', (select count(*) from attempts),
    'attempts_7d', (select count(*) from attempts where ts > now() - interval '7 days'),
    'accuracy_7d', (select round(avg(case when correct then 1.0 else 0 end), 3) from attempts where ts > now() - interval '7 days'),
    'signups_by_day', (select coalesce(jsonb_agg(jsonb_build_object('d', d, 'n', n) order by d), '[]'::jsonb) from (select date_trunc('day', created_at)::date as d, count(*) as n from profiles where created_at > now() - interval '30 days' group by 1) t),
    'attempts_by_day', (select coalesce(jsonb_agg(jsonb_build_object('d', d, 'n', n, 'u', u) order by d), '[]'::jsonb) from (select date_trunc('day', ts)::date as d, count(*) as n, count(distinct user_id) as u from attempts where ts > now() - interval '30 days' group by 1) t),
    'sessions_by_mode_30d', (select coalesce(jsonb_object_agg(mode, n), '{}'::jsonb) from (select coalesce(mode,'unknown') as mode, count(*) as n from sessions where ts > now() - interval '30 days' group by 1) t),
    'events_by_name_7d', (select coalesce(jsonb_object_agg(name, n), '{}'::jsonb) from (select name, count(*) as n from events where ts > now() - interval '7 days' group by 1) t),
    'skill_difficulty', (select coalesce(jsonb_agg(jsonb_build_object('skill', skill, 'n', n, 'acc', acc) order by acc), '[]'::jsonb) from (select skill, count(*) as n, round(avg(case when correct then 1.0 else 0 end),3) as acc from attempts group by skill having count(*) >= 10) t),
    'item_flags', (select coalesce(jsonb_agg(jsonb_build_object('qid', qid, 'n', n, 'acc', acc, 'med_secs', med) order by acc), '[]'::jsonb) from (
        select qid, count(*) as n, round(avg(case when correct then 1.0 else 0 end),3) as acc,
               round((percentile_cont(0.5) within group (order by secs))::numeric,1) as med
        from attempts group by qid
        having count(*) >= 8 and (avg(case when correct then 1.0 else 0 end) < 0.25 or avg(case when correct then 1.0 else 0 end) > 0.95)
        limit 40) t)
  ) into result;
  return result;
end $$;
revoke all on function admin_bi() from public;
grant execute on function admin_bi() to authenticated;
