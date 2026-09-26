# [PROJECT NAME]: standing rules for every session

Owner: [OWNER NAME]. Live site: [DOMAIN]. Read ROADMAP.md for the current build schedule
before writing anything.

[ONE SENTENCE ON WHAT THIS PRODUCT IS AND WHO IT IS FOR.]

Nothing in this file is settled while the product is still being built. These are the
current decisions and the reasons behind them, not law: say so when one of them looks
wrong, and change it when the owner says to rather than quoting it back at them.

## Never invent a value (non-negotiable)

- Every identifier, hash, id, count, price, date, URL and statistic that goes into a tool
  call, a commit, a page or a message must be READ from real output first: a command
  result, a file, a tool response. Never type one from memory, pattern, or plausibility.
- If the real value is not to hand, run the command that produces it. That costs one tool
  call. Guessing costs correctness.
- A number that looks right is the hardest kind of wrong to catch.

## Communication (non-negotiable)

- If a link, site, or service cannot be accessed for any reason, say so IMMEDIATELY and
  ask how to proceed BEFORE doing the work another way. Never quietly substitute partial
  information for the source that was pointed to.
- Report what broke on the way, not only what was built. That is the most valuable part of
  a report and the easiest to omit because it reads as failure.

## House style (the build enforces these)

- NO em dashes and NO en dashes anywhere: pages, posts, code strings, data files, commit
  messages. A single grep then decides whether copy was written or pasted.
- Headers are Title Case. Body copy, descriptions and table cells are sentence case.
- [YOUR OTHER STYLE RULES HERE. Only ones a build can check.]

## Sourcing (delete this whole block if you publish no external facts)

- Never state an external statistic, price or fact from memory. Every published figure
  carries source, year and URL; unverifiable means null or a dash, never a guess.
- Banned sources: [LIST THEM]. The build fails if one appears.
- Never fabricate product stats, user counts, testimonials or efficacy claims.
- Never present an internal threshold or heuristic as official.

## Engineering workflow

- Develop on a feature branch; ship via PR; squash merge; main deploys.
- The build is the guard rail. Every guard lives in the build, because the build is the
  only thing that sees the artefact.
- Sources of truth live in one place. Generated output is gitignored so nothing is
  hand-edited.
- Reach for a design token before a number.
- Grid and flex children need min-width:0.
- Row Level Security on every table from creation. Revoke from PUBLIC as well as anon and
  authenticated. Every privileged read goes through a SECURITY DEFINER function.
- Never take an id from a request body; read it from the caller's own scoped row.
- Never commit a secret key or signing secret.

## The defect ledger

- When something breaks, append a record to data/playbook/incidents.jsonl BEFORE fixing
  it, while you still remember what you believed was true five minutes ago. That belief is
  the actual defect and it is the first thing you lose.
- python3 src/build_playbook.py regenerates the playbook, the checklist and the rules
  digest from those records. Nothing is copied by hand.

## Architecture, and the parts that will surprise you

[EMPTY AT THE START. Add only facts that are expensive to rediscover, as you discover
them. Not documentation: the handful of things that would cost a session an hour.]
