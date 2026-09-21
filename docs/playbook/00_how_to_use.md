# How to Use This Book

This is the record of building one platform, written so it can be used to build a
different one.

The platform is Start From Nowhere, a test-preparation site with five adaptive exam
trainers, a college and business-school rankings library, a blog, a forum, subscriptions
through two payment processors, and an admin console. It was built between
{{FIRST_COMMIT_DATE}} and {{LAST_COMMIT_DATE}}, which is {{ELAPSED_DAYS}} days, across
{{COMMITS}} commits, by one owner directing a series of AI coding sessions. As of this
build it is {{PY_FILES}} Python files, {{JS_FILES}} JavaScript files, {{TS_FILES}}
TypeScript edge functions, {{SQL_FILES}} migrations and {{MD_FILES}} documents:
{{TRACKED_FILES}} tracked files in total.

None of those numbers were typed. They are measured from the repository every time this
document is built, which is the first thing worth copying.

## What is in here

The book has four kinds of chapter, and they age differently.

**The recipe chapters** say how to stand up each part of the system: the infrastructure,
the build, the interface, the algorithm, the content pipeline, the database, payments,
business intelligence. These are the slowest to rot, because they are mostly about
sequence and tradeoff rather than about any particular API.

**The defect ledger** is every bug, error and misfire that cost real time, with what was
seen, why it happened, how it surfaced, what fixed it, and what now stops it recurring.
Each entry ends with a lesson stated without reference to this codebase, because that is
the part that transfers.

**The analysis chapter** is computed from the ledger. It counts how defects were actually
found, which failure modes dominate, and which guards have already failed more than once.
A handwritten guide cannot contain this chapter, because it has to be recounted every time
the ledger changes.

**The bootstrap pack** is the part you use to start something new. It is a set of
ready-to-paste artefacts for opening a fresh Claude project on a different business idea,
with everything this build learned already loaded.

## How to actually use it

**Starting something new.** Go straight to the last chapter, The Bootstrap Pack. It gives
you three files and the order to use them in. You do not need to read the rest first; the
pack carries the distilled rules.

**Building a specific part.** Read the matching recipe chapter, then read the ledger
entries for that area. The recipe says what to do; the ledger says what will go wrong. The
second is worth more.

**Reviewing work before it ships.** Use The Checklist. It is generated from the ledger, so
every line on it exists because something went wrong once, and nothing is on it for
completeness.

## How this document stays true

It is built, not maintained. Three sources go in:

1. `docs/playbook/*.md`, the prose. Written by a person; this is the judgement.
2. `data/playbook/incidents.jsonl`, the defect ledger. One JSON record per incident,
   carrying the commit that fixed it and the file that now guards it.
3. The repository itself, harvested at build time for every figure in the text.

`python3 src/build_playbook.py` assembles them and writes Markdown, HTML, PDF and Word.
Three things fail the build rather than shipping quietly:

- An unresolved `{{PLACEHOLDER}}`, which means a fact the document wanted no longer exists.
- An incident citing a commit hash or a guard file that cannot be found.
- An em dash or en dash, because the house style bans them and the document about the
  house rules should not break them.

That last one is a joke with a serious point behind it. A rule that is only enforced by
attention is a rule that decays. Every rule worth having should have something that
notices when it is broken.

## Adding to it

When something breaks, add a record to `data/playbook/incidents.jsonl` before you fix it,
while you still remember what you believed was true five minutes ago. That belief is the
most valuable field and the first one you lose.

The record needs: what was seen, why, how it surfaced, the fix, the guard that now catches
it, and the lesson stated so it makes sense to someone who has never seen this code. The
`guard` field is what makes the ledger adaptive: the checklist chapter is generated from
those fields, so writing the record is the only step. Nothing has to be copied anywhere.

If two records name the same guard, the analysis chapter will say so, and that means the
guard did not hold and needs rebuilding rather than trusting.
