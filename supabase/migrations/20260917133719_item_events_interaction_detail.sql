-- Interaction detail for each answered item. Still no user, session, device or address
-- column, and none is added here: the whole reason this table needs no consent gate is
-- that a row cannot be joined to a person or to another row from the same person.
--
-- first_ms  milliseconds from the item rendering to the first option being picked, which
--           separates "knew it" from "worked it out" in a way total time cannot.
-- changes   how many times the chosen option was switched before submitting. A high mean
--           on one item is the signature of two defensible answers.
-- guessed   the learner's own admission that a correct answer was not confident.
-- reason    the learner's own tag for why a miss happened, from the fixed list the app
--           offers. Self-reported about the question, not about the person.
alter table public.item_events
  add column if not exists first_ms integer,
  add column if not exists changes  smallint,
  add column if not exists guessed  boolean,
  add column if not exists reason   text;

-- Bound what the browser can write. An open integer column on an insert-only, world
-- writable table is an invitation to store something else in it.
alter table public.item_events
  drop constraint if exists item_events_first_ms_ck,
  drop constraint if exists item_events_changes_ck,
  drop constraint if exists item_events_reason_ck;
alter table public.item_events
  add constraint item_events_first_ms_ck check (first_ms is null or (first_ms >= 0 and first_ms <= 3600000)),
  add constraint item_events_changes_ck  check (changes  is null or (changes  >= 0 and changes  <= 50)),
  add constraint item_events_reason_ck   check (reason   is null or char_length(reason) <= 40);
