-- PROPOSED, NOT APPLIED. Needs the owner's go-ahead before it touches project ftsqwbzhkzuudogkvoqa.
--
-- Why: profiles.state_blob predates multi-exam. It holds one state per user, while attempts,
-- skill_ratings and review_queue are all keyed by (user_id, exam). With the SAT trainer live, a
-- signed-in student who practices both exams would have whichever app saved last overwrite the
-- other exam's progress.
--
-- The app currently refuses to write over a blob belonging to another exam, which protects the
-- data but leaves cross-device sync unavailable for the second exam a student picks up. The
-- Account page says so in those words rather than failing quietly.
--
-- This migration is additive: it creates the per-exam table, copies each existing blob into the
-- exam its own record names, and leaves profiles.state_blob in place so nothing that still reads
-- it breaks. Dropping the old column would be a separate change, after the app has been reading
-- from the new table for a while.

create table if not exists exam_states (
  user_id uuid not null references auth.users(id) on delete cascade,
  exam text not null default 'gmat-focus',
  state_blob jsonb,
  updated_at timestamptz default now(),
  primary key (user_id, exam)
);

alter table exam_states enable row level security;

-- Same shape as the existing per-user policies: a user reads and writes only their own rows.
drop policy if exists exam_states_select_own on exam_states;
create policy exam_states_select_own on exam_states
  for select using (auth.uid() = user_id);

drop policy if exists exam_states_insert_own on exam_states;
create policy exam_states_insert_own on exam_states
  for insert with check (auth.uid() = user_id);

drop policy if exists exam_states_update_own on exam_states;
create policy exam_states_update_own on exam_states
  for update using (auth.uid() = user_id) with check (auth.uid() = user_id);

drop policy if exists exam_states_delete_own on exam_states;
create policy exam_states_delete_own on exam_states
  for delete using (auth.uid() = user_id);

-- Backfill: each existing blob goes to the exam it names, defaulting to the GMAT for blobs
-- written before the registry existed.
insert into exam_states (user_id, exam, state_blob, updated_at)
select p.id,
       coalesce(p.state_blob ->> 'exam', 'gmat-focus'),
       p.state_blob,
       now()
from profiles p
where p.state_blob is not null
on conflict (user_id, exam) do nothing;

-- After applying, the app changes are:
--   Cloud.pull:  select state_blob from exam_states where user_id = ... and exam = CURRENT_EXAM
--   Cloud.push:  upsert into exam_states on (user_id, exam)
--   Cloud.wipe:  also delete from exam_states where user_id = ...
-- and the blobLocked guard in src/app_template.html can be removed, along with this note.
