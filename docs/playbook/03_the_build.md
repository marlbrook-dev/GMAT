# The Build System

The build is the most valuable thing in the repository, and it is the part people skip.

## What it is

`python3 src/build.py` takes sources in `src/` and `data/` and writes every page of the
site. Nothing in the deployed output is hand-edited; the generated directories are
gitignored so there is no temptation. Sources of truth live in exactly one place, and the
build is the only thing that reads them.

The build currently produces five exam trainer applications, a landing page, a rankings
library of {{SCHOOL_FILES}} business schools and a separate college library, exam guide
pages, pricing, a blog, a forum shell, and the legal pages. It also produces this
document.

## Why a build rather than a framework

A framework gives you composition and gives up legibility. A build gives you a directory
of finished files you can open, diff, grep and serve from anything. At this scale that
trade is heavily in favour of the build, for a specific reason: **the output is
inspectable, so guards can run on the output.**

That turns out to be where most defects were caught. Not in the source, in the artefact.
Reading the built CSS rather than the template is what eventually found a nested comment
that had killed the palette on over a thousand pages. Reading the built page is what found
a stale count in a meta description that Google was showing.

## The guards, and what each one is for

Every one of these exists because of an incident. They are listed here in the order they
would catch a problem.

**Parse every generated script.** The build writes JavaScript into HTML. It runs node over
each inline script and refuses to write the page on a syntax error. One unescaped quote
inside a `onclick` string once took down the entire trainer, because a parse error kills
the whole script, not the one handler.

**Ban the characters you said you would ban.** Em dashes and en dashes fail the build in
any hand-edited document or item bank. It is a one-line check that makes a style rule
real.

**Assert the size of every collection.** Item counts per category, page counts, sitemap
entry counts, school counts. Not the contents, the size. Deletion by shadowing, a filter
dropping rows, a loop over an empty list: none of these raise anything, and all of them
show up instantly as a count that moved.

**Assert how many things you checked.** A guard that matched `\d{2,4}` silently stopped
checking the two largest item counts when they passed ten thousand, and kept passing. Any
guard that selects a subset should report the size of the subset it selected.

**Assert the platform's hard limits.** Cloudflare rejects a static asset over 25 MiB. The
build now fails on any asset over that, because a deploy-time rejection is an expensive
place to learn a number your build already knew.

**Compare inputs to outputs at every filter.** A length filter measuring the wrong unit
silently dropped sixteen valid items. Every stage that can reject should say how many it
rejected.

**Derive, never type.** Any number in copy that describes the size of something is
computed from that thing at build time. A typed number has a half-life.

## Reproducibility

Three consecutive builds must produce identical output. This is worth enforcing because
the failure is subtle: this project's item generator seeded from Python's `hash()`, which
is randomised per process, so every build produced a different bank and the pinned
statistics in the test file drifted run to run. It looked like a flaky test. It was a
broken promise. `zlib.crc32` fixed it.

If your build has any randomness, seed it from something stable and assert the
reproducibility, or you will eventually delete a test that was telling you the truth.

## The test ladder above the build

The build is the first rung. Above it, in the order they run:

{{TEST_LIST}}

{{TEST_FILES}} test files in total. The layering is deliberate:

1. **The build** catches structural problems in the artefact.
2. **Engine tests** run the domain logic headlessly, once per exam.
3. **Smoke tests** drive a real browser against the real built site at desktop and phone
   width, and assert behaviour rather than markup.
4. **Review bots** play the product adversarially and report what only use reveals.
5. **A weekly audit** re-checks contrast, links and metadata across every page.

Rung three is where the most valuable failures show up, and rung four is where the
embarrassing ones do.
