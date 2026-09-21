# Business Intelligence

## The three streams

Keep them separate and know what each can answer.

**Site events.** A first-party beacon on every page: path, referrer, UTM, a session id
from `sessionStorage`, device class, duration. Country and a salted address hash added by
a trigger so the raw address is never stored. Behind a consent banner that honours Global
Privacy Control and can be reopened from any page footer.

**Product telemetry.** What happened inside the product. Here that is item telemetry with
**no user, session, device or address column, by design**. It answers "is this item too
hard" and cannot answer "what did this person do", and that is the trade that lets it run
without a consent gate.

**Billing events.** Money. Covered in the payments chapter.

**They are deliberately not joined.** Nothing here attributes a subscription to a visit.
That is a design choice with a real cost, and it should be stated on the page rather than
quietly left as a gap the reader assumes is filled.

## Read through functions, always

No client reads an analytics table. Every admin view is a `SECURITY DEFINER` function
gated on admin membership, returning exactly the shape the page needs.

**One read per page, not six.** Six reads can disagree with each other: the tile says
eleven paying and the chart says twelve because a webhook landed between the two queries.
One statement, one snapshot, one story.

## The numbers not to compute

This is the part that separates a dashboard from a decoration.

**A churn rate needs a denominator held at the start of the window.** If your ledger is
younger than the window, you cannot supply one. The counts and the lost revenue are real;
the ratio would be a guess wearing a percentage sign. This dashboard prints the counts and
explicitly declines the rate, and says why, and starts printing it automatically once the
ledger is old enough.

**A conversion rate must exclude the undecided.** A trial still running is not a failed
trial. Counting it in the denominator produces a rate that rises on its own as trials
mature, which is worse than no rate at all.

**Trial revenue is never revenue.** State the pipeline figure separately and label it as
conditional.

**Gross and net are different numbers.** Show refunds beside charges, not subtracted from
them. Netting hides the month where a fifth of revenue came back.

**A snapshot take rate is not a cohort conversion rate.** Say which one you are showing.

## Say what the data covers

Every derived figure is "since the log began". Print that date on the page. A figure that
silently covers less than its label claims is the hardest kind of wrong to catch, and it
is the failure the whole discipline exists to prevent.

## The triage loop

Errors and moderation both work the same way, and the pattern is worth naming.

1. Capture into an insert-only table.
2. Cluster by signature, and attach the evidence to the cluster: the real message, the
   real stack, the builds, the pages, how many separate sessions hit it.
3. **A human decides.** Real, fixed, will not fix, or noise.
4. The decision is stored, and it mutes the cluster permanently.

The queue gets quieter as it learns rather than louder, and the stored labels are exactly
what a future model would train on. Nothing in it edits code, and that is deliberate:
trust is the binding constraint on automated repair, so the system proposes and explains,
and a person decides.

## Never fabricate

No invented user counts, testimonials, efficacy claims or seeded activity. On a forum,
house-authored posts say they are house-authored. This is not only an ethics rule; a
fabricated number in a dashboard eventually gets used for a decision, and by then nobody
remembers it was a placeholder.
