-- Meridian Prep: Phase 3 schema (Supabase Postgres). Apply via Supabase MCP apply_migration or SQL editor.
create table if not exists profiles (
  id uuid primary key references auth.users(id) on delete cascade,
  display_name text, test_date date, daily_goal int default 20, exam text default 'gmat-focus',
  plan text default 'free', created_at timestamptz default now()
);
create table if not exists attempts (
  id bigserial primary key, user_id uuid not null references auth.users(id) on delete cascade,
  exam text not null default 'gmat-focus', qid text not null, skill text not null, section text not null, diff int,
  correct boolean not null, secs int, flag text, reason text, guessed boolean default false, chosen jsonb, session_id text,
  ts timestamptz default now()
);
create index if not exists attempts_user_ts on attempts(user_id, ts desc);
create table if not exists skill_ratings (
  user_id uuid references auth.users(id) on delete cascade, exam text default 'gmat-focus', skill text,
  r int default 1000, n int default 0, c int default 0, t int default 0, hist jsonb default '[]',
  updated_at timestamptz default now(), primary key (user_id, exam, skill)
);
create table if not exists review_queue (
  user_id uuid references auth.users(id) on delete cascade, exam text default 'gmat-focus', qid text,
  interval_days int default 1, due timestamptz, lapses int default 0, primary key (user_id, exam, qid)
);
create table if not exists card_states (
  user_id uuid references auth.users(id) on delete cascade, card_id text, box int default 0, due timestamptz,
  seen int default 0, known int default 0, primary key (user_id, card_id)
);
create table if not exists sessions (
  id text primary key, user_id uuid references auth.users(id) on delete cascade, mode text, n int, c int, avg_secs int, ts timestamptz default now()
);
-- Row Level Security: each user sees only their own rows
alter table profiles enable row level security; alter table attempts enable row level security; alter table skill_ratings enable row level security;
alter table review_queue enable row level security; alter table card_states enable row level security; alter table sessions enable row level security;
create policy "own profile" on profiles for all using (auth.uid() = id) with check (auth.uid() = id);
create policy "own attempts" on attempts for all using (auth.uid() = user_id) with check (auth.uid() = user_id);
create policy "own ratings" on skill_ratings for all using (auth.uid() = user_id) with check (auth.uid() = user_id);
create policy "own review" on review_queue for all using (auth.uid() = user_id) with check (auth.uid() = user_id);
create policy "own cards" on card_states for all using (auth.uid() = user_id) with check (auth.uid() = user_id);
create policy "own sessions" on sessions for all using (auth.uid() = user_id) with check (auth.uid() = user_id);

-- Applied migration admin_bi: app_admins allowlist, is_admin(), admin_bi() aggregates RPC
-- (dashboard reads only via RPC; raw tables keep per-user RLS). See Supabase migration history.
-- Applied migration partner_crm: crm_contacts + crm_notes, admin-only RLS via is_admin().
