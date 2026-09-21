# Running the Build as an AI Loop

{{COMMITS}} commits in {{ELAPSED_DAYS}} days, one owner, a series of AI sessions. This
chapter is how that was actually run, including the parts that did not work.

## The division of labour

**The owner decides**: what to build, what it means, what is acceptable, and every
irreversible or outward-facing action. **The session does**: the building, the
measuring, the testing, and the reporting of what it found.

The failure mode at each end is worth naming. An owner who reviews every line becomes the
bottleneck and the throughput collapses to the speed of reading. A session that decides
product questions on its own produces something coherent that is not what anyone wanted.

## The rules file is the highest-leverage artefact

One file, read every turn, holding only load-bearing rules. Not documentation, not
architecture notes. The test for whether a line belongs in it: **would you otherwise have
to say this again?**

What earns a place:

- Style rules a build can enforce.
- Sourcing rules, with a named list of banned sources.
- **Never invent a value.** Every id, hash, count, price, date and URL must be read from
  real output before it goes into a tool call, a commit or a page.
- **Report a blocked resource immediately** and ask, rather than quietly working around it.
- The handful of architectural facts that are expensive to rediscover.

Every one of these was written after something went wrong. Write them at the start
anyway; the list above is transferable as-is.

## Ratchets, not reviews

The owner cannot read every line. So the correctness that matters is encoded in things
that fail loudly: build guards, pinned statistics, browser suites, review bots. The review
budget then goes to the few decisions that are genuinely judgement, rather than being
spread thinly over everything.

This is the same principle as the data layer. **Push the guarantee down to the layer that
cannot be bypassed.**

## What a session should report

Not a list of files changed. The useful report is:

1. What was built, in one paragraph.
2. **What broke on the way, and why.** This is the most valuable part and the easiest to
   omit, because it reads as failure. It is the opposite.
3. What is now guarded against, and where.
4. What was left undone, and whether that is a decision or a blocker.
5. Numbers, with the command that produced them.

The commit messages in this repository are written that way, which is why a defect ledger
could be reconstructed from them {{ELAPSED_DAYS}} days later. **Write the commit message
as though someone will need to mine it. Someone will.**

## Failure modes observed in this project

**Reporting a regression from one seed.** A stochastic measurement compared before and
after on a single seed showed an 88 to 72 percent drop. Across three seeds the spread
between seeds was larger than the effect. Run more seeds before reporting.

**Pausing to report when told to keep working.** A session that stops to summarise every
few minutes converts working time into reading time. If the owner has said to keep going,
keep going, and batch the reporting.

**Treating a policy document as a blocker.** A missing stylesheet reference was reported
as a privacy concern because the file lived in a directory named after the privacy page.
Be precise about what kind of problem you have found; a 404 is a 404.

**Typing a value that looked right.** A forty-character hex string was typed into a merge
call as though it were a commit SHA. It was rejected as malformed, which was luck; a
well-formed guess would have merged the wrong thing. `git rev-parse` costs one call.

**Adding a guard that did not guard.** Several ledger entries are guards that were too
narrow, too broad, or measuring the wrong thing. After writing a guard, break the thing on
purpose and confirm the guard fails.

## The cadence that worked

Long uninterrupted sessions with standing authorisation, punctuated by the owner
redirecting priorities, beat short supervised ones by a wide margin. The standing
authorisation that made it work was specific: merge your own work once the checks are
green, do not check in on each item, and stop immediately when told to.

The thing that makes that safe is not trust. It is that the checks are real, the
destructive actions still require asking, and the record of what happened is written down
well enough to audit later. Which is what this book is.
