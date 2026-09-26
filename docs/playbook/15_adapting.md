# Adapting This to a Different Business

Most of this book is about a test-preparation platform. This chapter separates what was
specific to that from what was structural, so you know what to keep.

## What was specific

The item response theory, the exam registries, the score bands, the school library, the
concordance between two editions of one exam. If you are not building an assessment
product, none of it applies directly.

## What was structural, and transfers unchanged

**The infrastructure.** Edge-hosted static pages, managed Postgres with Row Level
Security, serverless functions, hosted checkout. Under thirty dollars a month, and it
serves a hundred thousand generated items and fifteen hundred generated pages.

**The build as the guard rail.** Sources in, pages out, and every guard living in the
build because the build is the only thing that sees the artefact.

**Authorisation in the database.** RLS everywhere, privileged reads behind definer
functions, revoke from `PUBLIC`, never take an id from a request body.

**The event-ledger pattern.** Any external system that sends you events sends them out of
order, more than once, and sometimes twice under different names. Never write the payload;
re-read state. Put idempotency in a unique index. Keep an append-only record of facts
alongside whatever current-state row you maintain, because current state is destroyed on
every update.

**The honesty discipline.** Every published figure carries a source, a year and a URL.
Unverifiable is null, never a guess. Never present an internal threshold as official.
Never show a number about a person without its error bar. Decline to compute a metric you
cannot compute honestly, and say why on the page.

**The interface system.** One token file, three typefaces, negative tracking on headings,
`min-width: 0` on every grid and flex child, a complete palette on bare `:root` with only
overrides in the theme blocks, colours in charts validated under simulated colour vision
deficiency rather than chosen.

**The test ladder and its failure modes.** Every one of the five ways a test can be
silently wrong applies to any codebase.

**The defect ledger itself.** The single most transferable artefact in this repository is
`data/playbook/incidents.jsonl` and the script that turns it into this book.

## The substitution table

| This project | Yours | Keep |
| --- | --- | --- |
| Item bank generators | Whatever your content is | Dedup keys canonical under every legitimate transformation; counts reported per stage; filters report rejections |
| Exam registry | Any multi-tenant or multi-variant dimension | Resolve differences from data, never from `if (x === 'a')`, which treats "not a" as "the original" |
| Ability estimation | Any inferred number about a user | A range not a point, a floor on the interval, a minimum evidence threshold, the method published |
| School library | Any library of external facts | One file per entity, source and year and URL on every figure, banned-source list enforced at build time |
| Two exam editions | Any legacy unit beside a current one | Never convert, compare on a common normalised measure, cite the concordance |
| Stripe plus Apple | Any two sources of one truth | Leave the first alone, add a derivation on top, move readers to the derivation |
| Forum moderation | Any user-generated content | Automatic screen flags, a human decides, the decision is stored and mutes permanently |

## The first week, for something new

1. Write the rules file. Use the template in the bootstrap pack and fill in the four
   blanks.
2. Create the repository, the build script, and one page. Deploy that page to the real
   domain.
3. Learn the platform's limits now: per-file size, which directories the uploader walks,
   whether `www` and the apex are one origin, whether your headers file applies to
   responses your own code generates.
4. Stand up the database with RLS on every table from creation, and write one SQL smoke
   test that asserts a guarantee and rolls itself back.
5. Write the token file. All of it, both themes, before the second page exists.
6. Then build the product.

## The one paragraph version

Make failure loud before you make anything else. Put every guarantee in the layer that
cannot be bypassed: the database for authorisation, the build for correctness of the
artefact, a pinned number for anything statistical. Never write a figure you cannot
regenerate. Never show a number you cannot defend. When something breaks, write down what
you believed five minutes earlier, because that belief is the actual defect and it is the
first thing you will lose.
