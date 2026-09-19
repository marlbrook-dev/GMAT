-- INCOMPLETE ON PURPOSE, AND THE GAP IS NAMED HERE RATHER THAN LEFT TO BE DISCOVERED.
--
-- Three earlier migrations were applied straight to the project on 2026-09-18 and are
-- NOT mirrored in this directory, so a rebuild from these files alone will fail:
--
--   age_gate_and_data_sharing_consent      the age_tier enum, the data_sharing_* columns
--                                          on profiles, data_sharing_events,
--                                          data_sharing_policy, enforce_sharing_eligibility
--   birth_month_year_second_layer          birth_year, birth_month, age_from_birth,
--                                          tier_from_birth, sync_age_tier
--   data_sharing_export_and_profile_fields the twelve profile columns, sellable_profiles,
--                                          admin_sharing_cohort
--
-- They exist in the live project and in its migration history; reconstructing them here
-- is outstanding work.
--
-- Applied 2026-09-18 and 2026-09-19. Mirrored here so the schema is reproducible from
-- source rather than only from the live project.
--
-- The age-gated data sharing programme, plus the buy-and-append half added a day later.
-- Read src/sql/smoke_sharing.sql alongside this: it is the test that found the two
-- trigger bugs the comments below describe, and it will find them again if either
-- regresses.

-- ---------------------------------------------------------------------------------
-- 1. The opt-out control the CCPA link needs, and the first policy version.
-- ---------------------------------------------------------------------------------
-- An RPC rather than a PATCH on profiles, for two reasons that are one reason. The audit
-- row is not optional: "did I agree to this" has to be answerable from a record, and a
-- client that can write the flag directly can write it without the record. And
-- eligibility is a server question: the caller does not get to assert that they are 18.

create or replace function public.set_data_sharing(p_opt_in boolean, p_source text default 'account')
returns table (opt_in boolean, tier public.age_tier, policy_version text, changed_at timestamptz)
language plpgsql security definer set search_path = public, pg_temp as $$
declare
  v_uid uuid := auth.uid();
  v_tier public.age_tier;
  v_ver text;
  v_now timestamptz := now();
begin
  if v_uid is null then
    raise exception 'sign in required' using errcode = '28000';
  end if;
  select p.age_tier into v_tier from public.profiles p where p.id = v_uid;
  if v_tier is null then v_tier := 'undeclared'; end if;
  select pol.version into v_ver from public.data_sharing_policy pol
   where pol.in_force_from <= v_now order by pol.in_force_from desc limit 1;

  -- Opting OUT always works, whoever you are. Opting IN is gated on being an adult, and
  -- the gate lives here rather than in the interface, so turning it on is impossible
  -- rather than merely hidden.
  if p_opt_in and v_tier is distinct from '18_plus' then
    raise exception 'the data sharing programme is open to adults only' using errcode = '42501';
  end if;
  if p_opt_in and v_ver is null then
    raise exception 'no policy version in force' using errcode = '42501';
  end if;

  update public.profiles p
     set data_sharing_opt_in = p_opt_in,
         data_sharing_at = case when p_opt_in then v_now else null end,
         data_sharing_policy_version = case when p_opt_in then v_ver else null end
   where p.id = v_uid;
  insert into public.data_sharing_events (user_id, action, policy_version, age_tier, source)
  values (v_uid, case when p_opt_in then 'opt_in' else 'opt_out' end, v_ver, v_tier,
          coalesce(nullif(left(p_source, 40), ''), 'account'));
  return query select p_opt_in, v_tier, v_ver, v_now;
end $$;

create or replace function public.my_data_sharing()
returns table (opt_in boolean, tier public.age_tier, policy_version text, changed_at timestamptz)
language sql security definer set search_path = public, pg_temp as $$
  select coalesce(p.data_sharing_opt_in, false),
         coalesce(p.age_tier, 'undeclared'::public.age_tier),
         p.data_sharing_policy_version, p.data_sharing_at
  from public.profiles p where p.id = auth.uid();
$$;

-- PUBLIC holds EXECUTE on every new function by default; revoking from anon or
-- authenticated alone does nothing while it does.
revoke all on function public.set_data_sharing(boolean, text) from public, anon;
revoke all on function public.my_data_sharing() from public, anon;
grant execute on function public.set_data_sharing(boolean, text) to authenticated;
grant execute on function public.my_data_sharing() to authenticated;

-- sellable_profiles filters on consent recorded at or after in_force_from, so until this
-- row exists nothing is exportable. That is the behaviour we want, not an accident.
insert into public.data_sharing_policy (version, in_force_from, note)
values ('2026-09-18', '2026-09-18T00:00:00Z',
        'First version to disclose the data sharing programme. Adults 18 and over only, '
        'opt in, self declared profile fields only. Practice answers, essays, email, name, '
        'payment details, IP addresses, error reports and forum posts are excluded at '
        'every version. Consent recorded before this date does not qualify.')
on conflict (version) do nothing;

-- ---------------------------------------------------------------------------------
-- 2. Trigger firing order on profiles. This was a real bug, not a tidy-up.
-- ---------------------------------------------------------------------------------
-- Postgres fires same-timing triggers in alphabetical order by name, and these two were
-- named without anyone deciding an order, so they got one anyway:
-- profiles_sharing_eligibility sorted before profiles_sync_age_tier.
--
-- That is backwards. Eligibility was judged against the age_tier already in the row,
-- before sync_age_tier recomputed it from the birth month and year in the same statement.
-- An adult who set their birth date and opted in together had the opt-in revoked by the
-- trigger meant to protect minors, silently. Every exclusion still held, which is why it
-- looked fine: the failure was in the direction of sharing nothing.
--
-- The numbers are in the names on purpose. The order is load-bearing, so it should be
-- readable in \d profiles rather than deduced from the alphabet.
alter trigger profiles_sync_age_tier on public.profiles
  rename to profiles_trg_1_sync_age_tier;
alter trigger profiles_sharing_eligibility on public.profiles
  rename to profiles_trg_2_sharing_eligibility;

-- Second bug, same family. UPDATE OF <columns> fires on the columns NAMED IN THE
-- STATEMENT, not on the columns that changed, and not on what an earlier BEFORE trigger
-- wrote into NEW. So "update profiles set birth_year = 2011" ran sync_age_tier, stored a
-- minor's tier, and skipped eligibility entirely, leaving the opt-in true.
--
-- sellable_profiles filters on age_tier so nothing was exportable either way. It was
-- still wrong twice: the Account page reads the flag and would have told a 14 year old
-- their profile was being shared, and privacy.html says in as many words that the revoke
-- happens at the database level rather than by anybody remembering.
--
-- The column list was a micro-optimisation on a table written a few times per session.
-- Dropping it costs one enum comparison per update and makes the guarantee unconditional.
drop trigger if exists profiles_trg_2_sharing_eligibility on public.profiles;
create trigger profiles_trg_2_sharing_eligibility
  before insert or update on public.profiles
  for each row execute function public.enforce_sharing_eligibility();
