-- Applied 2026-09-19. Switches the sharing programme from opt in to opt out.
--
-- The first build asked adults to switch sharing ON. That was more conservative than
-- California requires: CCPA is an opt OUT regime, so an adult's data may be sold unless
-- they say no, provided notice was given and the Do Not Sell link is there. Both are. Opt
-- in was costing the entire cohort for no legal benefit.
--
-- It is not uniform, and pretending it is would be the expensive mistake. GDPR offers no
-- opt out for this: selling personal data in the EEA, the UK or Switzerland needs a
-- lawful basis, and consent is the only practical one. So the basis is per person and
-- decided by where they signed up.
--
-- Tested by src/sql/smoke_sharing.sql, which rolls itself back.

alter table public.profiles add column if not exists signup_country text;
comment on column public.profiles.signup_country is
  'Two letter country from cf-ipcountry at account creation. Decides whether sharing is '
  'opt out (default on) or opt in (default off). Distinct from profiles.country, which is '
  'self declared, optional, and must never drive a legal basis.';

create or replace function public.stamp_signup_country()
returns trigger language plpgsql security definer set search_path = public, pg_temp as $$
begin
  if new.signup_country is null then
    new.signup_country := nullif(upper(left(coalesce(req_header('cf-ipcountry'), ''), 2)), '');
  end if;
  return new;
end $$;

drop trigger if exists profiles_trg_0_signup_country on public.profiles;
create trigger profiles_trg_0_signup_country
  before insert on public.profiles
  for each row execute function public.stamp_signup_country();
revoke all on function public.stamp_signup_country() from public, anon, authenticated;

-- The active refusal, kept separate from data_sharing_opt_in. Under an opt out model
-- "has not opted in" and "has opted out" are completely different states, and collapsing
-- them into one nullable boolean is exactly how a refusal gets read as an absence.
alter table public.profiles add column if not exists data_sharing_opt_out boolean not null default false;
alter table public.profiles add column if not exists data_sharing_opt_out_at timestamptz;
comment on column public.profiles.data_sharing_opt_out is
  'The person said no. Always honoured, in every jurisdiction, whatever the basis, and '
  'never cleared except by the person themselves opting back in.';

-- An unknown country counts as consent required: unknown jurisdiction means unknown
-- obligations, and with Cloudflare in front of the site a missing header is rare enough
-- to be worth the caution.
create or replace function public.sharing_basis(p_country text)
returns text language sql immutable set search_path = public, pg_temp as $$
  select case
    when p_country is null then 'opt_in'
    when upper(p_country) in (
      'AT','BE','BG','HR','CY','CZ','DK','EE','FI','FR','DE','GR','HU','IE','IT','LV',
      'LT','LU','MT','NL','PL','PT','RO','SK','SI','ES','SE',   -- EU 27
      'IS','LI','NO',                                            -- rest of the EEA
      'GB','CH'                                                  -- UK, Switzerland
    ) then 'opt_in'
    else 'opt_out'
  end;
$$;
comment on function public.sharing_basis(text) is
  'opt_in where consent is required before selling (EEA, UK, Switzerland, unknown), '
  'opt_out everywhere else. Takes signup_country, never the self declared country.';
revoke all on function public.sharing_basis(text) from public, anon;
grant execute on function public.sharing_basis(text) to authenticated;

-- Both views are rebuilt rather than replaced: CREATE OR REPLACE VIEW cannot add a column
-- in the middle of the list. Enriched depends on plain, so it goes first and returns last.
drop view if exists public.sellable_profiles_enriched;
drop view if exists public.sellable_profiles;

-- Four conditions, and the third is the one worth reading twice. An account created
-- BEFORE the policy version that disclosed the programme never received notice of it, so
-- flipping the default must not sweep it in; those accounts are sellable only if they opt
-- in themselves. That rule mattered less under opt in. Under opt out it is the only thing
-- standing between a changed default and selling data collected under the opposite promise.
create view public.sellable_profiles as
select p.id, p.age_tier, p.country, p.signup_country,
       public.sharing_basis(p.signup_country) as basis,
       p.education_level, p.intended_major, p.target_schools, p.score_goal,
       p.application_year, p.budget_band, p.employer_industry, p.household_income_band,
       p.first_generation, p.military_status, p.study_hours_band, p.exam,
       p.data_sharing_at, p.data_sharing_policy_version
from public.profiles p
cross join lateral (
  select pol.version, pol.in_force_from from public.data_sharing_policy pol
  where pol.in_force_from <= now() order by pol.in_force_from desc limit 1
) cur
where p.age_tier = '18_plus'
  and p.data_sharing_opt_out is not true
  and p.created_at >= cur.in_force_from
  and (
    public.sharing_basis(p.signup_country) = 'opt_out'
    or (p.data_sharing_opt_in is true
        and p.data_sharing_at is not null
        and p.data_sharing_at >= cur.in_force_from)
  );

create view public.sellable_profiles_enriched as
select s.*,
       coalesce((select jsonb_object_agg(a.attribute, a.value) from public.profile_appended a
                  where a.user_id = s.id and (a.expires_at is null or a.expires_at > now())),
                '{}'::jsonb) as appended,
       coalesce((select array_agg(distinct a.source) from public.profile_appended a
                  where a.user_id = s.id and (a.expires_at is null or a.expires_at > now())),
                '{}'::text[]) as appended_sources
from public.sellable_profiles s;

revoke all on public.sellable_profiles from public, anon, authenticated;
revoke all on public.sellable_profiles_enriched from public, anon, authenticated;

-- The two RPCs change their return shape, so they are dropped rather than replaced.
--
-- The important change: saying no now WRITES something. Under opt in, "no" was the
-- absence of a yes, and absence is indistinguishable from never having been asked. Under
-- opt out, absence means the opposite, so a refusal has to be a stored fact or it is not
-- a refusal at all.
drop function if exists public.set_data_sharing(boolean, text);
drop function if exists public.my_data_sharing();

create function public.set_data_sharing(p_opt_in boolean, p_source text default 'account')
returns table (sharing boolean, basis text, tier public.age_tier, policy_version text, changed_at timestamptz)
language plpgsql security definer set search_path = public, pg_temp as $$
declare
  v_uid uuid := auth.uid();
  v_tier public.age_tier; v_basis text; v_ver text;
  v_now timestamptz := now(); v_sharing boolean;
begin
  if v_uid is null then raise exception 'sign in required' using errcode = '28000'; end if;
  select p.age_tier, public.sharing_basis(p.signup_country) into v_tier, v_basis
    from public.profiles p where p.id = v_uid;
  if v_tier is null then v_tier := 'undeclared'; end if;
  if v_basis is null then v_basis := 'opt_in'; end if;
  select pol.version into v_ver from public.data_sharing_policy pol
   where pol.in_force_from <= v_now order by pol.in_force_from desc limit 1;

  if p_opt_in then
    if v_tier is distinct from '18_plus' then
      raise exception 'the data sharing programme is open to adults only' using errcode = '42501';
    end if;
    if v_ver is null then
      raise exception 'no policy version in force' using errcode = '42501';
    end if;
    update public.profiles p set data_sharing_opt_in = true, data_sharing_at = v_now,
           data_sharing_policy_version = v_ver, data_sharing_opt_out = false,
           data_sharing_opt_out_at = null
     where p.id = v_uid;
  else
    -- Opting OUT always succeeds, for anyone, in any jurisdiction, at any age, with no
    -- conditions. There is no state in which refusing should fail.
    update public.profiles p set data_sharing_opt_out = true, data_sharing_opt_out_at = v_now,
           data_sharing_opt_in = false, data_sharing_at = null,
           data_sharing_policy_version = null
     where p.id = v_uid;
  end if;

  insert into public.data_sharing_events (user_id, action, policy_version, age_tier, source)
  values (v_uid, case when p_opt_in then 'opt_in' else 'opt_out' end, v_ver, v_tier,
          coalesce(nullif(left(p_source, 40), ''), 'account'));

  -- Report what is actually true by asking the view, not by reasoning about the flags.
  -- The view is what an export reads, so it is the only honest answer to "is my data
  -- being shared".
  select exists (select 1 from public.sellable_profiles s where s.id = v_uid) into v_sharing;
  return query select v_sharing, v_basis, v_tier, v_ver, v_now;
end $$;

comment on function public.set_data_sharing(boolean, text) is
  'Record the caller''s sharing choice and write the audit row. Opting out always '
  'succeeds, unconditionally. Opting in requires age_tier = 18_plus. The returned '
  'sharing flag is read back from sellable_profiles, not inferred.';

create function public.my_data_sharing()
returns table (sharing boolean, basis text, opted_out boolean, opt_in boolean,
               tier public.age_tier, policy_version text, changed_at timestamptz)
language sql security definer set search_path = public, pg_temp as $$
  select exists (select 1 from public.sellable_profiles s where s.id = p.id),
         public.sharing_basis(p.signup_country),
         coalesce(p.data_sharing_opt_out, false),
         coalesce(p.data_sharing_opt_in, false),
         coalesce(p.age_tier, 'undeclared'::public.age_tier),
         p.data_sharing_policy_version,
         coalesce(p.data_sharing_opt_out_at, p.data_sharing_at)
  from public.profiles p where p.id = auth.uid();
$$;

revoke all on function public.set_data_sharing(boolean, text) from public, anon;
revoke all on function public.my_data_sharing() from public, anon;
grant execute on function public.set_data_sharing(boolean, text) to authenticated;
grant execute on function public.my_data_sharing() to authenticated;
