alter table forum_threads add column if not exists last_author text;
update forum_threads set last_author = author_name where last_author is null;

create or replace function forum_after_post() returns trigger
language plpgsql security definer set search_path to 'public' as $$
begin
  update forum_threads set reply_count = reply_count + 1, last_post_at = new.created_at, last_author = new.author_name
  where id = new.thread_id;
  return new;
end $$;

create or replace function forum_thread_before() returns trigger
language plpgsql security definer set search_path to 'public' as $$
declare s jsonb; cnt int;
begin
  new.user_id := auth.uid();
  new.author_name := left(trim(coalesce(new.author_name, '')), 40);
  if char_length(new.author_name) < 2 then new.author_name := 'Anonymous'; end if;
  new.last_author := new.author_name;
  new.country := left(coalesce(req_header('cf-ipcountry'), ''), 8);
  new.ip_hash := req_ip_hash();
  new.reviewed_at := null; new.review_action := null;
  if not is_admin() then
    new.locked := false; new.hidden := false;
  end if;
  select count(*) into cnt from forum_threads
    where ip_hash = new.ip_hash and created_at > now() - interval '1 hour';
  if cnt >= 3 then
    raise exception 'Slow down: up to 3 new threads per hour.';
  end if;
  select count(*) into cnt from forum_threads
    where ip_hash = new.ip_hash and created_at > now() - interval '24 hours';
  if cnt >= 8 then
    raise exception 'Daily thread limit reached. Try again tomorrow.';
  end if;
  s := forum_screen(coalesce(new.title, '') || ' ' || coalesce(new.body, ''));
  new.flagged := (s->>'flagged')::boolean;
  new.flag_reason := nullif(s->>'reason', '');
  if (s->>'hide')::boolean then new.hidden := true; end if;
  return new;
end $$;
