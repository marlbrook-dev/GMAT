# The Bootstrap Pack: Starting a New Project With This Loaded

This chapter answers one question: what do you actually paste into a fresh Claude
conversation so that a new build starts with everything this one learned?

## The wrong answer, first

Do not paste the book. It is roughly the length of a short novel, and pasting it has three
problems. It consumes context that the actual work needs. It buries the twenty operative
rules inside several thousand sentences of reasoning about a test-prep site. And most of
it is *explanation*, which is what you want when you are deciding something and noise when
you are executing.

**Reference material and operating instructions are different artefacts and need different
delivery.** The book is reference. The rules are instructions. Only the second goes in the
prompt.

## The pack

`python3 src/build_playbook.py` writes four files into `playbook/bootstrap/`, all
generated from the same ledger as the book, so none of them can drift from it.

**`CLAUDE.template.md`** goes in the new repository's root. Claude Code reads it on every
turn. It is the constitution: the house rules, the never-invent-a-value rule, the sourcing
rules, the communication rule, and a short architecture section you fill in as you build.
Four bracketed blanks at the top are the only things you have to change.

**`KICKOFF.md`** is the literal first message for a new conversation. It sets the working
agreement, the phase order, and what a session should report. Paste it, then describe your
business idea underneath it.

**`RULES_DIGEST.md`** is every lesson in the defect ledger, compressed to one line each and
grouped by area. It is about three pages. This is the highest value-per-token artefact in
the whole project: {{INCIDENT_COUNT}} real defects reduced to the rules that prevent them,
with the specifics of this codebase stripped out.

**`incidents.jsonl`** is the raw ledger, copied so the new project can start appending to
it on day one rather than starting an empty one.

## How to load it, by surface

**Claude Code, new repository.** Copy `CLAUDE.template.md` to the repo root as
`CLAUDE.md`, fill in the four blanks, and copy `incidents.jsonl` to
`data/playbook/incidents.jsonl`. Copy `src/build_playbook.py` too, so the new project's
own ledger becomes its own book from the first defect. Then open a session with
`KICKOFF.md` as the first message.

**A Claude Project on claude.ai.** Put `BUILD_PLAYBOOK.md` and `RULES_DIGEST.md` into
Project Knowledge, where they are retrieved on demand rather than sitting in every
message. Put the contents of `CLAUDE.template.md`, filled in, into the project's custom
instructions. Start the first conversation with `KICKOFF.md`.

**A single conversation, no project.** Paste `RULES_DIGEST.md`, then `KICKOFF.md`, then
your idea. Attach `BUILD_PLAYBOOK.md` as a file if the surface allows it. That ordering
matters: rules first, so they frame everything after, and the long reference last or not
at all.

## Why this layering works

Three reasons, and they are worth understanding rather than just following.

**Retrieval beats repetition.** A document in project knowledge is consulted when relevant.
The same document in the prompt is re-read on every single turn, at full cost, mostly when
it is irrelevant. For anything longer than a few pages, retrieval is strictly better.

**Instructions need to be short enough to be followed.** A rule competing with ten thousand
words of context is a rule that gets applied inconsistently. The digest is deliberately
brutal: one line per lesson, imperative mood, no examples. The examples are in the book,
where they can be looked up when a rule seems wrong.

**The ledger is the part that compounds.** The recipe chapters age. The rules do not,
because each one is the residue of a real failure, and the failure modes of software are
considerably more stable than its tooling. A new project that starts with
{{INCIDENT_COUNT}} defects already prevented is genuinely ahead, and every defect it hits
of its own makes the next project further ahead still.

## Keeping the loop closed

The pack is only worth carrying forward if the new project feeds it back. So the working
agreement in `KICKOFF.md` includes one instruction that does the whole job:

> When something breaks, append a record to `data/playbook/incidents.jsonl` before fixing
> it, while you still remember what you believed was true five minutes ago.

That is the entire maintenance burden. Everything else, the checklist, the analysis, the
digest, the book, is generated from those records.

## What to change for a different domain

`CLAUDE.template.md` has four blanks:

1. **The product, in one sentence**, and who it is for.
2. **The house style rules you will enforce.** Keep the dash ban unless you have a reason
   not to; it is free and it makes the build's style enforcement real.
3. **The sourcing regime.** If you publish external facts, keep the whole thing including
   the banned-source list. If you do not, delete that block rather than leaving it as
   decoration.
4. **The architecture section.** Empty at the start. Fill it in as decisions are made, and
   only with things that are expensive to rediscover.

Everything else in the template is domain-independent and should be kept verbatim.
