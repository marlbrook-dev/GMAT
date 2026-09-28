# Rules Digest

Rules from 188 defects in a previous build, each reduced to the rule that prevents it. Every line is the residue of something that actually broke and cost real time. The reasoning behind each is in BUILD_PLAYBOOK.md; look it up when a rule seems wrong rather than guessing at it.

Generated 2026-09-28 from a ledger spanning 9 days and 152 commits.

## Read this first

The three ways defects were most often found, in order: found by reading the code or the output (101), found by measuring something (45), a test caught it (22). None of them is a tool. All three are habits: read the built output rather than the source that produced it, measure a number nobody has measured before, and render the thing and look at it.

The dominant failure mode is silent loss, 26 of 188: something quietly did less than it claimed. A loop over an empty list, a filter that dropped rows, a guard that stopped checking, a table that never received a write. None of these raise an error. Assert counts, not the absence of exceptions.

## Learned the hard way, more than once

These cost this build twice or more each. If you read nothing else here, read these.

- (7 times, content generation) A size threshold on a check is a silent exemption, and it grows as the corpus does: every schema written from a small authored corpus falls under it by construction, which is exactly the population most likely to carry a structural tell.
- (6 times, search and metadata) When a fix names a class of input, such as 'the stat field is free text', find every place that input is used before closing it.
- (6 times, content generation) Run the source check on every corpus that cites pages, not just the one that broke.
- (6 times, content generation) Finding a number on a page is not finding the fact. A check has to look for it beside the words that say what it counts, and notice when those words are about something else: another program, another class.
- (5 times, build system) A guard that covers a subset of cases reproduces the original defect in the cases it skips, and it is more dangerous than no guard because the incident it was written for feels closed.
- (5 times, content generation) An aggregate over a mixed population reports the population, and if part of that population is flat by construction it will hide the part that is not.
- (5 times, content generation) A corpus field is written against the one sentence the author had in mind, and the schema that reuses it three templates later has no way to know which shape it is.
- (5 times, content generation) A citation vouches only for what its source says, so check each figure against the source rather than checking that a citation is present.
- (4 times, content generation) Two lessons, and they compound. A rule copied into code by its examples loses the clause the examples were illustrating: CLAUDE.md bans six named sites and coaching site blogs, and the list kept the six and dropped the category, which is the half that generalises.
- (4 times, content generation) A counter that nothing reads is not instrumentation, it is a comment that looks like instrumentation, and it is worse than nothing because it answers the question 'is anyone watching this' with a yes.
- (4 times, content generation) A check that infers what to expect from the same data it is checking cannot fail on a missing field: absence reads as nothing to look for.
- (4 times, content generation) Any consumer that describes a value in words must read the field that records what kind of value it is, never the field's name.
- (4 times, content generation) A citation is only as current as the page it points to, and publishers leave old pages up.
- (4 times, content generation) Anything written ahead of its publication date is a promise about the future made from the past.
- (4 times, tests and guards) Loading a page is not the same as reading it. A chart can be a separate document inside the page that draws only when scrolled into view, and a page with trackers may never fall quiet, so a reader built for checking has to scroll like a person, collect every frame, and use waits that give up rather than hang.
- (3 times, css and layout) The same undefined-property failure will find you repeatedly, at every severity from one icon to an invisible legal control.
- (3 times, tests and guards) A path that exists on the machine you wrote the test on is not a path. Resolve environment-specific locations through one helper that falls back to the tool's own default, and return undefined rather than an empty string, because undefined means 'you decide' and an empty string means 'launch nothing'.
- (3 times, build system) A regex that counts things assumes a formatting convention, and a file that legitimately breaks the convention counts as zero rather than as an error.
- (3 times, tests and guards) Extracting a shared helper does not migrate the callers. The extraction fixes the file it was extracted from and leaves every sibling on the old path, which is two earlier defects in a different costume: a correction applied to the instances in hand rather than to the pattern.
- (3 times, build system) A size limit on a generated file is only a guard if something bounds the generator too; otherwise it is a delayed failure that lands on whoever commits next, and reads as their fault.
- (3 times, content generation) A module that nothing imports fails no test, and an exception raised on every draw is indistinguishable from an exception raised on a hard draw.
- (3 times, content generation) Reading the record does not prevent the defect; the practice does. This one was written hours after its own lesson was read closely enough to be catalogued as a recurrence, and it was caught by rendering three items rather than by remembering.
- (3 times, content generation) A generator's wrong answers are written as labels and read as labels, and nobody looks at the values two labels produce.
- (3 times, content generation) A generated item is checked as data, and this one was correct as data: the logic was valid, the key was right, the distractors were the intended errors.
- (3 times, content generation) A fix scoped to where the evidence was is a fix scoped to the sample, not to the defect.
- (3 times, content generation) When a defect is about a KIND of code rather than a line of code, a guard bolted to the site of the failure does not generalise, and writing one feels like closing the case.
- (3 times, search and metadata) An enumeration that has to be kept in step by memory will fall out of step, and the failure is silent because nothing downstream can tell the difference between a section that was excluded on purpose and one that was forgotten.
- (3 times, content generation) A stored phrase that goes into more than one slot has to be written for the hardest of them, and the transform has to run in the direction that cannot damage anything: capitalising a sentence opener is always safe, lowercasing one breaks proper nouns.
- (3 times, content generation) An edit that appends text has to read what it is appending to. A correction step that checks only its own goal (here, that the choice got longer) will happily achieve it by making the choice worse, and every check downstream measures the goal, so nothing notices.
- (3 times, content generation) A figure written twice on one page will eventually be written two ways. Where the site already holds a sourced value, a page that states it should be checked against that value, because a reader who meets $4 and $5 for the same fee trusts neither.
- (3 times, content generation) A presence check on a source field proves the field is filled, not that it is true.
- (3 times, content generation) A search result's snippet is not the page it links to. A figure taken from one has to be read again on the page before it is published, and a record that admits the snippet in a note while citing the page looks fully sourced, which is why nobody rereads it.
- (3 times, content generation) A report that says the same thing every week stops being read. When a checker has blind spots, record each judgement about a finding it cannot settle, so that what it prints shrinks to what is new; a list that mixes known false alarms with real errors hides the errors about as well as no list at all.
- (3 times, tests and guards) A checker has to know when it has not read its source. A response is not the page because it has text in it: a challenge, an error page or a login wall reads as a page with none of the facts on it, and every fact then looks wrong.
- (3 times, tests and guards) A checker's excuse category needs the same scrutiny as its findings. "Shows none of its figures" was given one cause and the cause was believed, but to a check that looks for numbers, a page whose every figure changed looks exactly like a page that never loaded.
- (3 times, build system) Two copies of one check drift apart. When a check exists in two places, a fix to one is a question about the other, and the cheapest answer is to make them share the code that splits text.
- (3 times, content generation) A style rule that nothing checks holds only for the work written after someone remembered it.
- (3 times, content generation) When a check fails the same way twice with different details, guard the shape rather than the instance.
- (2 times, search and metadata) Any number in user-facing copy that describes the size of something must be computed from that thing at build time.
- (2 times, infrastructure and deploy) Two hostnames are two origins and therefore two of everything the browser scopes by origin.
- (2 times, content generation) Test your content against the strategies a lazy adversary would use, not only against whether it is correct.
- (2 times, content generation) A record has parts that refer to one another, and a tool that edits one part by text is editing a graph while looking at a string.
- (2 times, build system) Two habits, both mine rather than the code's. Verify with the sequence the pipeline runs, read out of its config, not with the subset you remember: a suite chosen from memory drifts to the parts that were failing last week.
- (2 times, content generation) Every guard here measured the answer's place in its set, and a set of guards that all take the same kind of measurement shares a blind spot the size of everything else.
- (2 times, tests and guards) A ratchet is only read while it is quiet. One that fires on noise gets re-recorded as a reflex, and the re-recording is indistinguishable from accepting a real regression, so the mechanism that exists to catch regressions becomes the mechanism that launders them.
- (2 times, content generation) A template is a promise about the grammar of what goes into it, and the promise is invisible: the code says name and the sentence needs a singular noun phrase.
- (2 times, tests and guards) Run every browser suite when a site-wide element such as a modal ships, because a test nobody runs is a claim about the past.
- (2 times, content generation) A test measures what someone can get right without the skill, and there is more than one way to do that.
- (2 times, content generation) A figure with a source and a year can still go stale, because the source moves and the record does not.
- (2 times, content generation) When a parser must pull one value out of free text, anchor it to the words that give the value its meaning, not to its position, and return nothing when nothing anchors it: a sentence that says less is better than one that states a guess as fact.
- (2 times, search and metadata) Any sentence about your own product's state is data, and data belongs in one place: build the sentence from the source that knows, and check every page that could repeat it, including the text only search engines read.
- (2 times, css and layout) CSS forgives a variable that was never defined by quietly using the initial value, so a missing token never throws, it only looks slightly wrong.
- (2 times, content generation) A label fixed in code is a claim about every value the field will ever hold. When the data carries its own qualifier, such as a timing or a statistic, the label has to be read from the data, and anything that compares or scores the values has to use only the ones that share the qualifier the method names.
- (2 times, tests and guards) A checker that reads a page has to read the page a person sees, not the file behind it.
- (2 times, content generation) A fact filed next to another fact tends to inherit its citation. When two facts come from one section of a site, check that each one's own page says it, not the page its neighbour came from.
- (2 times, content generation) A number's presence on a page is weak evidence for a fact, because pages are full of numbers that mean other things: menus, dates, grade ranges, footnote markers.
- (2 times, content generation) A guard written for the instance found covers only where that instance was. When a rule applies everywhere, check where every page ends up, the built output, rather than one of the several places pages are written.
- (2 times, tests and guards) A figure copied from a page its publisher rewrites every year expires on the publisher's schedule, not yours.

## Content generation

- Any generator that claims reproducibility must be seeded from something stable across processes.
- Deletion by shadowing is invisible. Any collection whose size is a fact about the product needs its size asserted, not just its contents.
- A deduplication key must be canonical under every transformation the item legitimately undergoes.
- The same inflation arrives through a different door every time you close one. When you fix a dedup bug, ask what else shares an identity.
- Dedup can be wrong in both directions. An over-broad key deletes real content as silently as a narrow one inflates it.
- Every filter needs its rejection count reported. A filter that silently drops is indistinguishable from an input that was never there.
- In any set of multiple-choice content, count where the answers are. A positional tell makes the whole set worthless to a test-wise user, and it is invisible item by item.
- A correction table is a set of claims about outcomes, and an entry that quietly fails still counts as applied.
- A seeded shuffle is deterministic, which makes calling it twice look harmless: the same input gives the same output.
- A report that truncates its output invites the reader to write text that continues it, and a tool that appends will put that text somewhere else.
- A guard written from the instance in front of you covers that instance. An earlier defect was a bare infinitive in a noun slot, so the guard looked for bare infinitives, and the sentence one screen away in the same file was a wh clause in a clause slot and went straight through.
- A standard library function whose name is a plausible description of half of what it does will be used for that half.
- Presentation rules travel with the value, and a value formatted at the point of use is formatted by whoever was writing that line.
- A check is scoped to a grain, and the grain is a claim about where a defect can live.
- A check downgraded because a source is unreachable carries an assumption with no expiry date on it, and the assumption is usually narrower than the downgrade.

## Tests and guards

- Measure the moment the user can act, not a browser lifecycle event. A test that measures the wrong instant is worse than no test, because it produces a number people trust.
- A regex with a length bound is a guard with an expiry date. Assert the number of things checked, not only that the checks passed.
- A negative assertion passes when the system is broken in the right way. Always pair it with the positive case, or it is testing nothing.
- A test that is not wired into CI is a test that does not exist. Prove a suite runs in the place it is supposed to run, not on your machine.
- Before you measure a layout, assert the thing is rendered. Hidden elements answer most DOM questions, and they answer them wrongly.
- When you add a condition that skips a check, make sure it describes the failure and not something merely correlated with it.
- A commit hash is not a durable citation in a repository that squashes. Pull requests, issues and tags survive history rewriting; branch commits do not.
- An aggregate is a claim about whatever you grouped by. Group by the file and you have measured the file.

## Front end

- Generated code is code. If your build writes JavaScript into a string, the build must parse the result, because the blast radius of one bad character is the whole file, not the line.
- try/catch around an API that returns errors is decoration. Know which convention each call uses before you wrap it.
- A fixed rounding rule is wrong at one end of the range or the other. Pick the precision from the magnitude, and write the expected number down before you write the code that produces it.
- The moment a single-tenant store becomes multi-tenant, every key in it is a collision waiting to happen.
- A conditional that treats not-A as the original case is a bug the day a third case exists.

## Build system

- A parse guard covers the file shapes someone thought of. When the same code moves into a new shape, a separate file, a chunk, a worker, the guard does not follow it.
- A guard keyed to wording is a guard on the wording, not the fact, and every synonym is a hole in it.
- A heuristic stopping rule is right only when nothing better is known. Where the size of what is being collected is known exactly, stop at that size and check that it was reached.

## Search and metadata

- A refactor that moves data has to be followed to every reader, and a loop over nothing is the quietest failure in programming.
- When one model feeds two pages, generate both from the model in the same pass. Two places that must agree will not, and the reader who notices is the reader you were trying to convince.
- A URL that search engines know is not the site's to delete quietly; it belongs partly to everyone still linking to it.

## Scoring and selection

- Check that your instrumentation fired at all before you trust anything built on it.
- A type system spread across a renderer and a grader will drift. The cheapest guard is one that exercises every variant end to end, once.
- If your system branches on difficulty, measure that the branches actually differ.

## Infrastructure and deploy

- An exclusion list is a denylist, and denylists are wrong by omission. Derive the allowed set from what the built pages actually reference.
- Know your platform's hard limits and assert them in the build. A deploy-time rejection is a bad place to learn a number your build could have told you.

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

82 more rules, each learned once from a less costly defect, did not fit a prompt sized digest. The checklist in BUILD_PLAYBOOK.md has every rule.
