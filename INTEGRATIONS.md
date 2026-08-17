# Integrations plan (Meridian Prep)

| Need | Service | When | Notes |
|---|---|---|---|
| Hosting | Cloudflare Pages (Git connect to this repo) | Now | Root = landing page, `/app/` = trainer. Free custom domain. |
| Accounts + progress sync | Supabase (Auth magic link + Postgres, RLS) | LIVE (project meridian-prep, see supabase/README.md) | Wired in app: sign-in on Account tab, state sync, attempts + events tables. Needs Site URL / Redirect URL set once in Supabase Auth settings. |
| Payments | Stripe Checkout + Customer Portal, webhook to a Cloudflare Worker or Supabase Edge Function that sets `profiles.plan` | Phase 3 (with accounts) | Never handle card data in the app; Stripe-hosted checkout only. Add Stripe MCP/connector in Claude when ready. |
| Analytics | Cloudflare Web Analytics (cookie-free) now; Google Analytics 4 later if marketing needs it | Now / later | GA4 requires a consent banner in EU; Cloudflare's does not. |
| Sign in with Google | Supabase Auth Google provider | Phase 3 | One toggle in Supabase once a Google Cloud OAuth client exists. |
| Email (digest, magic links) | Supabase built-in for auth mail; Resend or Postmark for the weekly digest | Phase 3 | Design template: `design/templates/email/Email.dc.html`. |
| AI generation / coaching | Anthropic API from a Cloudflare Worker or Supabase Edge Function (key server-side) | Phase 3 | Generated items must be tagged and reviewed before entering the bank. |
| Search visibility | robots.txt currently blocks indexing; flip when public | Launch | Add sitemap.xml and Open Graph tags on the landing page. |
| Legal | Privacy policy, terms, GMAC trademark disclaimer (present) | Before payments | Stripe requires visible terms and refund policy. |

Claude connectors worth adding for this project: Supabase (connected), Cloudflare (connected), Stripe (when payments start), Google Analytics or Search Console (later), Resend/Postmark (later). GitHub is attached per session in Claude Code on the web.
