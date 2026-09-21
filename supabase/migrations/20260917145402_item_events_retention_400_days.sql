-- Retention for item telemetry, approved by the owner on 2026-09-17.
--
-- 400 days, matching the query window cap already enforced in admin_item_diagnostics, so
-- nothing the console can ask for is ever missing. The rows identify nobody, which is why
-- they need no consent; that is not a reason to keep them forever. An item's difficulty
-- and its distractor pattern are properties of the item, and a reading more than a year
-- old describes a bank that has since been edited.
--
-- Deliberately a function plus a schedule rather than a trigger: a delete on every insert
-- would put a scan in the path of answering a question.
create or replace function public.prune_item_events()
returns integer
language plpgsql
security definer
set search_path = public
as $$
declare
  removed integer;
begin
  delete from public.item_events where ts < now() - interval '400 days';
  get diagnostics removed = row_count;
  return removed;
end;
$$;

revoke all on function public.prune_item_events() from public, anon, authenticated;

comment on function public.prune_item_events() is
  'Deletes item_events rows older than 400 days. Owner-approved retention, 2026-09-17. Run daily by the pg_cron job item_events_retention.';

comment on table public.item_events is
  'Unlinkable item telemetry: which item was answered, which option was chosen, whether it was correct, how long it took, and the learner''s own guess and miss-reason tags. Carries no user, session, device or address column BY DESIGN, and must never gain one: that absence is why it needs no consent gate. Retained 400 days (prune_item_events).';
