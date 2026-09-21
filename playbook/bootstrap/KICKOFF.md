# Kickoff

You are building a new product with me. Before anything else, read RULES_DIGEST.md in
this project: it is 55 real defects from a previous build of a comparable platform,
compressed to one rule each. Those rules are the accumulated cost of 35 days of
building, and following them is cheaper than rediscovering them.

## The working agreement

- I decide what to build, what it means and what is acceptable. You decide how.
- You do not check in on each item. Work continuously and batch the reporting.
- Anything irreversible or outward-facing, ask first: deleting data, changing a live
  payment configuration, publishing something, sending anything to a third party.
- Merge your own work once the checks are green. Stop immediately when I say stop.
- Never invent a value. Read every id, hash, count, date and URL from real output.
- If something is blocked or unreachable, tell me at the moment it happens.

## The order of work

Do these in order. Most of what goes wrong goes wrong because something was done before
the thing that would have caught it.

1. **The rules file.** Copy CLAUDE.template.md to CLAUDE.md and fill in the blanks with me.
2. **The build.** A script that turns sources into output, even if it does almost nothing
   on day one. Every guard will live here.
3. **One page, deployed to the real host on the real domain.** Learn the platform's limits
   now: per-file size, which directories the uploader walks, whether www and the apex are
   one origin, whether the headers file applies to responses your own code generates.
4. **The data layer**, with RLS on every table from creation, and one SQL smoke test that
   asserts a guarantee and rolls itself back.
5. **The design token file.** The complete palette in both themes, the type scale, the
   spacing grid. All of it, before the second page exists.
6. **The product.**
7. **Instrumentation**, before spending anything on acquisition.
8. **Payments**, last. The append-only billing event ledger goes in BEFORE the first real
   subscriber, because it cannot be reconstructed afterwards.

## What to report back

Not a list of files changed. Report:

1. What was built, in one paragraph.
2. What broke on the way, and why. Append each one to data/playbook/incidents.jsonl.
3. What is now guarded against, and in which file.
4. What was left undone, and whether that is a decision or a blocker.
5. Numbers, with the command that produced them.

## Now

Here is what I want to build:

[DESCRIBE THE BUSINESS IDEA. What it is, who it is for, how it makes money, and what
would make it obviously better than what exists. Do not worry about technical detail; ask
me what you need.]

Before you write any code, tell me: the stack you propose and why, the first week's plan
against the order above, and the three things most likely to go wrong with this
particular idea.
