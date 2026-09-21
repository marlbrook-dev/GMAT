-- The open item in DATA_COLLECTION.md: item_events got a 400 day period because the
-- owner decided one, and the two tables that actually DO identify people, site_events
-- and client_errors, had none at all. Both carry a session id and a salted address
-- hash, so "we keep it until we think of something" is the weakest position of the
-- three and the only one a regulator would ask about first.
--
-- site_events: 400 days, matching item_events. Admissions is seasonal, so a full
-- application cycle plus the same month a year earlier is the shortest window in
-- which a traffic comparison means anything. Beyond that the rows describe a site
-- that no longer exists.
--
-- client_errors: 90 days. An error report names a build version, and a stack trace
-- from a build nobody is running is not evidence of anything. Admin > Errors triages
-- them in days, not seasons.
create or replace function public.prune_site_events()
returns integer
language plpgsql
security definer
set search_path = public
as $$
declare
  removed integer;
begin
  delete from public.site_events where ts < now() - interval '400 days';
  get diagnostics removed = row_count;
  return removed;
end;
$$;

create or replace function public.prune_client_errors()
returns integer
language plpgsql
security definer
set search_path = public
as $$
declare
  removed integer;
begin
  delete from public.client_errors where ts < now() - interval '90 days';
  get diagnostics removed = row_count;
  return removed;
end;
$$;

-- Nobody but the scheduler needs to call these.
revoke all on function public.prune_site_events() from public, anon, authenticated;
revoke all on function public.prune_client_errors() from public, anon, authenticated;

-- Staggered off item_events (03:17) so three deletes do not contend for the same
-- minute, and off each other.
select cron.unschedule('site_events_retention')
  where exists (select 1 from cron.job where jobname = 'site_events_retention');
select cron.schedule('site_events_retention', '29 3 * * *',
                     $j$select public.prune_site_events();$j$);

select cron.unschedule('client_errors_retention')
  where exists (select 1 from cron.job where jobname = 'client_errors_retention');
select cron.schedule('client_errors_retention', '41 3 * * *',
                     $j$select public.prune_client_errors();$j$);
