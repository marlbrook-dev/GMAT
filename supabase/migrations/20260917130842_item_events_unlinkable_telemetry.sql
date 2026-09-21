-- Item telemetry that is deliberately not personal data.
--
-- The adaptive engine needs to know how each item behaves: how often it is answered
-- correctly, how long it takes, and which wrong answer pulls. Today it learns none of
-- that, because attempts only sync for signed in users and the product's whole pitch
-- is that no account is needed. attempts holds zero rows.
--
-- The fix is a table with no user_id, no session id, no device id and no IP hash.
-- A row says "item GQ014 was answered, choice 2 was picked, it was wrong, it took 74
-- seconds". Nothing in it identifies or singles out a person, which is what makes it
-- lawful to collect from everyone without a consent gate, and it is the entire signal
-- the engine wants. Personal analytics stay in site_events, behind consent.
--
-- The cost of dropping the IP hash is that rows cannot be rate limited per device.
-- That is accepted deliberately: this data feeds PROPOSALS a human reviews, never an
-- automatic change to the bank or the engine, so poisoning it misleads a reviewer at
-- worst rather than silently retuning the product.

create table if not exists public.item_events (
  id          bigserial primary key,
  ts          timestamptz not null default now(),
  exam        text        not null,
  qid         text        not null,
  skill       text,
  section     text,
  diff        smallint,
  chosen      smallint,               -- index of the option picked; null for non multiple choice
  correct     boolean     not null,
  secs        integer,
  mode        text,                   -- practice, drill, game, mock
  constraint item_events_secs_sane   check (secs is null or (secs >= 0 and secs <= 3600)),
  constraint item_events_chosen_sane check (chosen is null or (chosen >= 0 and chosen <= 9)),
  constraint item_events_diff_sane   check (diff is null or (diff >= 1 and diff <= 5))
);

comment on table public.item_events is
  'Unlinkable per item telemetry. No user, session, device or IP column exists by design, so a row cannot be tied to a person. Feeds item difficulty and distractor analysis as proposals for human review. Personal analytics live in site_events behind consent.';

create index if not exists item_events_qid_ts_idx on public.item_events (qid, ts desc);
create index if not exists item_events_exam_ts_idx on public.item_events (exam, ts desc);

alter table public.item_events enable row level security;

-- Insert only, for anyone. There is no select policy, so no client can read it back;
-- admins read through the is_admin gated RPC below.
drop policy if exists item_events_insert on public.item_events;
create policy item_events_insert on public.item_events for insert to anon, authenticated with check (true);

revoke all on public.item_events from public, anon, authenticated;
grant insert on public.item_events to anon, authenticated;
grant usage, select on sequence public.item_events_id_seq to anon, authenticated;
