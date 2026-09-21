-- Postgres fires same-timing triggers in alphabetical order by name, and the two on
-- profiles were named without anybody deciding an order, so they got one anyway:
-- profiles_sharing_eligibility sorted before profiles_sync_age_tier.
--
-- That is backwards. Eligibility was judged against the age_tier already in the row,
-- before sync_age_tier had recomputed it from the birth month and year in the same
-- statement. So an adult who set their birth date and opted in together had the opt-in
-- revoked by the trigger meant to protect minors, silently, and an adult correcting
-- their year upward past 18 stayed ineligible. Every exclusion still held, which is why
-- it looked fine: the failure was in the direction of sharing nothing, not of sharing
-- what it should not.
--
-- The numbers are in the names deliberately. The order is load-bearing, so it should be
-- readable in \d profiles rather than deduced from the alphabet.
alter trigger profiles_sync_age_tier on public.profiles
  rename to profiles_trg_1_sync_age_tier;
alter trigger profiles_sharing_eligibility on public.profiles
  rename to profiles_trg_2_sharing_eligibility;

comment on function public.sync_age_tier() is
  'Derives age_tier from birth_year and birth_month. Runs as profiles_trg_1_sync_age_tier '
  'so that the eligibility trigger downstream sees the tier this statement establishes '
  'rather than the one it replaces. The numeric prefix is what orders them.';

comment on function public.enforce_sharing_eligibility() is
  'Revokes data_sharing_opt_in when age_tier is not 18_plus. Runs as '
  'profiles_trg_2_sharing_eligibility, after the tier has been synced.';
