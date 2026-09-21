# Tests and Guards

{{TEST_FILES}} test files, and the interesting thing about them is not what they assert.
It is that the analysis chapter can count how defects were **actually** found, and the
answer reshapes where you put effort.

## The ladder

**Rung 1: the build.** Structural guards on the artefact. Parse every generated script.
Assert every collection size. Fail on platform limits. Compare inputs to outputs at every
filter. Cheapest rung, catches the most.

**Rung 2: domain logic, headless.** The engine, run without a browser, once per variant.
Fast enough to run on every change.

**Rung 3: the real browser against the real built site.** Playwright against the built
output over a local server, at desktop and phone width, in both themes. **Assert
behaviour, not markup.** A markup assertion breaks on every refactor and passes through
every real bug.

**Rung 4: adversarial play.** A bot that uses the product the way a user would, repeatedly,
and reports what only use reveals. Three real defects here came from nowhere else.

**Rung 5: the periodic audit.** Contrast, links and metadata across every page, weekly.
Catches the slow rot that no single change is responsible for.

## The failure modes of tests themselves

Five entries in the defect ledger are about tests being wrong, and that proportion is not
an accident. **A broken test is invisible, because its output is identical to a working
one.**

**A negative assertion passes when the system is broken in the right way.** "Nothing is
sent when consent is refused" passed here because the test used the wrong storage key, so
consent was never configured, so nothing was ever sent. It would have passed with the
feature deleted. **Always pair a negative assertion with the positive case**, or you are
asserting nothing.

**A test can measure the wrong instant.** A performance test waited for the browser load
event, which waits for the async resource the optimisation moved off the critical path.
A change that made the page usable nine times faster would have reported no improvement.
**Measure the moment the user can act.**

**A guard can narrow its own scope.** A count check matching `\d{2,4}` stopped checking
the two largest counts when they passed ten thousand, and kept passing. **Assert how many
things you checked**, not only that the checks passed.

**A test can measure something that was never rendered.** A hidden element still answers
`innerText` and `getComputedStyle`. Layout and contrast assertions passed here on a view
that was never displayed. **Assert the thing is on screen before you measure its layout.**

**A test can classify by name instead of by value.** A theme parity check selected tokens
by name prefix and flagged a font size as a missing colour.

## Ratchets

For anything statistical, pin the number and allow it to move one way. If a fix improves
a statistic, pin the better value. This is how the length tell in the item bank went from
81 percent to chance and stayed there.

A ratchet only works if it is stable. This project's ratchets drifted run to run because
the generator seeded from a randomised hash, and a flaky ratchet gets deleted. **Seed from
something stable and assert reproducibility first.**

## Write the expected number before the code

The dashboard test here carries a fixture of two subscriptions and a comment block
computing, by hand, what every tile must show. The test knew $159.84 was the right answer
before the page existed, which is how it caught the page printing $160.

**If you cannot write down the expected output before you write the code, you do not yet
understand the requirement.**

## Wire it into CI, and prove it ran

The browser suites on this project **had never actually run.** Playwright was a declared
dependency in a repository where nothing had installed it. The tests existed, the command
existed, and the coverage was zero.

A test that is not wired into CI is a test that does not exist. Prove a suite runs in the
place it is supposed to run.

## Render it and look at it

Three defects here were found by taking a screenshot: a chart unreadable in dark mode, a
line chart implying values that never existed, and a dashboard that was not on screen.
None of them would have been caught by an assertion, because none of them were violations
of anything anybody had thought to assert.

**Budget for looking.** It is the cheapest test there is and the only one that catches
things you have not imagined.
