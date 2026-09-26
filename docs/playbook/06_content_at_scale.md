# Content at Scale, Without Lying About It

This platform ships over a hundred thousand practice items across {{BANK_FILES}} bank
files. Almost all are generated. The chapter is about how to do that without producing a
number that is technically true and substantively false.

## Generators, not text

An item is produced by a schema: a template plus a parameter space plus a rule for
generating distractors. The schema knows how to make a correct answer and how to make
wrong answers that are wrong for a reason.

**Every key is computed, never asserted.** The generator does not record which option is
correct; it computes the answer from the parameters and then places it. An asserted key is
a key that can be wrong, and a wrong key in a practice bank is the worst possible defect
because the learner concludes they are wrong.

## The counting problem

The hard part of generated content is not generating it. It is counting it honestly. This
project got the count wrong in four distinct ways.

**The dedup key must be canonical under every transformation the item legitimately
undergoes.** Answer position is randomised per draw, and the key hashed choices in order,
so one question with its options rearranged counted as two. Sort before hashing.

**Identity is not always the choices.** For reading items, identity is the passage plus
the question asked. Four passages produced five hundred "distinct" stated-idea items that
differed only in which of the passage's other sentences came along as distractors. A
student who has answered one has answered all of them.

**An over-broad key deletes as silently as a narrow one inflates.** Two different
conditional questions produced the same stem, hashed identically, and half the inference
items in any corpus would have vanished without a word.

**A filter that drops must say so.** A length guard measuring the wrong unit silently
removed sixteen valid items. Every rejection stage reports its rejection count.

The honest yield number for reading items here, once both dedup bugs were fixed, is about
six stated-idea and two inferred-idea questions per passage. That means five hundred
inference items needs roughly a hundred and seventy passages. **That number is the entire
cost of the category, and it is recorded rather than discovered later.**

## Quality ratchets

A generated bank drifts toward exploitable patterns unless something measures them. Two
that mattered here:

**The length tell.** In one section the longest option was the correct answer 81 percent
of the time. A test-wise student does not need to read the question. The generator now
draws distractors so that the key's length rank is uniform, and a ratchet in the test
suite fails if the tell reappears. It is down to chance.

**Comparable development.** Each added clause in a distractor is chosen to leave the
option wrong for the reason it was already wrong, so length and elaboration carry no
signal about correctness.

**A ratchet is a pinned number that may only move one way.** If a fix makes a statistic
better, pin the better number. This is the cheapest possible regression test for anything
statistical, and it works where an exact assertion cannot.

## Shipping a large bank to a browser

At a hundred thousand items the bank is tens of megabytes, and this is where content scale
becomes a performance problem.

- The whole bank as a blocking script meant **20.3 seconds to the first question on
  throttled 3G**. Nobody noticed, because nobody had measured it.
- The fix is a strided starter bank, small and covering every category, plus an async
  remainder that pushes into the same array. Time to first question fell to 7.6 and 11.0
  seconds, and blocking download from 11.3 MB to 1.2 MB.
- Platform limits bite here. Cloudflare rejects a single static asset over 25 MiB, so the
  remainder is chunked, and the build fails on any asset over the limit.
- When you change a file naming scheme, grep for the old name as a **string**, including
  inside regular expressions. A service worker precache pattern of `bank_rest\.js$` does
  not match `bank_rest1.js`, and the failure is silent degradation of offline support.

## The sourcing discipline for facts

Generated practice items are one thing. Published facts about the world are another, and
they need a different regime.

- **Every figure carries a source, a year and a URL.** Not a citation in prose: fields, on
  the record, validated at build time.
- **Unverifiable means null, and null renders as a dash.** Never a guess, never a
  plausible round number.
- **A named list of banned sources**, enforced by the validator. Forums, aggregators,
  crowd-edited encyclopaedias and coaching-company blogs. A build fails if one appears.
- **One file per entity**, so a fix touches one file and a validator can walk them all.
  This project holds {{SCHOOL_FILES}} school files under that scheme.
- **When a source cannot be reached, say so immediately and stop.** Two exams on this site
  are blocked, and recorded in the roadmap as blocked, because the test makers' pages
  return bot challenges. The rows that exist for them cite a banned source and are marked
  for replacement rather than quietly reused. Being blocked and saying so is a better
  state than being unblocked by a guess.
