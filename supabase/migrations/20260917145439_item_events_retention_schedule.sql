-- A retention function nobody runs is not retention, it is a comment. Schedule it.
create extension if not exists pg_cron with schema pg_catalog;

-- Idempotent: unschedule any earlier copy before scheduling, so re-running the migration
-- does not leave two jobs deleting the same rows.
do $$
begin
  perform cron.unschedule('item_events_retention');
exception when others then
  null;
end;
$$;

select cron.schedule('item_events_retention', '17 3 * * *',
                     $$select public.prune_item_events();$$);
