# Rules Digest

37 defects from a previous build, each reduced to the rule that prevents it. Every line is the residue of something that actually broke and cost real time. The reasoning behind each is in BUILD_PLAYBOOK.md; look it up when a rule seems wrong rather than guessing at it.

Generated 2026-09-21 from a ledger spanning 35 days and 64 commits.

## Read this first

The three ways defects were most often found, in order: found by reading the code or the output (15), found by measuring something (9), a test caught it (7). None of them is a tool. All three are habits: read the built output rather than the source that produced it, measure a number nobody has measured before, and render the thing and look at it.

The dominant failure mode is silent loss, 11 of 37: something quietly did less than it claimed. A loop over an empty list, a filter that dropped rows, a guard that stopped checking, a table that never received a write. None of these raise an error. Assert counts, not the absence of exceptions.

## Tests and guards

- Measure the moment the user can act, not a browser lifecycle event. A test that measures the wrong instant is worse than no test, because it produces a number people trust.
- A regex with a length bound is a guard with an expiry date. Assert the number of things checked, not only that the checks passed.
- Check your checker. A tool that cries wolf gets muted, and then it is worse than nothing.
- A negative assertion passes when the system is broken in the right way. Always pair it with the positive case, or it is testing nothing.
- A stochastic measurement on one seed is an anecdote. If your system has randomness, a single-run before-and-after cannot distinguish a change from the weather.
- Classify by what a thing is, not by what it is called. Naming conventions are a hint, never a type.
- A test that is not wired into CI is a test that does not exist. Prove a suite runs in the place it is supposed to run, not on your machine.
- Before you measure a layout, assert the thing is rendered. Hidden elements answer most DOM questions, and they answer them wrongly.

## Content generation

- Any generator that claims reproducibility must be seeded from something stable across processes. hash() is not, in Python, and the failure shows up as a flaky test rather than as a wrong answer.
- Deletion by shadowing is invisible. Any collection whose size is a fact about the product needs its size asserted, not just its contents.
- A deduplication key must be canonical under every transformation the item legitimately undergoes. Ask what varies per draw before you hash.
- The same inflation arrives through a different door every time you close one. When you fix a dedup bug, ask what else shares an identity.
- Dedup can be wrong in both directions. An over-broad key deletes real content as silently as a narrow one inflates it.
- Every filter needs its rejection count reported. A filter that silently drops is indistinguishable from an input that was never there.

## Front end

- Generated code is code. If your build writes JavaScript into a string, the build must parse the result, because the blast radius of one bad character is the whole file, not the line.
- Nobody notices a page getting slower one commit at a time. Put the number in a test the first time you care about it, not the first time somebody complains.
- try/catch around an API that returns errors is decoration. Know which convention each call uses before you wrap it.
- When you change a filename scheme, grep for the old name as a string, including inside regexes. A pattern is a hardcoded name wearing a disguise.
- A fixed rounding rule is wrong at one end of the range or the other. Pick the precision from the magnitude, and write the expected number down before you write the code that produces it.

## Infrastructure and deploy

- Two hostnames are two origins and therefore two of everything the browser scopes by origin. Pick one and redirect on the server, not in a meta tag.
- An exclusion list is a denylist, and denylists are wrong by omission. Derive the allowed set from what the built pages actually reference.
- Verify a cache-fronted fix with a cache-busting request, or you are testing the cache. This costs one query parameter and saves an hour of chasing a fix that already worked.
- Know your platform's hard limits and assert them in the build. A deploy-time rejection is a bad place to learn a number your build could have told you.

## CSS and layout

- CSS comments do not nest. When a whole page category loses its styling, read the built artefact, not the source that produced it.
- An undefined CSS custom property is silent. Audit computed colour, not authored colour, and do it on the rendered page.
- A dark mode does not break by having a wrong colour. It breaks by missing one. Any colour paired with a ramp has to move with the ramp.

## Database

- Postgres fires same-timing triggers alphabetically. If two triggers on one table have an order dependency, encode it in the name, and test the outcome rather than the code.
- UPDATE OF is a statement-shape filter, not a change filter. If you need 'when this value changed', compare OLD and NEW yourself.
- In Postgres, revoking from every role you can name still leaves PUBLIC. Verify with the advisors or by reading the acl, never by reading your own migration.

## Payments

- Idempotency belongs in the database, not in the handler. Handlers race; unique indexes do not.
- Read what a payment field means, not what it is called. Cumulative and incremental fields look identical until the second event.
- When a write is destructive, capture what you need from the old value first. Ask what question you will want to answer after this row is gone.

## Search and metadata

- A refactor that moves data has to be followed to every reader, and a loop over nothing is the quietest failure in programming. Derive counts from one source and assert they agree.
- Any number in user-facing copy that describes the size of something must be computed from that thing at build time. The moment it is typed, it has a half-life.

## Scoring and selection

- Check that your instrumentation fired at all before you trust anything built on it. An empty table looks identical to a quiet week.
- A type system spread across a renderer and a grader will drift. The cheapest guard is one that exercises every variant end to end, once.

## Interface and data display

- Chart form is a claim about the data. A line claims the values in between existed. Ask whether that claim is true before choosing it.
