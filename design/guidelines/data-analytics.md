# Data & analytics — event schema

Data collection powers the adaptive engine and the owner's command center. Principles: consent is collected once at signup (Terms + Privacy checkbox); collection is silent in the user's experience — no cookie-nag re-prompts, no "we're tracking you" chrome; the user's visible touchpoints are exactly two: the reassurance line at signup and the Privacy & data card on the Account page (download / delete).

## Event taxonomy

Identity: `account_created {exam, source}`, `wizard_completed {exam, goal_text, hours, tools}`, `plan_selected {plan, trial}`, `account_deleted {reason?}`.
Study loop: `round_started {exam, mode}`, `question_answered {qid, section, tag, correct, secs, skipped}`, `round_completed {exam, mode, correct, total, secs}`, `flashcard_flipped {deck, card}`.
Engagement: `session_started {platform}`, `streak_extended {days}`, `assist_prompt {text_len, accepted_suggestion}`.
Commerce: `checkout_started {plan}`, `payment_completed {plan, amount}`, `plan_cancelled {reason?}`.

Every event carries: `user_id, exam, timestamp, platform, app_version`. Question-level data is the crown jewel — per-question correct rates, timing distributions, and discrimination feed both the adaptive engine and content quality review (surfaced in the Question bank table of the owner view).

## Storage & governance

- Raw events append-only; aggregates (mastery, score estimate) recomputed per round.
- PII (name, email) stored separately from the event stream; events reference `user_id` only.
- Retention: raw events 24 months, aggregates for account lifetime; both purged within 30 days of account deletion.
- Export = the user's full event history + aggregates as JSON (Account → Download my data).

## Owner view

`ui_kits/web_app/Admin.jsx` — funnel metrics, live event stream, site settings (feature flags, banner copy, pricing), and question-bank management. Toggle User/Owner in the app header. Never linked from user-facing navigation.
