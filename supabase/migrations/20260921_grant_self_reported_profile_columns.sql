-- Applied 2026-09-21. Twelve self-reported fields on the Account page could be read back
-- but never written.
--
-- Two layers of authorisation guard this table and they had drifted apart. Row Level
-- Security scopes every write to the caller's own row (policy "own profile", USING and
-- WITH CHECK both auth.uid() = id). A separate column grant then decides which columns
-- any role may write at all, and that second layer is the one that stops a signed-in
-- browser setting its own plan to Pro. It was covering 5 of the 17 self-reported fields.
--
-- The page updated the other 12 anyway, the database refused, and the client swallowed
-- the refusal, so the user was told "Saved." every time. The data lived in that browser
-- and nowhere else. Recorded as INC-0056 in data/playbook/incidents.jsonl.
--
-- What is granted here is exactly the set a person declares about themselves. Nothing
-- derived and nothing the server owns: plan, plan_status, the Stripe columns, age_tier,
-- the data sharing columns, target_schools, marketing_opt_in and signup_country all stay
-- out, and the row policy means even these can only ever be written to the caller's own
-- row.
--
-- birth_month and birth_year are included deliberately. They feed age_tier through a
-- trigger, and age_tier itself is NOT granted, so a person can state their birth date,
-- exactly as they do at signup, and cannot set the tier the site derives from it. Being
-- unable to correct a birth date after signup is its own problem, and a privacy one.
--
-- Drift in either direction is now caught by src/sql/smoke_profile_grants.sql, which
-- asserts that every field the Account page offers is writable and that every
-- server-owned field is not. Verified by running it against a deliberately wrong list
-- and watching it raise.

grant update (
  education_level,
  intended_major,
  score_goal,
  application_year,
  budget_band,
  employer_industry,
  household_income_band,
  first_generation,
  military_status,
  study_hours_band,
  birth_month,
  birth_year
) on public.profiles to authenticated;

-- anon is deliberately NOT granted any of these. A profile row belongs to an account, and
-- an anonymous session has no row of its own to write to; the local copy in the browser is
-- the right home for its answers until it signs in.
