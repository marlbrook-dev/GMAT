# Payments

{{EDGE_FUNCTIONS}} edge functions handle money here: {{EDGE_FUNCTION_LIST}}.

## The shape

Hosted checkout, not a card form. The processor's hosted page removes PCI scope entirely,
and there is no version of building your own that is worth the saving.

The webhook is authenticated by the processor's signature rather than by your own auth,
which means it must be deployed with JWT verification **off** and the signature check
**on**. Get that pairing wrong in either direction and you have either an endpoint that
rejects every legitimate call or one that accepts every illegitimate one.

Every column the webhook writes is service-role only, left out of the column grants
entirely, so no browser session can forge a plan. **A signed-in user was once able to
grant themselves a paid plan on this project**; that is what the grant hardening is for.

## Two processors, and why the plan column stops being the answer

The moment a second payment source exists, "what has this person paid for" cannot be a
column, because it becomes a race: whichever webhook fired last wins, and a user who
subscribed on iOS gets downgraded the next time a card event lands on their row.

The resolution here: the original column stays exactly as it was, owned by the original
processor and untouched by anything new, and a function derives the **effective
entitlement** across every source. The application reads the function. Nothing about the
live, money-taking path changed, which was deliberate.

**Generalisation: when a second source of truth appears, do not teach the first one to
share. Add a derivation on top and move readers to it.**

## Promises that are load-bearing

Write these down and test them, because they are the ones that turn into complaints.

- **The free plan never asks for a card.** Tested in both signed-in and signed-out states.
- **Cancelling is one click, in the account page, through your own function.** Not through
  the processor's hosted portal, which may not be configured, and which puts the most
  important retention moment on somebody else's page.
- **The exception you cannot engineer around.** An Apple-sourced subscription is Apple's:
  there is no API to cancel on a user's behalf and the guidelines require pointing at
  Settings. So the button opens Apple's subscription management and explains why, rather
  than appearing to work and not. **Which path applies is decided by the entitlement
  record, never guessed from the platform the page happens to be open on.**
- **A refund window, stated, plus your own errors always refunded.**
- **Access continues to the end of the paid period.**

## The ledger, and the mistake to avoid

The most consequential payments decision in this project was made late and should have
been made first.

The profile row holds what an account pays **right now**, and it is overwritten on every
webhook. That means the instant a subscriber cancels, the evidence they ever paid is gone.
It is enough to gate access and useless for running a business: it cannot answer how much
revenue arrived this month, how much left, what share of trials converted, or what came
back out as refunds.

**Build the append-only billing event ledger before the first real subscriber.** It cannot
be reconstructed afterwards.

The design that works:

- One row per fact, normalised across processors so a chart reads one vocabulary.
- **Cash and recurring value in separate columns.** An annual plan is $99.99 of cash on one
  day and $8.33 of monthly revenue. A dashboard that adds those together is wrong in both
  directions.
- A `kind` column of your own verbs, not the processor's event names.
- `mrr_delta_cents` on every row, so new plus expansion minus contraction minus churn is
  the movement bridge by construction, and cannot be off by a rounding rule applied in one
  place and not another.

Four traps, all of which would have produced a plausible wrong number:

**Two event types announce one new subscription.** Hosted checkout completion and
subscription creation both fire, with different event ids, in no guaranteed order. Logging
both doubles new revenue. A partial unique index on (source, subscription id, kind) for
the once-per-lifetime kinds lets the database decide which arrived first.

**The first invoice is also an invoice.** Counting every paid invoice as a renewal
double-counts every new subscriber as a returning one. Only a cycle invoice is a renewal.
The cash still counts.

**The refunded amount is cumulative.** A charge reports total refunded to date, not the
amount of this refund, so a second partial refund counts the first one again. Use the most
recent refund entry.

**The cancellation write erases what you need to record the cancellation.** Read the prior
state before writing, or churned revenue is always zero.

**Sandbox is not money.** Test transactions carry real-looking prices. A sandbox row in a
revenue chart is a fictional dollar, and it will be believed.

**Know the units.** One processor reports price in milliunits: 4990 means $4.99. Reading
it as cents overstates revenue by a factor of ten, which is an error that looks like
success.

## Secrets

Secret keys and signing secrets live in the platform's secret store. Never in the
repository, never in an environment file that is committed, never in a log line. This is
the one rule in this book with no nuance attached to it.
