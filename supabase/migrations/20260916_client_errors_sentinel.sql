-- Sentinel, stage one: see the bugs.
--
-- Today a JavaScript error on a live page is invisible. Nobody finds out until a student
-- gives up and leaves, and nothing records that they did. Everything downstream of this
-- (identify the source, propose a fix, learn which signals matter) needs the signal to
-- exist first, so this is the foundation rather than the whole loop.
--
-- Grounding, from the two DevSecOps papers:
--   C2 Model Explainability / R2 evidence-based XAI: every cluster carries the raw
--      evidence (stack, build, pages, session counts) so a human can judge it. Nothing in
--      this design acts on its own; Winter et al. found trust in automated repair is the
--      crucial problem, and a live payment site is the wrong place to test that.
--   C14 Normality Drift / R14 (Han et al., OWAD: detect, explain, adapt): what counts as a
--      normal error rate changes every time we ship. Thresholds are therefore computed on
--      a rolling window rather than frozen, and triage decisions are stored as labels so
--      the baseline can be re-derived instead of hand-tuned.
--   Cid-Fuentes et al.: a detector that depends on historical failure data cannot adapt at
--      runtime, so this models current runtime behaviour, not a trained failure corpus.
--   Le and Zhang (NeuralLog): log parsing is itself a source of error, so the raw message
--      is stored verbatim and normalisation happens in a separate, inspectable column.

create table if not exists public.client_errors (
  id           bigserial primary key,
  ts           timestamptz not null default now(),
  -- What happened. Raw and untouched, so a parsing bug here cannot destroy the evidence.
  message      text not null,
  source       text,
  lineno       integer,
  colno        integer,
  stack        text,
  kind         text not null default 'error',   -- error | unhandledrejection | console
  -- Where and when. app_version is what pins a regression to the build that caused it.
  path         text,
  app_version  text,
  exam         text,
  device       text,
  ua           text,
  sid          text,
  -- Stable grouping key computed on the client and re-derivable on the server.
  signature    text not null,
  -- Same privacy posture as site_events: country and a salted hash, never a raw IP.
  country      text,
  ip_hash      text
);

create index if not exists client_errors_ts_idx        on public.client_errors (ts desc);
create index if not exists client_errors_signature_idx on public.client_errors (signature, ts desc);

alter table public.client_errors enable row level security;

-- Insert is open, exactly like site_events: an error beacon that requires a session cannot
-- report the errors that break sessions. There is deliberately no select policy, so the
-- rows are write-only from the browser and readable only through the is_admin gated RPC.
drop policy if exists client_errors_insert on public.client_errors;
create policy client_errors_insert on public.client_errors
  for insert to anon, authenticated with check (true);

-- Server-side stamping. The browser never sends an IP and cannot set country or ip_hash;
-- the same trigger pattern site_events uses.
create or replace function public.client_errors_before()
returns trigger
language plpgsql
security definer
set search_path to 'public'
as $function$
begin
  new.country := nullif(req_header('cf-ipcountry'), '');
  new.ip_hash := req_ip_hash();
  new.ts      := now();
  -- Caps, so a runaway loop cannot fill the table with one enormous stack.
  new.message := left(coalesce(new.message, ''), 500);
  new.stack   := left(new.stack, 2000);
  new.source  := left(new.source, 300);
  new.path    := left(new.path, 200);
  new.ua      := left(new.ua, 300);
  new.signature := left(coalesce(nullif(new.signature,''), 'unknown'), 200);
  return new;
end;
$function$;
revoke execute on function public.client_errors_before() from public;

drop trigger if exists client_errors_before_ins on public.client_errors;
create trigger client_errors_before_ins before insert on public.client_errors
  for each row execute function public.client_errors_before();

-- Triage decisions. This table is the part that makes the loop improve: every human
-- judgement about a signature is kept, so the system can stop showing what was called
-- noise and can weight what was called real. It is the labelled feedback that Du et al.
-- use for post-deployment adjustment, just held by a human rather than a model for now.
create table if not exists public.error_triage (
  signature   text primary key,
  status      text not null default 'open',   -- open | real | noise | fixed | wontfix
  severity    text,                           -- low | medium | high
  note        text,
  fixed_in    text,                           -- app_version the fix shipped in
  decided_by  text,
  decided_at  timestamptz,
  updated_at  timestamptz not null default now()
);
alter table public.error_triage enable row level security;
-- No policy at all: RLS default-denies, so only service_role and the admin RPCs touch it.

-- Clusters with their evidence attached, newest activity first. Aggregates plus a single
-- example stack per cluster, which is what a human actually needs to judge one.
create or replace function public.admin_errors(p_days integer default 7)
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
    'window_days', coalesce(p_days, 7),
    'total', (select count(*) from client_errors where ts > now() - make_interval(days => coalesce(p_days,7))),
    'clusters', (select coalesce(jsonb_agg(to_jsonb(c) order by c.n desc), '[]'::jsonb) from (
        select e.signature,
               count(*)                       as n,
               count(distinct e.sid)          as sessions,
               min(e.ts)                      as first_seen,
               max(e.ts)                      as last_seen,
               (array_agg(e.message order by e.ts desc))[1]     as message,
               (array_agg(e.stack   order by e.ts desc))[1]     as stack,
               (array_agg(e.source  order by e.ts desc))[1]     as source,
               array_agg(distinct e.path)                        as paths,
               array_agg(distinct e.app_version)                 as versions,
               array_agg(distinct e.device)                      as devices,
               coalesce(t.status, 'open')                        as status,
               t.severity, t.note, t.fixed_in
        from client_errors e
        left join error_triage t on t.signature = e.signature
        where e.ts > now() - make_interval(days => coalesce(p_days,7))
          -- Anything a human already called noise stays out of the way. This is the
          -- system getting quieter as it learns, rather than louder.
          and coalesce(t.status,'open') <> 'noise'
        group by e.signature, t.status, t.severity, t.note, t.fixed_in) c),
    'muted', (select count(*) from error_triage where status = 'noise'),
    -- Rolling baseline rather than a fixed threshold: "normal" moves every time we ship,
    -- which is the normality drift problem (C14). Comparing the window against the
    -- preceding one of equal length is the cheapest honest version of that.
    'errors_this_window', (select count(*) from client_errors
        where ts > now() - make_interval(days => coalesce(p_days,7))),
    'errors_prev_window', (select count(*) from client_errors
        where ts > now() - make_interval(days => coalesce(p_days,7) * 2)
          and ts <= now() - make_interval(days => coalesce(p_days,7)))
  ) into result;
  return result;
end;
$function$;
revoke execute on function public.admin_errors(integer) from public;
grant  execute on function public.admin_errors(integer) to authenticated;

-- Record a triage decision. Upsert so a signature can be re-judged as understanding grows.
create or replace function public.admin_triage_error(
  p_signature text, p_status text, p_severity text default null,
  p_note text default null, p_fixed_in text default null)
returns jsonb
language plpgsql
security definer
set search_path to 'public'
as $function$
begin
  if not is_admin() then raise exception 'admin only'; end if;
  if p_status not in ('open','real','noise','fixed','wontfix') then
    raise exception 'bad status';
  end if;
  insert into error_triage (signature, status, severity, note, fixed_in, decided_by, decided_at, updated_at)
  values (left(p_signature,200), p_status, p_severity, left(p_note,1000), p_fixed_in,
          auth.jwt() ->> 'email', now(), now())
  on conflict (signature) do update
    set status = excluded.status, severity = excluded.severity, note = excluded.note,
        fixed_in = excluded.fixed_in, decided_by = excluded.decided_by,
        decided_at = now(), updated_at = now();
  return jsonb_build_object('ok', true, 'signature', p_signature, 'status', p_status);
end;
$function$;
revoke execute on function public.admin_triage_error(text, text, text, text, text) from public;
grant  execute on function public.admin_triage_error(text, text, text, text, text) to authenticated;
