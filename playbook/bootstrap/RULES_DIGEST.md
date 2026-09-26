# Rules Digest

113 defects from a previous build, each reduced to the rule that prevents it. Every line is the residue of something that actually broke and cost real time. The reasoning behind each is in BUILD_PLAYBOOK.md; look it up when a rule seems wrong rather than guessing at it.

Generated 2026-09-26 from a ledger spanning 7 days and 51 commits.

## Read this first

The three ways defects were most often found, in order: found by reading the code or the output (50), found by measuring something (33), a test caught it (15). None of them is a tool. All three are habits: read the built output rather than the source that produced it, measure a number nobody has measured before, and render the thing and look at it.

The dominant failure mode is silent loss, 25 of 113: something quietly did less than it claimed. A loop over an empty list, a filter that dropped rows, a guard that stopped checking, a table that never received a write. None of these raise an error. Assert counts, not the absence of exceptions.

## Learned the hard way, more than once

These cost this build twice or more each. If you read nothing else here, read these.

- (5 times, build system) A guard that covers a subset of cases reproduces the original defect in the cases it skips, and it is more dangerous than no guard because the incident it was written for feels closed.
- (5 times, content generation) An aggregate over a mixed population reports the population, and if part of that population is flat by construction it will hide the part that is not.
- (5 times, content generation) A corpus field is written against the one sentence the author had in mind, and the schema that reuses it three templates later has no way to know which shape it is.
- (5 times, content generation) A size threshold on a check is a silent exemption, and it grows as the corpus does: every schema written from a small authored corpus falls under it by construction, which is exactly the population most likely to carry a structural tell.
- (4 times, content generation) A counter that nothing reads is not instrumentation, it is a comment that looks like instrumentation, and it is worse than nothing because it answers the question 'is anyone watching this' with a yes.
- (4 times, content generation) A check that infers what to expect from the same data it is checking cannot fail on a missing field: absence reads as nothing to look for.
- (3 times, tests and guards) A path that exists on the machine you wrote the test on is not a path. Resolve environment-specific locations through one helper that falls back to the tool's own default, and return undefined rather than an empty string, because undefined means 'you decide' and an empty string means 'launch nothing'.
- (3 times, build system) A regex that counts things assumes a formatting convention, and a file that legitimately breaks the convention counts as zero rather than as an error.
- (3 times, tests and guards) Extracting a shared helper does not migrate the callers. The extraction fixes the file it was extracted from and leaves every sibling on the old path, which is two earlier defects in a different costume: a correction applied to the instances in hand rather than to the pattern.
- (3 times, content generation) Reading the record does not prevent the defect; the practice does. This one was written hours after its own lesson was read closely enough to be catalogued as a recurrence, and it was caught by rendering three items rather than by remembering.
- (3 times, content generation) A fix scoped to where the evidence was is a fix scoped to the sample, not to the defect.
- (3 times, content generation) When a defect is about a KIND of code rather than a line of code, a guard bolted to the site of the failure does not generalise, and writing one feels like closing the case.
- (3 times, search and metadata) An enumeration that has to be kept in step by memory will fall out of step, and the failure is silent because nothing downstream can tell the difference between a section that was excluded on purpose and one that was forgotten.
- (2 times, content generation) Test your content against the strategies a lazy adversary would use, not only against whether it is correct.
- (2 times, css and layout) The same undefined-property failure will find you repeatedly, at every severity from one icon to an invisible legal control.
- (2 times, build system) Two habits, both mine rather than the code's. Verify with the sequence the pipeline runs, read out of its config, not with the subset you remember: a suite chosen from memory drifts to the parts that were failing last week.
- (2 times, build system) A size limit on a generated file is only a guard if something bounds the generator too; otherwise it is a delayed failure that lands on whoever commits next, and reads as their fault.
- (2 times, content generation) A module that nothing imports fails no test, and an exception raised on every draw is indistinguishable from an exception raised on a hard draw.
- (2 times, content generation) A generator's wrong answers are written as labels and read as labels, and nobody looks at the values two labels produce.
- (2 times, content generation) A template is a promise about the grammar of what goes into it, and the promise is invisible: the code says name and the sentence needs a singular noun phrase.
- (2 times, content generation) A generated item is checked as data, and this one was correct as data: the logic was valid, the key was right, the distractors were the intended errors.
- (2 times, search and metadata) When a fix names a class of input, such as 'the stat field is free text', find every place that input is used before closing it.
- (2 times, content generation) Any consumer that describes a value in words must read the field that records what kind of value it is, never the field's name.
- (2 times, tests and guards) Run every browser suite when a site-wide element such as a modal ships, because a test nobody runs is a claim about the past.

## Content generation

- Any generator that claims reproducibility must be seeded from something stable across processes.
- Deletion by shadowing is invisible. Any collection whose size is a fact about the product needs its size asserted, not just its contents.
- A deduplication key must be canonical under every transformation the item legitimately undergoes.
- The same inflation arrives through a different door every time you close one. When you fix a dedup bug, ask what else shares an identity.
- Dedup can be wrong in both directions. An over-broad key deletes real content as silently as a narrow one inflates it.
- Every filter needs its rejection count reported. A filter that silently drops is indistinguishable from an input that was never there.
- In any set of multiple-choice content, count where the answers are. A positional tell makes the whole set worthless to a test-wise user, and it is invisible item by item.
- A guard on the extreme of a distribution can be satisfied by moving the mass next to the extreme.
- A correction table is a set of claims about outcomes, and an entry that quietly fails still counts as applied.
- A seeded shuffle is deterministic, which makes calling it twice look harmless: the same input gives the same output.
- Writing a second tool for the same job in a different context reproduces every detail the first one learned the hard way, unless the detail is written down somewhere the second author will look.
- A report that truncates its output invites the reader to write text that continues it, and a tool that appends will put that text somewhere else.
- A record has parts that refer to one another, and a tool that edits one part by text is editing a graph while looking at a string.
- A guard that takes the intent as an argument is only as good as the argument, and an argument derived by hand from the same data the guard is checking is a second implementation of the thing being checked.
- A guard written from the instance in front of you covers that instance. An earlier defect was a bare infinitive in a noun slot, so the guard looked for bare infinitives, and the sentence one screen away in the same file was a wh clause in a clause slot and went straight through.
- A standard library function whose name is a plausible description of half of what it does will be used for that half.
- Presentation rules travel with the value, and a value formatted at the point of use is formatted by whoever was writing that line.
- A check is scoped to a grain, and the grain is a claim about where a defect can live.
- Every guard here measured the answer's place in its set, and a set of guards that all take the same kind of measurement shares a blind spot the size of everything else.
- Two lessons, and they compound. A rule copied into code by its examples loses the clause the examples were illustrating: CLAUDE.md bans six named sites and coaching site blogs, and the list kept the six and dropped the category, which is the half that generalises.
- Two corpora side by side, one guarded per unit and one guarded only in total, is not two levels of rigour but one measurement and one blind spot.
- A list of misconceptions is a list of labels and a student sees numbers. Where every characteristic error runs the same direction the key sits at a predictable place in the ordered options however carefully the item is shuffled, because the shuffler can only place it among the candidates it is handed.
- Generated data gets checked for the properties the questions need, monotone and positive and distinguishable, and not for the properties the world needs.
- Fixing an instance of a defect is the moment to sweep for the rest of it, and the sweep is worth running even when it is too noisy to become a check.
- A check downgraded because a source is unreachable carries an assumption with no expiry date on it, and the assumption is usually narrower than the downgrade.
- When the same file already solves a problem correctly, the second implementation is the one to distrust: the reference was available and was not used, so whatever made it easy to skip will make it easy to skip again.
- A provenance label is a factual claim and deserves the same checking as the number it annotates.
- When a page publishes a number the build computes, the page should read it from the build.

## Tests and guards

- Measure the moment the user can act, not a browser lifecycle event. A test that measures the wrong instant is worse than no test, because it produces a number people trust.
- A regex with a length bound is a guard with an expiry date. Assert the number of things checked, not only that the checks passed.
- Check your checker. A tool that cries wolf gets muted, and then it is worse than nothing.
- A negative assertion passes when the system is broken in the right way. Always pair it with the positive case, or it is testing nothing.
- A stochastic measurement on one seed is an anecdote. If your system has randomness, a single-run before-and-after cannot distinguish a change from the weather.
- Classify by what a thing is, not by what it is called. Naming conventions are a hint, never a type.
- A test that is not wired into CI is a test that does not exist. Prove a suite runs in the place it is supposed to run, not on your machine.
- Before you measure a layout, assert the thing is rendered. Hidden elements answer most DOM questions, and they answer them wrongly.
- An error feed with no filter is a feed nobody reads. Signal has to be defended, and the cheapest defence is a human label that mutes permanently, so the queue gets quieter as it learns.
- A guard that reads the repository needs the repository. CI checkouts are shallow by default, and anything that walks history, blames a line or resolves an old hash will fail in a way that looks like the data is wrong rather than the clone.
- When you add a condition that skips a check, make sure it describes the failure and not something merely correlated with it.
- A commit hash is not a durable citation in a repository that squashes. Pull requests, issues and tags survive history rewriting; branch commits do not.
- A metric that moves against you when the product improves will eventually be used to justify reverting an improvement.
- An aggregate is a claim about whatever you grouped by. Group by the file and you have measured the file.
- A check that reports pass or fail from a handful of random draws is a check that will flip on work that has nothing to do with it, and the cost is not the false alarm.
- A ratchet is only read while it is quiet. One that fires on noise gets re-recorded as a reflex, and the re-recording is indistinguishable from accepting a real regression, so the mechanism that exists to catch regressions becomes the mechanism that launders them.

## Front end

- Generated code is code. If your build writes JavaScript into a string, the build must parse the result, because the blast radius of one bad character is the whole file, not the line.
- Nobody notices a page getting slower one commit at a time. Put the number in a test the first time you care about it, not the first time somebody complains.
- try/catch around an API that returns errors is decoration. Know which convention each call uses before you wrap it.
- When you change a filename scheme, grep for the old name as a string, including inside regexes.
- A fixed rounding rule is wrong at one end of the range or the other. Pick the precision from the magnitude, and write the expected number down before you write the code that produces it.
- The moment a single-tenant store becomes multi-tenant, every key in it is a collision waiting to happen.
- A conditional that treats not-A as the original case is a bug the day a third case exists.
- Anything that reports failures must not be able to report its own. Check whether each call rejects or throws before you wrap it, and make the reporting path unable to re-enter itself.
- Async on a script tag decides when it runs, not when it downloads, so an async tag still competes for bandwidth with everything the page is waiting for.

## Search and metadata

- A refactor that moves data has to be followed to every reader, and a loop over nothing is the quietest failure in programming.
- Any number in user-facing copy that describes the size of something must be computed from that thing at build time.
- When one model feeds two pages, generate both from the model in the same pass. Two places that must agree will not, and the reader who notices is the reader you were trying to convince.
- Test every noun in a title against the page's own data, because a title is a promise to someone who has not seen the page yet.
- A URL that search engines know is not the site's to delete quietly; it belongs partly to everyone still linking to it.

## Build system

- A parse guard covers the file shapes someone thought of. When the same code moves into a new shape, a separate file, a chunk, a worker, the guard does not follow it.
- A guard keyed to wording is a guard on the wording, not the fact, and every synonym is a hole in it.
- A file generated for a different audience has to be read as that audience, not as the one that generated it.

## Scoring and selection

- Check that your instrumentation fired at all before you trust anything built on it.
- A type system spread across a renderer and a grader will drift. The cheapest guard is one that exercises every variant end to end, once.
- If your system branches on difficulty, measure that the branches actually differ.
- When you add a filter, find every path that adds items after the filter runs. A gate on the entry point is not a gate on the set.
- Anything a page promises is the same for everyone has to be assigned, stored and served, not recomputed from whatever happens to be loaded, because the recomputation will eventually run against different inputs.
- Measure an adaptive policy per student, not in aggregate: a pooled statistic averages the starved students with the well-served ones and reports a system that works.

## Infrastructure and deploy

- Two hostnames are two origins and therefore two of everything the browser scopes by origin.
- An exclusion list is a denylist, and denylists are wrong by omission. Derive the allowed set from what the built pages actually reference.
- Verify a cache-fronted fix with a cache-busting request, or you are testing the cache.
- Know your platform's hard limits and assert them in the build. A deploy-time rejection is a bad place to learn a number your build could have told you.
- A guard that is a hand-kept list of safe paths is written by the same hand that made the mistake.
- An optional safety parameter is a guard only while its value is read rather than recalled.

## CSS and layout

- CSS comments do not nest. When a whole page category loses its styling, read the built artefact, not the source that produced it.
- An undefined CSS custom property is silent. Audit computed colour, not authored colour, and do it on the rendered page.
- A dark mode does not break by having a wrong colour. It breaks by missing one. Any colour paired with a ramp has to move with the ramp.
- CSS never fails loudly. A malformed rule is skipped, a bad selector eats the block after it, and an undefined variable paints as nothing.

## Payments

- Idempotency belongs in the database, not in the handler. Handlers race; unique indexes do not.
- Read what a payment field means, not what it is called. Cumulative and incremental fields look identical until the second event.
- When a write is destructive, capture what you need from the old value first. Ask what question you will want to answer after this row is gone.
- Row Level Security is row-level. Which columns a role may write is a separate grant, and anything money depends on belongs to the service role alone.
- Enumerate every value a third-party status field can take before you branch on one of them.

## Database

- Postgres fires same-timing triggers alphabetically. If two triggers on one table have an order dependency, encode it in the name, and test the outcome rather than the code.
- UPDATE OF is a statement-shape filter, not a change filter. If you need 'when this value changed', compare OLD and NEW yourself.
- In Postgres, revoking from every role you can name still leaves PUBLIC. Verify with the advisors or by reading the acl, never by reading your own migration.
- An empty catch block around a write is a silent-loss defect waiting to be born. If a save can fail, the person must be told; a success toast that fires regardless of the result is worse than no toast, because it actively teaches the user the data is safe.

## Interface and data display

- Chart form is a claim about the data. A line claims the values in between existed.
- Never encode a state by colour alone. The word also survives greyscale printing, forced-colors mode and a glance from across a room, so it is better for everyone and not only for the people it is required by.
- Copy that says above, below, left or right is a hard dependency on layout that nothing checks.
