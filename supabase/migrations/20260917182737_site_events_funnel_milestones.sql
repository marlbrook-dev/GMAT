-- The funnel is measurable up to the moment somebody opens a trainer and no further.
-- Last month: 188 consented sessions, 17 of which opened a trainer, and nothing at all
-- about whether any of those 17 answered a question. item_events records the answering
-- but carries no session, device or user by design, so it cannot be joined to a visit,
-- and that stays true: this adds the step to site_events instead, which already holds a
-- session id under consent and is already disclosed.
--
-- No new personal data. A milestone row carries the same sid and path a pageview row
-- already carries, plus the name of the step reached.
alter table public.site_events
  add column if not exists step text;

comment on column public.site_events.step is
  'Funnel milestone reached, set only on kind=''milestone'' rows. One of app_open, '
  'first_answer, round_done, account_created, trial_started. Consent gated exactly as '
  'every other site_events row is.';

-- Keep the write surface as narrow as it was: anon may insert, nobody may select.
-- Constrain the vocabulary so a typo in the client cannot quietly create a new step
-- that the funnel view then fails to count.
alter table public.site_events
  drop constraint if exists site_events_step_vocab;
alter table public.site_events
  add constraint site_events_step_vocab check (
    step is null or step in
      ('app_open','first_answer','round_done','account_created','trial_started')
  );

create index if not exists site_events_step_idx
  on public.site_events (step, ts desc) where step is not null;
