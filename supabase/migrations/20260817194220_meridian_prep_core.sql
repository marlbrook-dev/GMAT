create table if not exists profiles (
  id uuid primary key references auth.users(id) on delete cascade,
  display_name text, email text, test_date date, daily_goal int default 20, exam text default 'gmat-focus',
  plan text default 'free', state_blob jsonb, consent_at timestamptz, created_at timestamptz default now(), updated_at timestamptz default now()
);
create table if not exists attempts (
  id bigserial primary key, user_id uuid not null references auth.users(id) on delete cascade,
  exam text not null default 'gmat-focus', qid text not null, skill text not null, section text not null, diff int,
  correct boolean not null, secs int, flag text, reason text, guessed boolean default false, chosen jsonb, session_id text,
  ts timestamptz default now()
);
create index if not exists attempts_user_ts on attempts(user_id, ts desc);
create index if not exists attempts_qid on attempts(qid);
create table if not exists events (
  id bigserial primary key, user_id uuid references auth.users(id) on delete cascade,
  name text not null, exam text, props jsonb, platform text, app_version text, ts timestamptz default now()
);
create index if not exists events_user_ts on events(user_id, ts desc);
create index if not exists events_name_ts on events(name, ts desc);
create table if not exists sessions (
  id text primary key, user_id uuid references auth.users(id) on delete cascade, mode text, n int, c int, avg_secs int, ts timestamptz default now()
);
alter table profiles enable row level security; alter table attempts enable row level security; alter table events enable row level security; alter table sessions enable row level security;
create policy "own profile" on profiles for all using (auth.uid() = id) with check (auth.uid() = id);
create policy "own attempts" on attempts for all using (auth.uid() = user_id) with check (auth.uid() = user_id);
create policy "own events" on events for all using (auth.uid() = user_id) with check (auth.uid() = user_id);
create policy "own sessions" on sessions for all using (auth.uid() = user_id) with check (auth.uid() = user_id);
-- auto-create profile row on signup
create or replace function public.handle_new_user() returns trigger language plpgsql security definer set search_path = public as $$
begin insert into public.profiles (id, email) values (new.id, new.email) on conflict (id) do nothing; return new; end; $$;
drop trigger if exists on_auth_user_created on auth.users;
create trigger on_auth_user_created after insert on auth.users for each row execute procedure public.handle_new_user();
-- item-level analytics for content review (owner view later): per-question correct rate and median time
create or replace view item_stats as
select qid, count(*) as n, avg(case when correct then 1 else 0 end)::numeric(4,3) as p_correct, percentile_cont(0.5) within group (order by secs) as median_secs
from attempts group by qid;
