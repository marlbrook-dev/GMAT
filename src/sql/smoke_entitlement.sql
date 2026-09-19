-- Entitlement resolution across two payment sources. Paste into the Supabase SQL editor
-- or run through execute_sql. Always ends by raising, which rolls the whole block back:
-- results arrive in the error message and nothing synthetic survives.
--
-- The case that matters most is the last one. Somebody who subscribed on both platforms
-- must get the higher tier AND be told they are paying twice, because the alternative is
-- taking two payments and saying nothing.
do $$
declare
  u uuid[] := array['00000000-0000-4000-8000-0000000000e1','00000000-0000-4000-8000-0000000000e2',
                    '00000000-0000-4000-8000-0000000000e3','00000000-0000-4000-8000-0000000000e4',
                    '00000000-0000-4000-8000-0000000000e5','00000000-0000-4000-8000-0000000000e6',
                    '00000000-0000-4000-8000-0000000000e7','00000000-0000-4000-8000-0000000000e8'];
  r text := E'\n'; ok boolean := true; g record;
begin
  insert into auth.users (id, instance_id, aud, role, email, encrypted_password,
                          email_confirmed_at, created_at, updated_at)
  select x, '00000000-0000-0000-0000-000000000000', 'authenticated', 'authenticated',
         'ent-' || x || '@example.invalid', '', now(), now(), now() from unnest(u) x;
  insert into public.profiles (id, email) select x, 'x@example.invalid' from unnest(u) x
    on conflict (id) do nothing;

  update public.profiles set plan='plus', plan_status='active',  current_period_end=now()+interval '20 days' where id=u[2];
  update public.profiles set plan='pro',  plan_status='past_due',current_period_end=now()+interval '5 days'  where id=u[3];
  update public.profiles set plan='pro',  plan_status='canceled',current_period_end=now()-interval '1 day'   where id=u[4];

  insert into public.apple_subscriptions (original_transaction_id,user_id,product_id,tier,status,expires_at,environment) values
   ('T5',u[5],'sfn.pro.monthly','pro','active', now()+interval '25 days','Production'),
   ('T6',u[6],'sfn.plus.monthly','plus','grace', now()+interval '3 days','Production'),
   ('T7',u[7],'sfn.pro.monthly','pro','expired',now()-interval '2 days','Production'),
   ('T8',u[8],'sfn.pro.monthly','pro','active', now()+interval '10 days','Production'),
   ('T9',u[7],'sfn.plus.monthly','plus','refunded',now()+interval '30 days','Production');
  update public.profiles set plan='plus', plan_status='active', current_period_end=now()+interval '15 days' where id=u[8];

  for i in 1..8 loop
    select * into g from public.entitlement(u[i]);
    r := r || format(E'  e%s -> plan=%-5s source=%-6s managed_by=%-6s double_billed=%s\n',
                     i, g.plan, g.source, g.managed_by, g.double_billed);
  end loop;

  select * into g from public.entitlement(u[1]);
  if g.plan <> 'free' then ok:=false; r:=r||E'  FAIL e1 no payment should be free\n'; end if;
  select * into g from public.entitlement(u[2]);
  if g.plan <> 'plus' or g.source <> 'stripe' then ok:=false; r:=r||E'  FAIL e2 stripe plus\n'; end if;
  select * into g from public.entitlement(u[3]);
  if g.plan <> 'pro' then ok:=false; r:=r||E'  FAIL e3 past_due must keep access\n'; end if;
  select * into g from public.entitlement(u[4]);
  if g.plan <> 'free' then ok:=false; r:=r||E'  FAIL e4 cancelled must not\n'; end if;
  select * into g from public.entitlement(u[5]);
  if g.plan <> 'pro' or g.managed_by <> 'apple' then ok:=false; r:=r||E'  FAIL e5 apple pro\n'; end if;
  select * into g from public.entitlement(u[6]);
  if g.plan <> 'plus' then ok:=false; r:=r||E'  FAIL e6 grace must keep access\n'; end if;
  select * into g from public.entitlement(u[7]);
  if g.plan <> 'free' then ok:=false; r:=r||E'  FAIL e7 expired and refunded must be free\n'; end if;
  select * into g from public.entitlement(u[8]);
  if g.plan <> 'pro' or g.source <> 'apple' or not g.double_billed then
    ok:=false; r:=r||E'  FAIL e8 higher tier wins and double billing is flagged\n'; end if;

  r := r || format(E'\n%s\n', case when ok then 'ENTITLEMENT RESOLUTION HOLDS'
                                   else 'SOMETHING FAILED, READ THE LINES ABOVE' end);
  raise exception 'RESULTS (rolled back): %', r;
end $$;
