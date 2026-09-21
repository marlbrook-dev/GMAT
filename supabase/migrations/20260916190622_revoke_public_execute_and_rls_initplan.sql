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

revoke execute on function public.is_admin() from public;
grant  execute on function public.is_admin() to anon, authenticated;

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

create index if not exists forum_posts_user_id_idx   on public.forum_posts (user_id);
create index if not exists forum_threads_user_id_idx on public.forum_threads (user_id);
create index if not exists sessions_user_id_idx      on public.sessions (user_id);
