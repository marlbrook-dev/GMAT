# Supabase (Phase 3)

Project: `meridian-prep` (ref ftsqwbzhkzuudogkvoqa, us-east-1, Free plan) in marlbrook-dev's Org. URL https://ftsqwbzhkzuudogkvoqa.supabase.co. The app embeds the publishable key (safe for browsers; Row Level Security protects data).

Applied migration `meridian_prep_core`: profiles (state_blob jsonb, plan, consent_at, trigger auto-creates row on signup), attempts, events, sessions, RLS policies, `item_stats` view (per-question correct rate and median time for content review).

## One-time settings Hunter must do in the Supabase dashboard (Authentication > URL Configuration)
- Site URL: your Cloudflare Pages URL, e.g. https://gmat-xxxx.pages.dev/app/
- Redirect URLs: add https://gmat-xxxx.pages.dev/** (and your custom domain later)
Magic-link sign-in will not complete until this is set. Optional: Authentication > Providers > Google (needs a Google Cloud OAuth client).

## How sync works in the app
Anonymous use stores everything in localStorage. After sign-in, the app pulls `profiles.state_blob`; if the account has more answers than this device, the account wins (device copy stays until overwritten). Every answer also inserts a row into `attempts`, product events go to `events`, and the full state is upserted 2.5 s after each change. Delete my data wipes attempts, events, sessions and the blob.
