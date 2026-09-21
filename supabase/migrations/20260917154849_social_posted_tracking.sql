-- Which generated social posts have actually been sent, and where.
--
-- The queue itself is a build artefact regenerated on every build, so it cannot remember
-- anything. This table is the memory: without it the same post reappears every day and
-- the queue is a list rather than a queue.
--
-- Admin only in both directions. There is nothing here worth reading for anyone else, and
-- the ability to mark a post sent is the ability to hide it from the person posting.
create table if not exists public.social_posted (
  post_key   text primary key,
  channel    text not null default 'x',
  posted_at  timestamptz not null default now(),
  posted_by  uuid references auth.users(id) on delete set null,
  note       text,
  constraint social_posted_channel_ck check (channel in ('x','linkedin','bluesky','other')),
  constraint social_posted_note_ck check (note is null or char_length(note) <= 500)
);

alter table public.social_posted enable row level security;

drop policy if exists social_posted_admin_read on public.social_posted;
drop policy if exists social_posted_admin_write on public.social_posted;
drop policy if exists social_posted_admin_delete on public.social_posted;

create policy social_posted_admin_read on public.social_posted
  for select to authenticated using (public.is_admin());
create policy social_posted_admin_write on public.social_posted
  for insert to authenticated with check (public.is_admin());
-- Unmarking matters: a mis-click otherwise buries a post permanently.
create policy social_posted_admin_delete on public.social_posted
  for delete to authenticated using (public.is_admin());

comment on table public.social_posted is
  'Marks which generated social posts have been published and on which channel. Admin read and write only; the queue itself is a build artefact with no memory.';
