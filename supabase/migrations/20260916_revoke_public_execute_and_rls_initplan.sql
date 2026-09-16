-- Two findings from the Supabase advisors, and one lesson worth writing down.
--
-- 1. The lesson. 20260916_harden_plan_column_and_rpc_surface.sql revoked EXECUTE on the
--    admin and trigger functions "from anon, authenticated" and I checked the explicit
--    grants afterwards, which looked clean. They were not. Postgres grants EXECUTE on every
--    new function to PUBLIC by default, and anon and authenticated inherit that. Revoking
--    a role's own grant leaves the PUBLIC grant untouched, so the door stayed open. The
--    tell is a leading "=X/postgres" in pg_proc.proacl. Always revoke from PUBLIC too.
--
--    Nothing was exploitable through that gap. The five trigger functions return `trigger`,
--    which PostgREST will not expose and which Postgres refuses to call directly, and every
--    admin_* function opens with `if not is_admin() then raise exception`. This is defence
--    in depth: one refactor that drops a guard line should not become a data breach.
revoke execute on function public.handle_new_user()        from public;
revoke execute on function public.site_events_before()     from public;
revoke execute on function public.forum_post_before()      from public;
revoke execute on function public.forum_after_post()       from public;
revoke execute on function public.forum_thread_before()    from public;
revoke execute on function public.admin_mod_queue()        from public;
revoke execute on function public.admin_moderate(text, bigint, text) from public;
revoke execute on function public.admin_traffic(integer)   from public;
revoke execute on function public.admin_user_detail(uuid)  from public;
revoke execute on function public.admin_users(text, integer, text, integer) from public;
revoke execute on function public.admin_bi()               from public;

-- is_admin() keeps its explicit grants on purpose: the app calls it to decide whether to
-- show the Admin tab. It reads auth.jwt() and returns false for a caller who is not on the
-- admin list, so an anonymous call learns nothing. Only the implicit PUBLIC grant goes.
revoke execute on function public.is_admin() from public;
grant  execute on function public.is_admin() to anon, authenticated;

-- 2. RLS initplan. A bare auth.uid() inside a policy is re-evaluated once per row.
--    Wrapping it in a scalar subquery makes Postgres evaluate it once per statement.
--    Same predicate, same access, much better plan as attempts grows.
alter policy "own profile"  on public.profiles
  using ((select auth.uid()) = id) with check ((select auth.uid()) = id);
alter policy "own attempts" on public.attempts
  using ((select auth.uid()) = user_id) with check ((select auth.uid()) = user_id);
alter policy "own events"   on public.events
  using ((select auth.uid()) = user_id) with check ((select auth.uid()) = user_id);
alter policy "own sessions" on public.sessions
  using ((select auth.uid()) = user_id) with check ((select auth.uid()) = user_id);
alter policy thread_moderate on public.forum_threads
  using (((select auth.uid()) = user_id) or is_admin())
  with check (((select auth.uid()) = user_id) or is_admin());
alter policy post_moderate on public.forum_posts
  using (((select auth.uid()) = user_id) or is_admin())
  with check (((select auth.uid()) = user_id) or is_admin());
alter policy thread_insert on public.forum_threads
  with check ((((select auth.uid()) is null) and (user_id is null)) or (user_id = (select auth.uid())));
alter policy post_insert on public.forum_posts
  with check ((((select auth.uid()) is null) and (user_id is null)) or (user_id = (select auth.uid())));

-- 3. Foreign keys with no covering index. Every one of these is a delete-time and
--    join-time scan today; "delete my data" walks exactly these paths.
create index if not exists forum_posts_user_id_idx   on public.forum_posts (user_id);
create index if not exists forum_threads_user_id_idx on public.forum_threads (user_id);
create index if not exists sessions_user_id_idx      on public.sessions (user_id);
