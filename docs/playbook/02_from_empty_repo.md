# From an Empty Repository to a Live Site

The order below is the one that worked, and the order matters more than any individual
step. Most of what went wrong in this build went wrong because something was done before
the thing that would have caught it.

## Phase 0: the rules file, before any code

Write the project's standing rules into a file the AI session reads on every turn. On this
project that is `CLAUDE.md`, {{MD_FILES}} documents in, and it is still the highest
leverage file in the repository.

It is not documentation. It is the constitution, and it should contain only things that
are load-bearing and that you would otherwise have to say again:

- The house style rules that a build can enforce. Ours bans em dashes and en dashes
  outright, everywhere, including commit messages. That sounds trivial. It means a
  single grep decides whether copy was written by hand or pasted from somewhere, and the
  build fails on a violation.
- The sourcing rules. Ours: never state a statistic, price or external fact from memory;
  every published figure carries a source, a year and a URL; unverifiable means null, never
  a guess; and a named list of banned sources.
- **Never invent a value.** Every identifier, hash, id, count, price, date and URL that
  goes into a tool call, a commit or a page must be read from real output first. This rule
  exists on this project because a forty-character hex string was once typed straight into
  a merge call as though it were a commit SHA. The API rejected it as malformed, which was
  luck. A well-formed guess would have merged something else.
- The communication rule. Ours: if a link or a service cannot be reached, say so
  immediately and ask, before doing the work another way. Never quietly substitute a
  screenshot or a memory for the source that was pointed to.

Every one of those was written after something went wrong. Start with them anyway.

## Phase 1: the build, before the content

Write the thing that turns sources into pages before you have many pages. Ours is
`src/build.py`, and on day one it did almost nothing. What matters is that it exists, so
that every guard you later need has somewhere to live.

By the end it does all of this, and each item was added the day it was needed:

- Injects shared header, footer and CSS into every page from one place
- Parses every inline script with node and fails on a syntax error
- Fails on an em or en dash in any hand-edited document or item bank
- Fails on any asset larger than the platform's per-file limit
- Counts what it produced and asserts the counts agree across artefacts
- Writes the sitemap from the same directory scan that writes the pages

None of these are clever. All of them exist because of an entry in the defect ledger.

## Phase 2: one page, deployed, for real

Deploy the simplest possible page to the real domain before building anything else. Not a
staging environment: the actual production host, on the actual domain, through the actual
pipeline.

Everything you learn here is cheap now and expensive later. The per-file size limit. Which
directories the asset uploader walks. Whether your headers file applies to responses your
own code generates. Whether `www` and the apex are the same origin. That last one cost
this project a split consent state and a diluted ranking signal, and it is ten lines of
redirect in the right place.

## Phase 3: the data layer, with the guarantees tested

Before the interface, get the database right, because it is the thing you cannot casually
change later.

1. Every table has Row Level Security enabled, from creation. Not later.
2. A table with no policy denies everyone, which is the correct default for anything only
   your server should touch.
3. Every privileged read goes through a `SECURITY DEFINER` function that checks admin
   membership. Clients never read a privileged table directly.
4. Revoke from `PUBLIC` as well as from `anon` and `authenticated`. Revoking from the roles
   you can name leaves `PUBLIC` holding the grant, and it will not show up in the place you
   think to look.
5. Test the guarantee, not the code. Write a SQL smoke test that asserts what must be true
   and rolls itself back. Two trigger bugs on this project were found exactly that way and
   would not have been found by reading.

## Phase 4: the interface system, before the interfaces

One file that defines the type scale, the tracking ramp, the spacing grid, one page width,
one gutter and one reading measure, injected everywhere. On this project that is
`src/partials.py`, currently {{TOKEN_COUNT}} tokens.

The reason to do this early is arithmetic. This site reached thirty-seven font sizes,
twenty-eight spacing values and eight page widths before the system landed, and pulling
them back to one scale was a multi-day job that touched everything. Doing it on day one
costs an hour.

## Phase 5: the product

Now build the thing. By this point the build catches syntax errors, the database refuses
unauthorised reads, the type system stops the interface drifting, and you can deploy.

## Phase 6: instrumentation, before growth

Before spending anything on acquisition, be able to answer: how many people arrive, what
they do, where they stop. That is the beacon, the funnel and the error queue. All three
are small. All three are useless retroactively, which is the entire argument for doing
them before you need them.

## Phase 7: payments

Last, and only when there is something worth paying for. The payments chapter has the
details. The one scheduling note: the event ledger that lets you answer "how much revenue
arrived and how much left" has to exist **before** the first real subscriber, because it
cannot be reconstructed afterwards from a table you overwrite on every webhook. This
project learned that in the right order by luck rather than judgement.

## The shape of the whole thing

Read backwards, the order is: make failure loud, make authorisation impossible to bypass,
make the interface consistent, then build features, then measure, then charge. Each phase
makes the next one cheaper to get wrong.
