-- Applied 2026-09-20. Social sign in, with every claim traceable to the provider that
-- asserted it.
--
-- The reason this is a table rather than a few more columns on profiles: an OAuth
-- provider gives us assertions, not facts, and providers differ in what they assert and
-- how reliably. Google's email is verified. Apple's is often a private relay address that
-- forwards. GitHub's may be absent entirely. Flattening that into profiles.email loses
-- the one thing that makes it trustworthy later, which is knowing who said it and when.
--
-- The rule enforced here, and it is the whole point: store exactly what a provider sent,
-- attributed, and never infer. No deriving a display name from an email local part, no
-- guessing a country from a locale, no filling a birth date nobody gave us. A blank stays
-- blank.
--
-- Worth stating plainly because it shapes what this can ever be used for: OAuth does NOT
-- hand over a person's history. The default scopes return an id, usually an email, and
-- sometimes a display name. Not search history, not purchases, not contacts, not
-- documents. Anything beyond that needs additional scopes, explicit consent, and for the
-- sensitive ones a provider security review. None of those extra scopes are requested.

create table if not exists public.identity_claims (
  id            bigint generated always as identity primary key,
  user_id       uuid not null references auth.users(id) on delete cascade,
  provider      text not null check (provider in
                  ('apple','google','azure','github','email')),
  -- The provider's own id for this person. Stable across email changes, which is why it
  -- is the join key and the email is not.
  provider_uid  text not null,
  -- Exactly what arrived, unmodified. Keeping the raw payload means a later question
  -- about where a value came from is answerable from the record.
  raw_claims    jsonb not null default '{}'::jsonb,
  email         text,
  -- Whether the PROVIDER says it verified this address. Apple private relay counts as
  -- verified and deliverable; an unverified Google address does not.
  email_verified boolean,
  -- True when the address is an Apple private relay forwarder. It works, but it is not
  -- the person's real address and must never be presented as one, or sold as one.
  is_private_relay boolean generated always as
                  (email is not null and email like '%@privaterelay.appleid.com') stored,
  full_name     text,
  avatar_url    text,
  locale        text,
  first_seen    timestamptz not null default now(),
  last_seen     timestamptz not null default now(),
  unique (provider, provider_uid)
);

comment on table public.identity_claims is
  'What each OAuth provider asserted about a user, attributed and unmodified. Providers '
  'give assertions, not facts, and they differ in what they assert and how reliably. '
  'Nothing here is ever inferred: a field a provider did not send stays null.';
comment on column public.identity_claims.is_private_relay is
  'Apple private relay addresses forward but are not the person''s real address. Never '
  'present one as their email, and never include one in a data sharing export.';

create index if not exists identity_claims_user_idx on public.identity_claims (user_id);

alter table public.identity_claims enable row level security;
drop policy if exists identity_claims_own_read on public.identity_claims;
create policy identity_claims_own_read on public.identity_claims
  for select to authenticated using (user_id = auth.uid());
revoke all on public.identity_claims from public, anon;
grant select on public.identity_claims to authenticated;

-- Record a sign in, and fill ONLY blanks on the profile.
--
-- The merge rule is one sentence: a provider may fill a field the person has left empty,
-- and may never overwrite a field the person filled in themselves. Somebody who typed
-- their preferred name into the Account page does not get it silently replaced by their
-- legal name from Microsoft on their next sign in.
create or replace function public.record_identity_claim()
returns trigger language plpgsql security definer set search_path = public, pg_temp as $$
declare
  m jsonb := coalesce(new.raw_user_meta_data, '{}'::jsonb);
  v_provider text := coalesce(new.provider, 'email');
  v_name text;
  v_avatar text;
  v_email text := nullif(new.identity_data->>'email', '');
  v_verified boolean;
begin
  -- Providers disagree on the key. Take the ones they actually use and nothing else: an
  -- absent name is absent, not a chance to synthesise one from the address.
  v_name := nullif(coalesce(new.identity_data->>'full_name',
                            new.identity_data->>'name',
                            m->>'full_name', m->>'name'), '');
  v_avatar := nullif(coalesce(new.identity_data->>'avatar_url',
                              new.identity_data->>'picture',
                              m->>'avatar_url', m->>'picture'), '');
  -- Only trust an explicit true. A missing email_verified is unknown, not verified.
  v_verified := case when (new.identity_data->>'email_verified')::text = 'true' then true
                     when (new.identity_data->>'email_verified')::text = 'false' then false
                     else null end;

  insert into public.identity_claims
    (user_id, provider, provider_uid, raw_claims, email, email_verified,
     full_name, avatar_url, locale)
  values
    (new.user_id, v_provider, new.id, coalesce(new.identity_data, '{}'::jsonb),
     v_email, v_verified, v_name, v_avatar, nullif(new.identity_data->>'locale',''))
  on conflict (provider, provider_uid) do update
    set last_seen = now(),
        raw_claims = excluded.raw_claims,
        -- Apple sends the name ONCE, on the first authorization, and never again. So a
        -- later sign in must not null it out by overwriting with what it did not send.
        email = coalesce(excluded.email, identity_claims.email),
        email_verified = coalesce(excluded.email_verified, identity_claims.email_verified),
        full_name = coalesce(excluded.full_name, identity_claims.full_name),
        avatar_url = coalesce(excluded.avatar_url, identity_claims.avatar_url),
        locale = coalesce(excluded.locale, identity_claims.locale);

  -- Fill blanks on the profile. coalesce ordering is the enforcement: the existing value
  -- wins whenever there is one.
  update public.profiles p
     set display_name = coalesce(nullif(p.display_name, ''), v_name),
         email = coalesce(nullif(p.email, ''), v_email)
   where p.id = new.user_id;

  return new;
end $$;

drop trigger if exists identities_record_claim on auth.identities;
create trigger identities_record_claim
  after insert or update on auth.identities
  for each row execute function public.record_identity_claim();

revoke all on function public.record_identity_claim() from public, anon, authenticated;

-- What the app shows on the Account page: which accounts are linked, and what each one
-- actually told us. Deliberately exposes is_private_relay, because a person who signed
-- in with Apple and hid their email should be able to see that we only have a forwarder.
create or replace function public.my_identities()
returns table (provider text, email text, email_verified boolean, is_private_relay boolean,
               full_name text, avatar_url text, first_seen timestamptz)
language sql stable security definer set search_path = public, pg_temp as $$
  select c.provider, c.email, c.email_verified, c.is_private_relay,
         c.full_name, c.avatar_url, c.first_seen
  from public.identity_claims c
  where c.user_id = auth.uid()
  order by c.first_seen;
$$;

revoke all on function public.my_identities() from public, anon;
grant execute on function public.my_identities() to authenticated;
