# The Data Layer

{{TABLES_IN_MIGRATIONS}} tables across {{MIGRATIONS}} migrations, with the database rather
than the application as the enforcement point.

## Row Level Security as the default posture

1. **Enable RLS on every table at creation.** Not in a later pass.
2. **No policy means no access**, which is exactly right for anything only your server
   should touch. This project's telemetry, error and billing tables all have RLS on and no
   policies at all; the service role bypasses RLS, and admins read through functions.
3. **Public read where public read is the point**, scoped: forum rows that are not hidden,
   for instance.
4. **Open insert with server-side stamping.** The forum takes posts from anyone with no
   account. The client cannot set the author, the country or the address hash; triggers
   do. A client-supplied field is a claim.

## The `SECURITY DEFINER` pattern

Every privileged read is a function that checks admin membership and then reads. Clients
never touch the underlying table.

Two rules that are easy to get wrong:

**Revoke from `PUBLIC`, not just from `anon` and `authenticated`.** A leading `=X/postgres`
in `pg_proc.proacl` means `PUBLIC` holds `EXECUTE`, and revoking from every role you can
name changes nothing. Verify with the platform's advisors or by reading the ACL. Never
verify by reading your own migration.

**Never take an id from the request body.** The cancel-subscription and portal functions
here read the caller's id from their own RLS-scoped row. A function that accepts an id
and acts on it is a function that acts on anyone's row.

## Triggers, and the two that bit

**Postgres fires same-timing triggers in alphabetical order by name.** On this project
`profiles_sharing_eligibility` sorted before `profiles_sync_age_tier`, so eligibility was
judged against a stale age tier and **silently revoked every legitimate adult opt-in**.
If two triggers on one table have an order dependency, encode it in the name with a
numeric prefix.

**`UPDATE OF <columns>` fires on the columns named in the statement**, not on what
actually changed, and not on what an earlier `BEFORE` trigger wrote into `NEW`. So
`update profiles set birth_year = 2011` ran the sync, stored a minor's tier, and skipped
the eligibility check entirely. If you need "when this value changed", fire on every
update and compare `OLD` to `NEW` yourself.

Both were found by a SQL smoke test that asserted the **guarantee** and rolled itself
back. Neither would have been found by reading the trigger.

## Ordering, idempotency and the event problem

Webhooks do not arrive in order. Notifications do not arrive in order. This is not an edge
case, it is the normal condition, and the consequences are severe: a `deleted` landing
after an `updated` resurrects a cancelled plan, and the reverse downgrades a paying
customer.

The discipline, which applies to any external event source:

1. **Never write the event payload.** The payload tells you *which* thing changed. Re-read
   the current state from the source of truth and write that.
2. **Guard on a monotonic field.** A notification older than what you last wrote is
   discarded. Apple provides `signedDate`; most systems provide something.
3. **Terminal states are terminal.** A refund or a revocation is never overwritten by a
   late renewal.
4. **Put idempotency in the database, not the handler.** A unique index on the natural key
   is correct under concurrency. A check-then-insert in application code is not.

## Retention

- Unlinkable telemetry: 400 days here, on a scheduled job rather than a trigger, because
  a delete on every insert puts a table scan in the path of the user's action.
- The retention window should match the longest window your console can query, so nothing
  the interface can ask for is ever missing.
- **A billing ledger is not telemetry.** It is a financial record and it is kept.

## Migrations as a readable record

Every migration in this repository opens with a comment explaining what it does and, more
importantly, **why the obvious alternative was rejected**. Read six months later, the
"why not" is the part you need; the "what" is in the SQL.

Keep the applied migrations mirrored in the repository, and keep a manifest with
checksums. Applying through a console and forgetting to mirror is how a schema and its
history diverge, and the divergence is invisible until somebody tries to rebuild.

## Privacy as a data-model decision

Two ideas here are worth copying wholesale.

**Unlinkability by construction.** The item telemetry table has no user column, no session
column, no device column and no address column, **by design, and must never gain one**.
That absence is precisely why it needs no consent gate. Privacy enforced by a schema is
stronger than privacy enforced by a policy document, because a schema cannot be forgotten.

**Keep what someone told you separate from what you were told about them.** Self-reported
attributes live on the profile. Third-party appended attributes live in a separate table
that cascades on deletion. They are never merged, so what a person said about themselves
stays distinguishable from what was bought about them, forever.
