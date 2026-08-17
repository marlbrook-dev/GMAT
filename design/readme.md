# Start From Nowhere — Design System

Design system for **Start From Nowhere** (name invented at the user's request), an adaptive GMAT prep product: short game-like study rounds (quizzes, timed sprints, flashcards, mock sections) driven by an AI learner model. The brand is professional and institutional — the go-to, trusted resource — while staying easy to read. Confident and adaptive in voice, never arrogant. **Positioning: a hybrid of a serious test-prep company and Quizlet** — institutional trust signals (serif, navy, guarantee, evidence) around light, game-like study mechanics (flashcard sets, quick rounds, AI-generated practice).

**Sources:** none provided. Authored from the company description plus user picks (name, navy+gold palette, rising-path logo, serif+sans type). Surfaces: web app, marketing website, slide deck, email. The platform is multi-exam (GMAT first; GRE, LSAT, MCAT, Executive Assessment planned) — every experience keys off the exam chosen at onboarding.

## Content fundamentals

- **Voice:** confident, considered coach. Second person ("You're on pace"). Claims are specific and evidenced ("+72 average improvement, n = 1,140"), never boastful. AI framed as attentiveness: "a plan that studies you back", not "revolutionary AI".
- **Casing:** sentence case everywhere; all-caps only for tiny letterspaced labels (11–12px).
- **Copy shape:** short declaratives; fact first, nudge second. Explanations start with "Why:".
- **Numbers:** concrete and mono-set (645, 78%, 1:52).
- **Emoji:** never. Legal: always include the GMAC trademark disclaimer on public surfaces.

## Visual foundations

- **Color:** deep navy primary (`--brand-primary` #122B4E), brass gold accent (#C7A252, text-safe #A8842F) reserved for emphasis moments — badges, dividers, the CTA on navy. Cool-gray neutrals on `--gray-50`. Section hues: blue = Quant, violet = Verbal, teal = Data Insights. Status: green/red/amber/blue with 50-tint backgrounds. Green is status-only, never brand.
- **Type:** Source Serif 4 (600/700) for headlines h1–h3; Manrope (700/800) for UI — buttons, tabs, card titles, labels; IBM Plex Sans (400–600) body; IBM Plex Mono for timers, scores, slide numbers.
- **Cards:** white, 1px border, 10px radius, low navy-tinted shadow; hover lifts to `--shadow-md`. Crisp radii 6/8/10px; pills for badges/tracks/switches only.
- **Motion:** 120–200ms ease-out; color/shadow/width fades only. Hover darkens, press scale(.97), focus 3px navy ring.
- **Dark surfaces:** navy-800/900 blocks for hero score cards, CTA bands, title slides — gold type/rule as the counterpoint.
- **Backgrounds:** flat solids; no gradients, textures, or imagery. Blur only on the sticky website nav; scrim only under dialogs.

## Logo & iconography

- **Logo:** `assets/logo.svg` (navy tile, gold path rising from an origin dot — "from nowhere, upward") and `assets/logo-inverse.svg` for dark surfaces. Wordmark: "Start From Nowhere" in Source Serif 4 700, "Prep" in gold-600 (gold-500 on navy). An original mark designed here — vector only.
- **Icons:** minimal functional strokes (chevron, check, ×) at 2–3.5px round caps. Recommendation: Lucide via CDN for product icons (flagged substitution). No emoji.

## Design constraints (for anyone — human or agent — building with this system)

- **Spacing:** use `--space-*` tokens only; never arbitrary pixel values. 16px (`--space-4`) grid gaps, 24px (`--space-6`) card padding by default.
- **Type hierarchy is semantic:** page/hero heading → Source Serif 4 700; card/section title → Manrope 700–800; body → IBM Plex Sans 400; label/caps → IBM Plex Sans 600 at 11–12px letterspaced; any number a user watches (score, timer, count) → IBM Plex Mono.
- **State contract:** every interactive element has explicit hover (darken or gray tint), active (scale .97), and focus-visible (`--focus-ring`, 3px navy) treatments, transitioning at `--duration-fast` with `--ease-out`. No interactive element ships without all three.
- **Color discipline:** navy acts, gold accents (sparingly), green/red mean correct/incorrect only, section hues never mix with status hues.
- Stacking: z-index only from the scale --z-sticky 20 / --z-dropdown 40 / --z-modal 100 / --z-toast 110; layered components use isolation:isolate.
- Async surfaces ship designed loading/empty/error states (guidelines/states.html); reduced-motion users get a working reduced experience (wired globally).
- Craft rules: guidelines/ux-craft.md · AI UX patterns: guidelines/ai-ux.md · Analytics event schema: guidelines/data-analytics.md · SEO content strategy: guidelines/seo-content.md
- Compose the exported components (`window.GMATStudyGuideDesignSystem_efe656`) rather than re-implementing them; props contracts live in each `.d.ts`.

## Intentional additions

No component source existed; standard set authored plus product primitives: `ProgressBar`, `QuizOption`, `StatTile`.

## Index

- `styles.css` → `tokens/` (colors, typography, spacing, effects, fonts, base).
- `assets/` — logo.svg, logo-inverse.svg.
- `guidelines/` — 14 specimen cards (Colors, Type, Spacing, Brand) + ux-craft.md and ai-ux.md rulebooks.
- `components/` — forms (Button, IconButton, Input, Select, Checkbox, Radio, Switch), display (Card, Badge, Tag, Tooltip), navigation (Tabs, Dropdown), feedback (Dialog, Toast, ProgressBar), study (QuizOption, StatTile, Flashcard).
- `ui_kits/web_app/` — interactive Dashboard → Practice → Results + Account page, signup wizard (account + plan steps), and an owner-only Admin view (User/Owner toggle).
- `ui_kits/website/` — marketing homepage, blog ("The Study Room", with reader-submission form), Terms of Use page.
- `templates/slide-deck/`, `templates/email/` — branded deck and email starting points.
- `SKILL.md` — agent skill entry point.

Fonts load from Google Fonts CDN (Source Serif 4, Manrope, IBM Plex Sans/Mono); swap in licensed binaries via `tokens/fonts.css` if acquired.
