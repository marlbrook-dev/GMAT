-- Do the two layers of authorisation on profiles still agree with the Account page?
--
-- Row Level Security scopes every write to the caller's own row. A separate column grant
-- decides which columns a role may write at all, and that second layer is what stops a
-- signed-in browser setting its own plan to Pro. Nothing compared the second layer
-- against the form until twelve self-reported fields had been silently unwritable for
-- the life of the feature (INC-0056).
--
-- So this asserts both directions, because only asserting one is how the drift happened:
-- every field the Account page offers must be writable by authenticated, and every field
-- the server owns must not be.
--
-- Run: paste into the SQL editor, or through the MCP connector. It reads only, and it
-- raises rather than returning rows, so a failure cannot be scrolled past.

do $$
declare
  -- Kept in step with the About You form and birthSave() in src/app_template.html.
  -- Adding a field to that form without adding it here is the drift this catches.
  declared text[] := array[
    'age_range','gender','country','role_type','referral_src',
    'education_level','intended_major','score_goal','application_year',
    'budget_band','employer_industry','household_income_band',
    'first_generation','military_status','study_hours_band',
    'birth_month','birth_year'];
  -- Derived, or written only by an edge function or a trigger. A person may state their
  -- birth date; they may not state the age tier the site derives from it, and they may
  -- certainly not state their plan.
  server_owned text[] := array[
    'plan','plan_status','plan_amount_cents','plan_interval',
    'stripe_customer_id','stripe_subscription_id','age_tier','age_declared_at',
    'data_sharing_opt_in','data_sharing_opt_out','data_sharing_at',
    'data_sharing_policy_version','target_schools','marketing_opt_in',
    'signup_country','trial_end','current_period_end','cancel_at_period_end'];
  c text;
  bad text[] := '{}';
  n_pol int;
begin
  foreach c in array declared loop
    if not has_column_privilege('authenticated', 'public.profiles', c, 'UPDATE') then
      bad := bad || ('authenticated cannot write ' || c || ', but the Account page offers it');
    end if;
    if not has_column_privilege('authenticated', 'public.profiles', c, 'SELECT') then
      bad := bad || ('authenticated cannot read ' || c || ', so the page cannot show what is stored');
    end if;
  end loop;

  foreach c in array server_owned loop
    if has_column_privilege('authenticated', 'public.profiles', c, 'UPDATE') then
      bad := bad || ('authenticated CAN write ' || c || ', which the server owns');
    end if;
    if has_column_privilege('anon', 'public.profiles', c, 'UPDATE') then
      bad := bad || ('anon CAN write ' || c || ', which the server owns');
    end if;
  end loop;

  -- The column grants are only the second layer. Without a row policy scoping writes to
  -- the caller's own row, every grant above would let any signed-in user edit anyone.
  select count(*) into n_pol from pg_policy
   where polrelid = 'public.profiles'::regclass
     and pg_get_expr(polwithcheck, polrelid) like '%auth.uid()%';
  if n_pol < 1 then
    bad := bad || 'no row policy with an auth.uid() WITH CHECK on profiles: the column grants are the only thing standing between a user and everyone else''s row';
  end if;

  if array_length(bad, 1) is not null then
    raise exception E'profile grants do not match the Account page:\n  %',
      array_to_string(bad, E'\n  ');
  end if;
  raise notice 'profile grants ok: % declared fields writable, % server owned fields refused, row policy present',
    array_length(declared, 1), array_length(server_owned, 1);
end $$;
