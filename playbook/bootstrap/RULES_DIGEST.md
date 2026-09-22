# Rules Digest

68 defects from a previous build, each reduced to the rule that prevents it. Every line is the residue of something that actually broke and cost real time. The reasoning behind each is in BUILD_PLAYBOOK.md; look it up when a rule seems wrong rather than guessing at it.

Generated 2026-09-22 from a ledger spanning 35 days and 71 commits.

## Read this first

The three ways defects were most often found, in order: found by reading the code or the output (27), found by measuring something (19), a test caught it (11). None of them is a tool. All three are habits: read the built output rather than the source that produced it, measure a number nobody has measured before, and render the thing and look at it.

The dominant failure mode is silent loss, 19 of 68: something quietly did less than it claimed. A loop over an empty list, a filter that dropped rows, a guard that stopped checking, a table that never received a write. None of these raise an error. Assert counts, not the absence of exceptions.

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
- When you add a condition that skips a check, make sure it describes the failure and not something merely correlated with it. A skip is indistinguishable from a pass in the output, so the fix for a noisy check can silently delete it.
- A path that exists on the machine you wrote the test on is not a path. Resolve environment-specific locations through one helper that falls back to the tool's own default, and return undefined rather than an empty string, because undefined means 'you decide' and an empty string means 'launch nothing'.
- A commit hash is not a durable citation in a repository that squashes. Pull requests, issues and tags survive history rewriting; branch commits do not. Cite the thing that outlives the merge, and make any check of the other one advisory.
- A metric that moves against you when the product improves will eventually be used to justify reverting an improvement. When a number goes the wrong way after a change that should only have helped, measure the underlying thing directly before believing either the number or your own explanation of it. Never redefine the metric in the same change that made it look bad.
- An aggregate is a claim about whatever you grouped by. Group by the file and you have measured the file. State the grouping in the sentence that reports the result, and the overclaim becomes visible while you are writing it.
- Extracting a shared helper does not migrate the callers. The extraction fixes the file it was extracted from and leaves every sibling on the old path, which is INC-0059 and INC-0064 in a different costume: a correction applied to the instances in hand rather than to the pattern. Three suites had failed visibly and ten were wrong; the seven silent ones were found by the guard, not by reading. When a helper exists because a direct call was wrong, make the direct call fail the build, and let it enumerate the callers rather than enumerating them by hand.

## Content generation

- Any generator that claims reproducibility must be seeded from something stable across processes. hash() is not, in Python, and the failure shows up as a flaky test rather than as a wrong answer.
- Deletion by shadowing is invisible. Any collection whose size is a fact about the product needs its size asserted, not just its contents.
- In any set of multiple-choice content, count where the answers are. A positional tell makes the whole set worthless to a test-wise user, and it is invisible item by item.
- Test your content against the strategies a lazy adversary would use, not only against whether it is correct. Measure the score of a rule that ignores the question.
- A deduplication key must be canonical under every transformation the item legitimately undergoes. Ask what varies per draw before you hash.
- The same inflation arrives through a different door every time you close one. When you fix a dedup bug, ask what else shares an identity.
- Dedup can be wrong in both directions. An over-broad key deletes real content as silently as a narrow one inflates it.
- Every filter needs its rejection count reported. A filter that silently drops is indistinguishable from an input that was never there.
- A guard on the extreme of a distribution can be satisfied by moving the mass next to the extreme. When you correct for a measured bias, measure the whole distribution afterwards, not the statistic you were correcting.
- A correction table is a set of claims about outcomes, and an entry that quietly fails still counts as applied. Aggregate metrics hide this well: a table where half the entries work still moves the number in the right direction, which reads as success. State the per item intent in a form the machine can check, and every entry that did nothing says so by name.
- A seeded shuffle is deterministic, which makes calling it twice look harmless: the same input gives the same output. What repeats is the permutation, not the randomisation, and a permutation applied to its own result is biased toward leaving things where they were. Any function whose value comes from being applied exactly once should refuse to be applied twice rather than relying on the caller to remember. The second lesson is about reading: the generator printed the defect on every run, above the line being watched.

## Front end

- Generated code is code. If your build writes JavaScript into a string, the build must parse the result, because the blast radius of one bad character is the whole file, not the line.
- The moment a single-tenant store becomes multi-tenant, every key in it is a collision waiting to happen. Enumerate the writers before you add the second tenant, not after.
- A conditional that treats not-A as the original case is a bug the day a third case exists. Resolve variants from data, and the third one costs a row rather than a search.
- Nobody notices a page getting slower one commit at a time. Put the number in a test the first time you care about it, not the first time somebody complains.
- try/catch around an API that returns errors is decoration. Know which convention each call uses before you wrap it.
- When you change a filename scheme, grep for the old name as a string, including inside regexes. A pattern is a hardcoded name wearing a disguise.
- A fixed rounding rule is wrong at one end of the range or the other. Pick the precision from the magnitude, and write the expected number down before you write the code that produces it.
- Anything that reports failures must not be able to report its own. Check whether each call rejects or throws before you wrap it, and make the reporting path unable to re-enter itself.

## CSS and layout

- The same undefined-property failure will find you repeatedly, at every severity from one icon to an invisible legal control. One audit of computed colour catches the whole class.
- CSS comments do not nest. When a whole page category loses its styling, read the built artefact, not the source that produced it.
- CSS never fails loudly. A malformed rule is skipped, a bad selector eats the block after it, and an undefined variable paints as nothing. Anything that matters visually has to be asserted on the rendered page, because the parser will not tell you.
- An undefined CSS custom property is silent. Audit computed colour, not authored colour, and do it on the rendered page.
- A dark mode does not break by having a wrong colour. It breaks by missing one. Any colour paired with a ramp has to move with the ramp.

## Payments

- Row Level Security is row-level. Which columns a role may write is a separate grant, and anything money depends on belongs to the service role alone.
- Enumerate every value a third-party status field can take before you branch on one of them. The value you did not think of is usually the one that matters commercially.
- Idempotency belongs in the database, not in the handler. Handlers race; unique indexes do not.
- Read what a payment field means, not what it is called. Cumulative and incremental fields look identical until the second event.
- When a write is destructive, capture what you need from the old value first. Ask what question you will want to answer after this row is gone.

## Infrastructure and deploy

- Two hostnames are two origins and therefore two of everything the browser scopes by origin. Pick one and redirect on the server, not in a meta tag.
- An exclusion list is a denylist, and denylists are wrong by omission. Derive the allowed set from what the built pages actually reference.
- Verify a cache-fronted fix with a cache-busting request, or you are testing the cache. This costs one query parameter and saves an hour of chasing a fix that already worked.
- Know your platform's hard limits and assert them in the build. A deploy-time rejection is a bad place to learn a number your build could have told you.
- A guard that is a hand-kept list of safe paths is written by the same hand that made the mistake. Derive the safe set from the artefact, not from memory.

## Scoring and selection

- If your system branches on difficulty, measure that the branches actually differ. A label is not a property.
- Check that your instrumentation fired at all before you trust anything built on it. An empty table looks identical to a quiet week.
- A type system spread across a renderer and a grader will drift. The cheapest guard is one that exercises every variant end to end, once.
- When you add a filter, find every path that adds items after the filter runs. A gate on the entry point is not a gate on the set.

## Database

- Postgres fires same-timing triggers alphabetically. If two triggers on one table have an order dependency, encode it in the name, and test the outcome rather than the code.
- UPDATE OF is a statement-shape filter, not a change filter. If you need 'when this value changed', compare OLD and NEW yourself.
- In Postgres, revoking from every role you can name still leaves PUBLIC. Verify with the advisors or by reading the acl, never by reading your own migration.
- An empty catch block around a write is a silent-loss defect waiting to be born. If a save can fail, the person must be told; a success toast that fires regardless of the result is worse than no toast, because it actively teaches the user the data is safe. And where two layers of authorisation have to agree, something has to compare them: the one that is wrong will not announce itself.

## Build system

- A regex that counts things assumes a formatting convention, and a file that legitimately breaks the convention counts as zero rather than as an error. Any counter that can return zero for a non-empty input needs a per-source assertion, not just a total.
- A parse guard covers the file shapes someone thought of. When the same code moves into a new shape, a separate file, a chunk, a worker, the guard does not follow it. List what the guard covers against what the deploy actually ships, and check the difference rather than the intention.
- A guard keyed to wording is a guard on the wording, not the fact, and every synonym is a hole in it. Widening the wording is the obvious repair and it trades missed defects for false alarms, which cost more because they get the guard switched off. Match a phrase that only the thing you care about can produce, rather than every word it might happen to use.
- A guard that covers a subset of cases reproduces the original defect in the cases it skips, and it is more dangerous than no guard because the incident it was written for feels closed. When you add a check, enumerate everything of that kind and cover all of it, or state in the code which cases are deliberately excluded and why.

## Search and metadata

- A refactor that moves data has to be followed to every reader, and a loop over nothing is the quietest failure in programming. Derive counts from one source and assert they agree.
- Any number in user-facing copy that describes the size of something must be computed from that thing at build time. The moment it is typed, it has a half-life.
- When one model feeds two pages, generate both from the model in the same pass. Two places that must agree will not, and the reader who notices is the reader you were trying to convince.

## Interface and data display

- Chart form is a claim about the data. A line claims the values in between existed. Ask whether that claim is true before choosing it.
- Never encode a state by colour alone. The word also survives greyscale printing, forced-colors mode and a glance from across a room, so it is better for everyone and not only for the people it is required by.
- Copy that says above, below, left or right is a hard dependency on layout that nothing checks. Name the thing instead, and the sentence survives every rearrangement.
