# The Algorithm: Adaptive Selection and Honest Scoring

This chapter is about a test-preparation engine, but the transferable part is the last
section, and it applies to any product that shows a person a number about themselves.

## The shape of the engine

One engine serves {{EXAM_COUNT}} exams ({{EXAM_LIST}}). Adding an exam is a registry entry
plus a tagged bank, not a fork. That was not free: the single most useful refactor in the
project was making the section keys, skill lists and copy resolve from an exam id injected
at build time, instead of being hardcoded. Before it, one application had been shipping a
score card headed with the wrong exam's name and telling students to calibrate at the
wrong test maker's site.

**If you have two of something, resolve the differences from data, not from conditionals.**
A conditional on `if (exam === 'sat')` treats "not SAT" as "the original one", and that
assumption breaks silently the moment there is a third.

## Ability estimation

Three-parameter logistic item response theory, fitted by Fisher scoring, producing an
ability estimate and a standard error. Alongside it, an Elo-style per-skill rating that
moves faster and is what the learner actually sees at the skill level.

The two exist for different jobs and it is worth being clear about which is which. The IRT
estimate is for the score band, because it has a defensible error term. The Elo rating is
for selection and for the skill table, because it responds quickly enough to feel like it
is paying attention.

## Item selection, and the two bugs in it

Selection targets an item near the learner's current ability, with a damping factor so a
run of luck does not send the difficulty somewhere absurd.

**Bug one: selecting on a per-skill counter instead of measured ability.** Early on, a
skill with fewer than six answers targeted a fixed starting rating rather than the
learner's measured ability in that section. A strong student answering a new skill got
beginner items. The fix targets the section's measured ability until the skill has its own
evidence.

**Bug two: re-serving items the learner had already answered.** The candidate pool did not
exclude seen items, so a short session could serve the same question twice. The fix
filters to unseen candidates and falls back to the full pool only when unseen is empty.
The same fix had to be applied separately to passage groups, because a passage drags its
sibling questions along with it and the group was not being filtered.

Both were found by a **review bot**: a script that sits the exam repeatedly against the
real engine and reports what only playing reveals. It measures estimate recovery, band
coverage across ability levels, whether selection actually adapts, bank reach, starving
skills, and whether a deliberately planted weakness is diagnosed. That last one is the
sharpest test in the suite, because it has a known right answer.

**Measuring a stochastic system on one seed is an anecdote.** A change here looked like it
dropped band coverage from 88 percent to 72. Across three seeds the baseline was 52, 88
and 80 against 72, 80 and 72 for the change. The spread between seeds was larger than the
effect, and the regression did not exist.

## Scoring, and the honesty constraints

This is the transferable part.

The product reports an estimated **range** on the exam's own scale, never a single number,
never called a predicted score, and never shown before a minimum evidence threshold. The
band half-width is the standard error of the ability estimate with a floor, so it can
narrow with evidence but never collapses to a point.

Four rules sit behind that, and every one of them is a rule about not overclaiming:

1. **A range, not a number.** A single number implies a precision the estimate does not
   have. The interval is the honest object.
2. **A floor on the interval.** Even with a lot of evidence, the interval never gets
   narrower than the floor, because the model's error is not the only error.
3. **Nothing before the evidence threshold.** An estimate from four answers is noise with
   a decimal point.
4. **The method is published, and the calibration is named as ours.** The scale anchoring
   is this product's calibration, not the test maker's, and the page that explains the
   method says so and stays in step with the code.

Two further rules are specific but generalise:

- **Never mix incomparable scales.** Two editions of one exam use different ranges and are
  not convertible; they are compared by percentile only, with the concordance cited. Any
  product with a legacy unit and a current one has this problem.
- **Never present an internal threshold as official.** A routing cut chosen here is ours
  and is labelled ours.

The pattern underneath all of it: **when you show someone a number about themselves, the
number is a claim, and the claim has an error bar whether or not you print it.** Printing
it is the difference between a product people trust and one they catch out.
