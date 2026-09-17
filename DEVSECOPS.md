# DevSecOps review, and the self-improving loop

Written 2026-09-16, against the live system on commit `a1494b5`. Every claim below is
either marked VERIFIED with the check that produced it, or marked UNVERIFIED. Nothing here
is stated from memory.

## 1. The three documents

### 1a. Fu, Pasuksmit and Tantithamthavorn, *AI for DevSecOps: A Landscape and Future Opportunities* (Monash University and Atlassian, April 2024)

A systematic literature review of 99 papers published 2017 to 2023, organising AI-driven
security work into 12 tasks across the DevOps lifecycle and extracting 15 challenges (C1 to
C15) each paired with a research opportunity (R1 to R15).

This is the substantive document of the three. It is a real SLR with a stated method, a
reproducible taxonomy, and challenges specific enough to act on. The parts that bear
directly on what we are building:

- **C1, Data Imbalance.** Chakraborty et al. found deep-learning vulnerability detection
  loses up to 73 percent of F1 to class imbalance. Yang et al. found over-sampling beats
  under-sampling, yet 33 to 58 percent of decisions still were not driven by the
  vulnerable statement at all. The lesson for us is narrower than the paper's: real bug
  signal is rare against a flood of noise, so any detector we build has to be judged on
  what it surfaces, not on an accuracy number.
- **C2, Model Explainability, and R2, evidence-based XAI.** The challenge recurs three
  times in the taxonomy (C2-1, C2-2, C2-3), which is the clearest signal in the paper.
  Winter et al. state the case bluntly: trust is the crucial problem in automated program
  repair, and a tool has to demonstrate reliability before anyone will act on it.
- **C3, Lack of AI Security Tooling** in IDEs, in CI/CD, and for infrastructure scanning.
- **C10, Automated Repair on Real-World Scenarios.** Repair techniques that work on
  benchmarks do not transfer cleanly to production code.
- **C14, Normality Drift, and R14.** Han et al. name the problem precisely: anomaly
  detection is usually trained zero-positive, on what normal looks like, and the
  distribution of normal shifts over time, so a detector trained on history quietly stops
  working. Their answer, OWAD, is a framework to **detect, explain and adapt** to normality
  shift at the distribution level rather than per sample. This is the single most useful
  idea in the paper for a system meant to improve with time.
- **Cid-Fuentes et al.** A detector that depends on historical failure data cannot adapt at
  runtime; model current runtime behaviour instead.
- **Du et al.** A lifelong-learning framework that adjusts the model post-deployment on
  labelled false positives and false negatives.
- **Le and Zhang, NeuralLog.** Log parsing is itself a source of error, and parse failures
  degrade detection, so they skip the parse step.

### 1b. Surasani, *DevSecOps for AI Systems: Security Automation, Model Protection, and Governance Frameworks* (Journal of Computer Science and Technology Studies, Al-Kindi Center)

An overview paper by an independent researcher. Useful as a checklist, much weaker as
evidence. Its structure is SAST/DAST/IAST plus AIOps (section 2), model protection
including watermarking, federated learning and LLM threats (section 3), and governance and
compliance (section 4).

Two honest caveats, because taking it at face value would waste our time:

1. **Most of it does not apply to us.** Sections 3.1 through 3.3 are about protecting
   models you train and ship: watermarking, federated learning, encryption of training,
   model theft and adversarial input. We do not train or ship a model. We use AI to help
   build a static site. Treating that material as a to-do list would mean building
   defences for assets we do not own.
2. **Its practical advice is generic.** Section 2.4's best practices reduce to integrate
   tools into CI/CD, train the staff, and keep the tools updated. True, and not actionable
   at our size beyond what we already do.

What it does contribute: the section 4 framing that compliance is something you automate
into the pipeline rather than audit after the fact. That is the argument for the build-time
guards we already run (the dash guard, the school-source validator, the i18n ceiling) and
for adding more of them rather than adding checklists.

### 1c. Islam, *Prompt engineering for web development* (bachelor's thesis)

A student thesis on using generative AI and prompt frameworks to build web applications,
arguing that prompt engineering lowers the cost barrier for people with ideas and limited
resources. It is descriptive rather than empirical: no controlled comparison, no defect
data, no security content. It describes how this site is in fact being built, but it does
not provide evidence for any engineering decision, and it should not be cited as if it did.
Its relevance is that it names the risk we actually carry: code produced quickly by an
assistant, with the human reviewing rather than authoring, needs machine-checked guards,
because review attention is the scarce resource.

## 2. What the review found in our system

Each finding is what the papers' framing pointed at, checked against the real system rather
than assumed.

### Fixed in this pass

**F1. Revoking a Postgres grant from a role does nothing while PUBLIC still holds it.**
VERIFIED. The Supabase security advisor reported 11 SECURITY DEFINER functions callable by
`anon`, including several an earlier migration in this branch had supposedly locked.
`pg_proc.proacl` showed a leading `=X/postgres` on each: the PUBLIC grant Postgres adds to
every new function, which `anon` inherits. Checking per-role grants after the revoke looked
clean, because the per-role grants were clean. Fixed by revoking from PUBLIC; the advisor
count went from 11 to 1, and the 1 is `is_admin()`, which is intentional.
Not exploitable as it stood: VERIFIED that five of the functions return `trigger`, which
PostgREST will not expose and Postgres refuses to call directly, and every `admin_*`
function opens by raising unless `is_admin()`. This was depth, not a breach.

**F2. Stripe webhook events are not ordered, and we were writing the event payload.**
VERIFIED by inspection against Stripe's delivery semantics. A `customer.subscription.deleted`
arriving after a `customer.subscription.updated` would have resurrected a cancelled plan
(free access forever); the reverse ordering would have downgraded a paying customer. Fixed:
every subscription event now re-reads the subscription from Stripe and writes current state,
which is correct whatever order events arrive in. Falls back to the payload if the re-read
fails, because stale state beats no state.

**F3. No HSTS, no CSP, no Permissions-Policy on a site that takes card payments.**
VERIFIED against the live site: `curl -sSI https://startfromnowhere.com/` returned
`x-content-type-options`, `x-frame-options` and `referrer-policy`, and no
`strict-transport-security` and no `content-security-policy`. Added all three to `_headers`.
VERIFIED the CSP does not break anything: the built app served over HTTP with the exact
policy boots identically to without it (12 skills, 448 bank items, same dashboard length,
9 nav buttons, zero violations), and blob-URL data export still works.

**F4. A JavaScript error on a live page was invisible.** VERIFIED: no error capture existed
anywhere in the codebase. This is the gap section 3 addresses.

### Checked and found sound, so nobody re-litigates them

**Forum output escaping.** VERIFIED. Every path where user-submitted content reaches the
DOM is escaped: `esc(t.title)`, `esc(t.author_name)`, and `paras(t.body)`, which escapes
each paragraph before inserting it. No stored XSS found. The CSP added in F3 is depth, not
a fix for a known hole.

**The plan column.** VERIFIED earlier in this branch via
`information_schema.column_privileges`: `plan` is not writable by `anon` or `authenticated`,
and the 14 columns the app legitimately writes still are. Every billing column added since
is excluded by construction, because the grant is a column list rather than a table grant.

**Error and triage tables.** VERIFIED against the live project: an anonymous insert into
`client_errors` returns 201 and the trigger stamps `country` and a salted `ip_hash` with no
raw IP, while an anonymous `select` returns `[]` with a row present. Same for
`error_triage`, which has RLS on and no policy at all, so it default-denies.

### Open, with an owner

| # | Finding | Status |
|---|---|---|
| O1 | `client_errors` and `site_events` accept unauthenticated inserts with no rate limit, so either could be flooded. The forum tables have trigger-level rate limits; these do not. | UNVERIFIED as exploited. Worth a per-IP-hash limit before traffic grows. |
| O2 | Leaked-password protection is off in Supabase Auth. We sign in with magic links, so this is precautionary. | Dashboard toggle, owner only. |
| O3 | `script-src` still needs `unsafe-inline`, because every page carries inline scripts. | Closing it means extracting the inline scripts to files with hashes. Real work, not urgent. |
| O4 | No dependency or secret scanning in CI. | `.github/workflows` runs the publish cron only. |
| O5 | No billing event log, so trial-to-paid conversion can only be reported as a snapshot ratio. | Called out in the Revenue tab itself. |

## 3. Sentinel: the loop that improves with time

The ask was a system that detects bugs and errors, identifies the source, determines a
solution, acts, and gets better as it goes. Built in stages, because stage one has to exist
before any of the others mean anything.

**Stage 1, detect.** `partials.sentinel_js()` ships with the site footer, so every content
page carries it, and it is wired separately into both trainers and the blog. It reports
uncaught errors, unhandled rejections and failed resource loads to `client_errors`. Three
rules it cannot break, since a broken error reporter is worse than none: it cannot throw,
it cannot loop (one report per signature per page view, ten maximum), and it cannot report
its own failures. First party, insert-only from the browser, no select policy, raw IP never
stored. Disclosed in privacy.html section 2.

**Stage 2, identify the source.** Messages are normalised before grouping: numbers, urls,
hex and quoted strings collapse to placeholders, so the same bug is one cluster however
many different values it carries. VERIFIED in Chromium: four thrown errors including two
differing only by an integer produced three clusters, which is the right answer. Every row
carries the build id, so a regression pins to the build that introduced it. Following Le
and Zhang, the raw message is stored verbatim and normalisation is a separate, inspectable
field, so a bug in the normaliser cannot destroy the evidence.

**Stage 3, determine a solution.** The Errors tab shows each cluster with its evidence
attached: real message, real stack, the builds, the pages, how many distinct sessions.
This is R2 applied literally, and it is why the tab shows a stack rather than a score.

**Stage 4, act.** A human marks each cluster real, fixed, wont fix, or noise. **Nothing in
this system edits code.** That is a deliberate reading of C10 and of Winter et al.: repair
techniques do not transfer cleanly to production, trust has to be earned first, and a live
payment site is the wrong place to test either finding. The fix ships through the normal
pull request.

**Stage 5, learn.** Two mechanisms, both from the papers:

- *Labelled feedback (Du et al.).* Every triage decision is stored in `error_triage`.
  Marking a cluster noise mutes it permanently, so the queue gets quieter as it learns
  rather than louder. Those labels are the training set a severity model would need, and
  they accumulate from the first day whether or not that model is ever built.
- *Rolling baseline (C14, R14, Han et al.).* The headline number compares the window
  against the preceding window of equal length rather than against a fixed threshold.
  What counts as a normal error rate moves every time we ship a feature or a new exam, and
  a frozen threshold is stale the day after it is set. This is the cheapest honest version
  of detect, explain and adapt; a distribution-level version is the next step, not the
  first one.

### What is deliberately not built yet, and why

- **Auto-remediation.** See stage 4. Revisit when the triage log shows the diagnosis has
  been right consistently, which is the reliability Winter et al. say has to come first.
- **A trained severity model.** Premature at one profile and zero subscribers. C1 says a
  model trained on this much data would learn the majority class. The labels are being
  collected now so that the model is possible later.
- **Ingesting public vulnerability feeds.** The owner asked for the system to improve as
  more public resources become available. The honest sequence is dependency scanning in CI
  first (O4), since we have almost no runtime dependencies to scan and a feed with nothing
  to match against is theatre.

## 4. Item telemetry and the consent gate

Added 2026-09-17, and the reason is worth recording: `attempts` held **zero rows**. Every
claim about the adaptive engine learning was, in production, learning from nobody, because
`Cloud.logAttempt` returns early without a signed-in user and the product deliberately
needs no account. The signal was not weak; it did not exist.

`item_events` fixes that by inverting the usual trade. Rather than asking people to sign in
or to consent so that we can attribute their answers, it records the answer and attributes
it to no one: exam, question id, skill, section, difficulty, option chosen, correct,
seconds, mode, milliseconds to first pick, answer switches, and the learner's own guess and
miss-reason tags. There is no user, session, device or address column, and adding one is
the one change this table must never take. VERIFIED by column inspection: RLS on, one
insert policy, zero select policies, zero identifying columns. VERIFIED over the wire with
the shipped publishable key: insert returns 201, select returns 42501.

That absence is what makes it lawful without a consent banner, and it is also what makes
the banner honest about what it does and does not cover. The banner gates `site_events`,
which carries a session id and is therefore personal data. Refusing is one click beside
accept at the same size, a Global Privacy Control signal is honoured as a refusal without
asking, and withdrawing stops the beacon on the page you withdrew it from rather than at
the next load. VERIFIED in Chromium by `src/smoke_consent.js`, 33 checks, including that
nothing is sent before a choice is made.

`DATA_COLLECTION.md` works through what else is collectable, with and without consent, and
why most of the consent-only categories are refused rather than taken.

**Read back by a human, not by code.** Admin > Items applies four deterministic rules over
the counts (key may be wrong, no discrimination, dead option, far off pace) plus two that
only exist because the interaction is recorded (answered by guess, keeps changing hands).
Each flag renders with the numbers that produced it and a control that opens the actual
stem. Nothing on the tab edits a question. Same reading of C10 as stage 4 above.

### What is deliberately not built yet, and why

- **A retention period.** The table has none. Named as open in `DATA_COLLECTION.md` with a
  proposal of 400 days, matching the query cap in `admin_item_diagnostics`.
- **Automatic item retirement.** A rule that pulls a flagged item from circulation would be
  acting on a signal that has, at time of writing, zero rows behind it. The flags exist so
  that a person can judge them; the automation argument can be had once there is a history
  of those judgements to check the rules against.

## 5. How to keep this document honest

Every claim above carries VERIFIED with the check, or UNVERIFIED. When a finding is fixed,
move it and name the check that proved it. When a check cannot be run, say so rather than
softening the claim, which is the same rule the site applies to school statistics.
