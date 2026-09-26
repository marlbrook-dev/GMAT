-- UPDATE OF <columns> fires on the columns NAMED IN THE STATEMENT, not on the columns
-- that actually changed, and not on what an earlier BEFORE trigger wrote into NEW. So
-- "update profiles set birth_year = 2011" ran sync_age_tier, which set NEW.age_tier to
-- '13_17' in memory, and then skipped the eligibility trigger entirely, because the
-- statement never named age_tier. The row was stored with a minor's tier and the opt-in
-- still true.
--
-- sellable_profiles filters on age_tier so nothing was exportable either way, which is
-- why this survived the first pass. It was still wrong twice over: the Account page reads
-- the flag, so it would have told a 14 year old their profile was being shared, and the
-- privacy policy now says in as many words that the revoke happens at the database level
-- rather than by anybody remembering. A policy sentence is a promise, and this one was
-- not being kept.
--
-- The column list was a micro-optimisation on a table written a few times per session.
-- Dropping it costs one enum comparison per update and makes the guarantee unconditional.
drop trigger if exists profiles_trg_2_sharing_eligibility on public.profiles;

create trigger profiles_trg_2_sharing_eligibility
  before insert or update on public.profiles
  for each row execute function public.enforce_sharing_eligibility();

-- Revocation is one way on purpose. An age corrected downward revokes; correcting it
-- back up does not silently re-enable sharing, because the consent that was withdrawn
-- was withdrawn, and re-granting it is an act the person takes, not one a birth year
-- takes for them.
comment on trigger profiles_trg_2_sharing_eligibility on public.profiles is
  'Revokes data_sharing_opt_in whenever the stored age_tier is not 18_plus. Fires on '
  'every insert and update rather than a column list, because UPDATE OF keys off the '
  'columns named in the statement and would miss a tier changed by the sync trigger.';
