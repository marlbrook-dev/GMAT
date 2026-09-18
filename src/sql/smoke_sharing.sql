-- Database half of the data sharing guarantees. Paste into the Supabase SQL editor, or
-- run through the MCP execute_sql tool. It ALWAYS ends by raising, which rolls the whole
-- block back: the results arrive in the error message and nothing synthetic survives.
-- Confirm that afterwards with:
--   select count(*) from auth.users where email like 'smoke-%@example.invalid';  -- want 0
--
-- The browser half lives in src/smoke_sharing.js. This is the half a page cannot test:
-- whether the view and the triggers hold when somebody writes the table directly.
--
-- Two bugs were found by exactly this test and would not have been found by reading the
-- code, because both were about trigger firing rules rather than trigger bodies:
--
--   1. Both triggers are BEFORE triggers, and Postgres fires same-timing triggers in
--      alphabetical order by name. profiles_sharing_eligibility sorted before
--      profiles_sync_age_tier, so eligibility was judged against the age_tier already in
--      the row rather than the one the same statement was establishing. Every legitimate
--      adult opt-in was silently revoked. Hence the trg_1 / trg_2 names: the order is
--      load-bearing and should be readable rather than deduced from the alphabet.
--
--   2. The eligibility trigger was BEFORE INSERT OR UPDATE OF age_tier,
--      data_sharing_opt_in. UPDATE OF fires on the columns NAMED IN THE STATEMENT, not on
--      what changed and not on what an earlier BEFORE trigger wrote into NEW. So
--      "update profiles set birth_year = 2011" ran the sync, stored a minor's tier, and
--      never ran the eligibility check. The view still excluded the row, so nothing was
--      exportable, but the flag said otherwise and the Account page reads the flag.
--
-- The lesson both share: an exclusion that is never exercised is not known to work.
do $$
declare
  u1 uuid := '00000000-0000-4000-8000-000000000001';
  u2 uuid := '00000000-0000-4000-8000-000000000002';
  u3 uuid := '00000000-0000-4000-8000-000000000003';
  u4 uuid := '00000000-0000-4000-8000-000000000004';
  r text := E'\n'; n int; t text; ok boolean := true;
begin
  -- A trigger on auth.users creates the profiles row, so these update rather than insert.
  insert into auth.users (id, instance_id, aud, role, email, encrypted_password,
                          email_confirmed_at, created_at, updated_at)
  select x, '00000000-0000-0000-0000-000000000000', 'authenticated', 'authenticated',
         'smoke-' || x || '@example.invalid', '', now(), now(), now()
  from unnest(array[u1,u2,u3,u4]) x;
  insert into public.profiles (id, email) select x, 'x@example.invalid'
    from unnest(array[u1,u2,u3,u4]) x on conflict (id) do nothing;

  -- Birth data and opt-in in ONE statement, which is the case bug 1 broke.
  update public.profiles set birth_year=1995, birth_month=5, country='US',
    data_sharing_opt_in=true, data_sharing_at=now(),
    data_sharing_policy_version='2026-09-18' where id=u1;
  -- A 16 year old with the flag forced true directly in the table, bypassing the RPC.
  update public.profiles set birth_year=2010, birth_month=5, country='US',
    data_sharing_opt_in=true, data_sharing_at=now(),
    data_sharing_policy_version='2026-09-18' where id=u2;
  -- An adult whose consent predates the policy that disclosed the programme.
  update public.profiles set birth_year=1990, birth_month=2, country='US',
    data_sharing_opt_in=true, data_sharing_at='2026-06-01T00:00:00Z',
    data_sharing_policy_version='2026-09-18' where id=u3;
  update public.profiles set birth_year=1988, birth_month=9, country='US' where id=u4;

  select count(*) into n from public.sellable_profiles where id=u1;
  r := r || format(E'adult, opted in under the current policy      -> sellable %s  (want 1)  %s\n',
                   n, case when n=1 then 'ok' else 'FAIL' end);
  if n<>1 then ok:=false; end if;

  select age_tier::text into t from public.profiles where id=u2;
  select count(*) into n from public.sellable_profiles where id=u2;
  r := r || format(E'16 year old, opt_in forced true in the table  -> tier %s, sellable %s  (want 13_17, 0)  %s\n',
                   t, n, case when n=0 and t='13_17' then 'ok' else 'FAIL' end);
  if n<>0 or t<>'13_17' then ok:=false; end if;

  select count(*) into n from public.sellable_profiles where id=u3;
  r := r || format(E'adult, consent predates the policy in force   -> sellable %s  (want 0)  %s\n',
                   n, case when n=0 then 'ok' else 'FAIL' end);
  if n<>0 then ok:=false; end if;

  select count(*) into n from public.sellable_profiles where id=u4;
  r := r || format(E'adult, never opted in                        -> sellable %s  (want 0)  %s\n',
                   n, case when n=0 then 'ok' else 'FAIL' end);
  if n<>0 then ok:=false; end if;

  -- The realistic failure: somebody corrects a birth year long after opting in.
  update public.profiles set birth_year=2011 where id=u1;
  select coalesce(data_sharing_opt_in::text,'null') into t from public.profiles where id=u1;
  select count(*) into n from public.sellable_profiles where id=u1;
  r := r || format(E'that adult corrected to a 14 year old         -> opt_in %s, sellable %s  (want false, 0)  %s\n',
                   t, n, case when t='false' and n=0 then 'ok' else 'FAIL' end);
  if t<>'false' or n<>0 then ok:=false; end if;

  -- Revocation is one way on purpose: a birth year cannot re-grant consent.
  update public.profiles set birth_year=1995 where id=u1;
  select coalesce(data_sharing_opt_in::text,'null') into t from public.profiles where id=u1;
  r := r || format(E'corrected back up to an adult                 -> opt_in %s  (want false, revoked stays revoked)  %s\n',
                   t, case when t='false' then 'ok' else 'FAIL' end);
  if t<>'false' then ok:=false; end if;

  select count(*) into n from public.data_sharing_events where user_id=u1 and action='revoked_by_age';
  r := r || format(E'the revoke wrote an audit row                 -> %s row(s)  (want 1)  %s\n',
                   n, case when n=1 then 'ok' else 'FAIL' end);
  if n<>1 then ok:=false; end if;

  r := r || format(E'\n%s\n', case when ok then 'ALL DATABASE GUARANTEES HOLD'
                                   else 'SOMETHING FAILED, READ THE LINES ABOVE' end);
  raise exception 'RESULTS (rolled back): %', r;
end $$;
