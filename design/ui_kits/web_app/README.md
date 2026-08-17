# Study Web App UI kit

Interactive click-through of the core product loop: Dashboard → Practice round → Results.

- `index.html` — entry; loads the compiled component bundle and the three screens.
- `AppShell.jsx` — top nav bar (wordmark, nav pills, streak badge, avatar).
- `Dashboard.jsx` — stats row, section mastery, today's plan, game grid.
- `Practice.jsx` — adaptive question flow with select → submit → reveal → next.
- `Results.jsx` — round summary and question review.
- `Account.jsx` — profile, program, plan & billing, notifications, privacy & data (download/delete).
- `Admin.jsx` — owner-only command center: metrics, live event stream, site settings, question bank. Toggle User/Owner in the header.
- `Onboarding.jsx` — 4-step new-program wizard (multi-exam: GMAT, GRE, LSAT, MCAT, EA) with predictive goal suggestions, recommended tools, account creation (Terms/Privacy consent), and plan selection; open via "New program".

All screens compose the design-system primitives (`Button`, `Card`, `QuizOption`, `StatTile`, `ProgressBar`, `Badge`, `Tabs`); no re-implemented components. This is a from-scratch design (no source product existed), so it defines rather than recreates the product look.
