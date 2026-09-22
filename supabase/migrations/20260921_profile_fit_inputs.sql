-- Applied 2026-09-21. Three self-reported fields that let a shortlist become a fit view.
--
-- The rankings library already carries, for each school and with a source and a year on
-- every figure, what its admitted class looked like: average GPA, average years of work
-- experience, tuition. A student can read those. What they cannot do is see their own
-- numbers beside them, which is the whole point of keeping a shortlist.
--
-- These three are self-reported and belong to the person, so they are granted to
-- authenticated exactly as the other declared fields are, and they are covered by the
-- same drift guard (src/sql/smoke_profile_grants.sql), which exists because twelve such
-- fields were silently unwritable until INC-0056.
--
-- What is NOT here, deliberately: any derived score, any admission probability, any
-- composite. The comparison is computed in the page from published figures at the moment
-- it is shown, so it can never be stored, exported, or mistaken for a prediction.
-- CLAUDE.md: honest fit banding, never fake probabilities.
--
-- gpa is numeric rather than a float because a GPA is a reported figure with two
-- decimals, not a measurement, and because 3.70 must not come back as 3.6999999. The
-- check allows up to 4.30, since some transcripts carry an A-plus scale; any other scale
-- is out of scope rather than silently rescaled.

alter table public.profiles
  add column if not exists gpa                numeric(4,2),
  add column if not exists work_exp_years     smallint,
  add column if not exists tuition_budget_usd integer;

alter table public.profiles
  drop constraint if exists profiles_gpa_range,
  add  constraint profiles_gpa_range
       check (gpa is null or (gpa >= 0 and gpa <= 4.30));

alter table public.profiles
  drop constraint if exists profiles_work_exp_range,
  add  constraint profiles_work_exp_range
       check (work_exp_years is null or (work_exp_years >= 0 and work_exp_years <= 60));

alter table public.profiles
  drop constraint if exists profiles_tuition_budget_range,
  add  constraint profiles_tuition_budget_range
       check (tuition_budget_usd is null or (tuition_budget_usd >= 0 and tuition_budget_usd <= 1000000));

comment on column public.profiles.gpa is
  'Self-reported undergraduate GPA on a 4.0 scale, as the person states it. Never inferred, never rescaled from another scale.';
comment on column public.profiles.work_exp_years is
  'Self-reported full-time work experience in years at the point of application.';
comment on column public.profiles.tuition_budget_usd is
  'Self-reported total the person can put toward tuition. Compared against published tuition only; it is not a cost-of-attendance model.';

grant update (gpa, work_exp_years, tuition_budget_usd) on public.profiles to authenticated;
