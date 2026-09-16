-- APPLIED to the live project on 2026-09-16 (migration
-- `harden_plan_column_and_rpc_surface`). Recorded here so the repo is the record.
--
-- 1. THE PAYMENT BYPASS. profiles had a single "own profile" policy, FOR ALL with
--    USING/WITH CHECK (auth.uid() = id), and table-level UPDATE granted to
--    authenticated. RLS is row-level, not column-level, so any signed-in user could run
--        update profiles set plan='pro' where id = auth.uid()
--    from the browser console and grant themselves Pro forever. The client never writes
--    plan; only the Stripe webhook does, via the service role, which bypasses both RLS
--    and column grants. So plan must not be writable by API roles at all.
revoke update on public.profiles from anon, authenticated;
grant update (id, email, state_blob, display_name, test_date, daily_goal, exam,
              consent_at, age_range, gender, country, role_type, referral_src, updated_at)
  on public.profiles to anon, authenticated;

revoke insert on public.profiles from anon, authenticated;
grant insert (id, email, state_blob, display_name, test_date, daily_goal, exam,
              consent_at, age_range, gender, country, role_type, referral_src, updated_at)
  on public.profiles to anon, authenticated;

-- 2. Trigger functions were callable as RPCs. They are SECURITY DEFINER and exist only
--    to fire on their tables; direct invocation is never legitimate. Revoking API
--    EXECUTE does not affect trigger firing.
revoke execute on function public.handle_new_user() from anon, authenticated;
revoke execute on function public.site_events_before() from anon, authenticated;
revoke execute on function public.forum_post_before() from anon, authenticated;
revoke execute on function public.forum_after_post() from anon, authenticated;
revoke execute on function public.forum_thread_before() from anon, authenticated;

-- 3. Admin RPCs already raise 'admin only' for non-admins, so this is defence in depth:
--    it removes the call surface and the error-based probing it allows. authenticated
--    keeps EXECUTE because a signed-in admin calls them; is_admin() stays callable so
--    the app can ask cheaply whether to show the Admin tab.
revoke execute on function public.admin_bi() from anon;
revoke execute on function public.admin_users(text, integer, text, integer) from anon;
revoke execute on function public.admin_user_detail(uuid) from anon;
revoke execute on function public.admin_traffic(integer) from anon;
revoke execute on function public.admin_mod_queue() from anon;
revoke execute on function public.admin_moderate(text, bigint, text) from anon;

-- 4. Pin search_path on the remaining helpers; everything else already set it.
alter function public.req_header(text) set search_path = public;
alter function public.req_ip_hash() set search_path = public;
alter function public.forum_screen(text) set search_path = public;

-- 5. item_stats is an internal content-review view that nothing in the app reads. It
--    was a SECURITY DEFINER view readable by API roles, leaking item analytics.
revoke select on public.item_stats from anon, authenticated;
