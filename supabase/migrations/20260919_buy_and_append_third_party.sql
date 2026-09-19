-- Applied 2026-09-19. Data bought about our own users and appended to their profile.
--
-- Its own table rather than columns on profiles, for three reasons that are the same
-- reason. A deletion request has to reach purchased data, and it cannot reach what it
-- cannot tell apart. privacy.html says the profile fields are self-declared, and that
-- sentence stays true only if bought values never land in them. And when a broker's data
-- is wrong, which it routinely is, we need to drop that source without touching what the
-- person told us themselves.
--
-- The split this follows is the one the law draws. Buying and appending needs NOTICE,
-- which privacy.html section 2 gives. Selling needs an OPT OUT, which set_data_sharing
-- already is. So purchased attributes may attach to any adult account, and nothing leaves
-- for a partner unless that account has also switched sharing on.

create table if not exists public.profile_appended (
  id           bigint generated always as identity primary key,
  user_id      uuid not null references auth.users(id) on delete cascade,
  attribute    text not null check (length(attribute) between 1 and 60),
  value        text check (length(value) <= 200),
  source       text not null check (length(source) between 1 and 80),
  acquired_at  timestamptz not null default now(),
  expires_at   timestamptz,
  unique (user_id, attribute, source)
);
create index if not exists profile_appended_user_idx   on public.profile_appended (user_id);
create index if not exists profile_appended_source_idx on public.profile_appended (source);

-- Appending to a minor fails rather than being filtered out later by whoever remembers.
create or replace function public.enforce_append_eligibility()
returns trigger language plpgsql security definer set search_path = public, pg_temp as $$
declare v_tier public.age_tier;
begin
  select p.age_tier into v_tier from public.profiles p where p.id = new.user_id;
  if v_tier is distinct from '18_plus' then
    raise exception 'third party data may only be appended to accounts recorded as 18 or over (tier: %)',
      coalesce(v_tier::text, 'no profile') using errcode = '42501';
  end if;
  return new;
end $$;

drop trigger if exists profile_appended_adults_only on public.profile_appended;
create trigger profile_appended_adults_only
  before insert or update on public.profile_appended
  for each row execute function public.enforce_append_eligibility();

-- If an age is later corrected below 18, purchased data about that account goes. The
-- sharing trigger revokes consent on the same event; this is the other half of it.
create or replace function public.purge_appended_on_minor()
returns trigger language plpgsql security definer set search_path = public, pg_temp as $$
begin
  if new.age_tier is distinct from '18_plus' then
    delete from public.profile_appended where user_id = new.id;
  end if;
  return new;
end $$;

drop trigger if exists profiles_trg_3_purge_appended on public.profiles;
create trigger profiles_trg_3_purge_appended
  after insert or update on public.profiles
  for each row execute function public.purge_appended_on_minor();

-- A person can read and delete what we bought about them, and nobody can insert: appends
-- run through the service role only.
alter table public.profile_appended enable row level security;
drop policy if exists profile_appended_own_read on public.profile_appended;
create policy profile_appended_own_read on public.profile_appended
  for select to authenticated using (user_id = auth.uid());
drop policy if exists profile_appended_own_delete on public.profile_appended;
create policy profile_appended_own_delete on public.profile_appended
  for delete to authenticated using (user_id = auth.uid());
revoke all on public.profile_appended from public, anon;
grant select, delete on public.profile_appended to authenticated;

-- Two views on purpose. sellable_profiles is unchanged: self-declared fields only.
--
-- sellable_profiles_enriched adds the purchased attributes. Separate, because reselling
-- data we bought is a different business from selling what our own users told us.
-- California's Delete Act exempts a business selling data about people it has a direct
-- relationship with, and every row here is about an account holder, so that exemption
-- should still hold. The line is close enough that crossing it should be visible in the
-- schema instead of buried in a join.
create or replace view public.sellable_profiles_enriched as
select s.*,
       coalesce((select jsonb_object_agg(a.attribute, a.value) from public.profile_appended a
                  where a.user_id = s.id and (a.expires_at is null or a.expires_at > now())),
                '{}'::jsonb) as appended,
       coalesce((select array_agg(distinct a.source) from public.profile_appended a
                  where a.user_id = s.id and (a.expires_at is null or a.expires_at > now())),
                '{}'::text[]) as appended_sources
from public.sellable_profiles s;
revoke all on public.sellable_profiles_enriched from public, anon, authenticated;

-- ---------------------------------------------------------------------------------
-- Advisor findings against the two migrations above, fixed the same day.
-- ---------------------------------------------------------------------------------
-- data_sharing_policy had no RLS. PostgREST exposes every public table, so the policy
-- version list was writable by anyone holding the publishable key. sellable_profiles
-- joins it to decide whether a consent predates the disclosure, so moving in_force_from
-- backwards would have made consent collected under the old "we never sell" promise
-- exportable. Read stays open: it is a published document.
alter table public.data_sharing_policy enable row level security;
drop policy if exists data_sharing_policy_public_read on public.data_sharing_policy;
create policy data_sharing_policy_public_read on public.data_sharing_policy
  for select to anon, authenticated using (true);
revoke insert, update, delete on public.data_sharing_policy from anon, authenticated;
grant select on public.data_sharing_policy to anon, authenticated;

-- A mutable search_path on a SECURITY DEFINER function is the classic escalation: the
-- caller's search_path decides which `profiles` the function means.
alter function public.enforce_sharing_eligibility()       set search_path = public, pg_temp;
alter function public.sync_age_tier()                     set search_path = public, pg_temp;
alter function public.age_from_birth(smallint, smallint)  set search_path = public, pg_temp;
alter function public.tier_from_birth(smallint, smallint) set search_path = public, pg_temp;

-- Trigger functions were reachable at /rest/v1/rpc/ as SECURITY DEFINER. Calling one
-- outside a trigger errors, so it was not exploitable, but it is surface nobody put
-- there on purpose.
revoke all on function public.enforce_sharing_eligibility()       from public, anon, authenticated;
revoke all on function public.enforce_append_eligibility()        from public, anon, authenticated;
revoke all on function public.purge_appended_on_minor()           from public, anon, authenticated;
revoke all on function public.sync_age_tier()                     from public, anon, authenticated;
revoke all on function public.age_from_birth(smallint, smallint)  from public, anon, authenticated;
revoke all on function public.tier_from_birth(smallint, smallint) from public, anon, authenticated;
