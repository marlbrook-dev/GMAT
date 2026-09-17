# What we are allowed to collect, what we do collect, and what we refuse

Written because the ask was "determine everything we are allowed to gather and collect,
especially if the user gives us consent." The honest answer has three parts, and only the
first one is about law.

This is our own working reading, not legal advice, and it has not been through counsel.
Where it makes a judgement call it says so. Everything it claims about our own system was
checked against the database and the built pages on 2026-09-17, and the checks are named.

## 1. The finding, up front

**Consent is not the lever we thought it was.** The single most valuable stream for this
product, per-item behaviour, needs no consent at all, because with the identifiers stripped
it is not personal data. Consent buys attribution and marketing data: where a visitor came
from, which campaign, how long they stayed, which pages they read in what order. That is
worth having and we now ask for it properly. But it is not what makes the adaptive engine
better.

So the strategy is the opposite of "ask for consent, then take everything." It is:

1. Take the behavioural signal **unlinkably**, where the question of consent does not
   arise, and take it in as much detail as the product can actually use.
2. Ask for the attribution signal **honestly**, with a real refusal, and lose the visitors
   who say no without degrading anything for them.
3. Refuse the categories whose only real use is advertising, because we do not advertise
   and saying so is worth more than the data.

## 2. The four gates a field has to pass

A field is collectable only if it clears all four. Most arguments about privacy confuse
gate A with gate C.

**Gate A: is it personal data at all?** Data that cannot be linked to an identified or
identifiable person is outside GDPR and outside the CCPA definition of personal
information. The test is not "did we remove the name", it is "can this row be tied back to
a person, or joined to another row from the same person, by us or by anyone with means
reasonably likely to be used." A table with no user id, no session id, no device id, no IP
and no timestamp precise enough to act as one passes gate A. A table with a random session
id does not, because that id links rows to each other.

**Gate B: does it read or write the visitor's device?** ePrivacy in the EU and PECR in the
UK gate *any* storage or retrieval on terminal equipment, not just cookies and not just
personal data. localStorage, sessionStorage, IndexedDB and fingerprinting all count.
Consent is required unless the access is strictly necessary to deliver the service the
person asked for. This is why "we use no cookies" is not a defence: the rule is about
storage access, not the word cookie.

**Gate C: what is the lawful basis?** Contract, legitimate interest, or consent.
Legitimate interest requires a balancing test that a regulator could read, and it is not
available where gate B already requires consent.

**Gate D: is it a special category, or a minor's?** Health, biometrics, race, religion,
politics, sex life and trade union membership need explicit consent or another Article 9
condition. Minors matter here specifically: the SAT and ACT trainers are aimed at people
under 18, GDPR Article 8 sets the age of valid consent at 13 to 16 depending on the member
state, and COPPA applies under 13 in the US. Any design that leans on a child's consent is
a design we should not ship.

## 3. What we collect today

Checked against `information_schema.columns` and `pg_policies` on 2026-09-17.

| What | Table | Gate A | Gate B | Basis | Disclosed |
|---|---|---|---|---|---|
| Item outcome and interaction: exam, question id, skill, section, difficulty, option chosen, correct, seconds, mode, ms to first pick, answer switches, self-reported guess, self-reported miss reason | `item_events` | Not personal data: no user, session, device or address column exists | No device read or write | Legitimate interest, and outside GDPR on gate A | Banner and privacy 2 |
| Page analytics: path, referrer, campaign tags, device class, viewport, duration, session id, country and salted IP hash | `site_events` | Personal data: the session id links rows | Writes `sessionStorage` | **Consent**, refusable, GPC honoured | Banner and privacy 2 |
| Client errors: message, stack, file, line, build, path, device, user agent, session id | `client_errors` | Personal data by the same reasoning | Reads the same session id | Legitimate interest in a working product | Privacy 2 |
| Account: email, practice history, ratings, review queue, settings | `profiles`, `attempts`, `sessions` | Personal data | localStorage, strictly necessary for a product that works signed out | Contract | Privacy 2 |
| Self-reported profile: age range, gender, country, role | `profiles` | Personal data, and age range plus gender are sensitive in effect | None extra | Consent, optional, editable, Account page only | Privacy 2 |
| Forum posts: body, chosen name, country, salted IP hash | `forum_*` | Personal data, and public by design | Device pseudonym in localStorage | Contract plus legitimate interest in moderation | Privacy 2 |
| Subscription facts: tier, status, period dates, Stripe ids | `profiles` | Personal data | None | Contract | Privacy 2 |

The raw IP address is never stored anywhere: a database trigger derives a country and a
salted hash and the address is discarded. Verified by column inspection.

## 4. What consent would additionally allow, and what we should do about each

This is the list the question asked for: things that are lawful to collect with valid
consent. The recommendation column is the product judgement, which is a separate thing
from the legal one.

| Candidate | Lawful with consent? | Recommendation |
|---|---|---|
| Per-item interaction detail (time to first pick, switches, hesitation) | Needs no consent once unlinkable | **Taken.** Shipped 2026-09-17. This was the highest value item on the list and consent was never the obstacle. |
| Which explanation or hint was opened, and for how long | No consent needed unlinkably | **Take next.** Same table, same shape. Tells us which explanations actually work. |
| Passage scroll and re-read behaviour on reading items | No consent needed unlinkably | **Take, carefully.** Useful for reading comprehension calibration. Store aggregate counts per item, never a timeline, because a timeline plus an item id starts to look like a session. |
| Referrer, campaign, path sequence, dwell | Yes, with consent | **Taken.** This is what the banner is for. |
| A persistent device id across sessions | Yes, with consent (gate B) | **Decline.** It would convert every unlinkable row into a linkable one, which is precisely the property we are relying on. The cost is not worth the cohort analysis. |
| City-level or finer location from IP | Yes, with consent | **Decline.** Country is enough for everything we actually do. |
| Email open and click tracking | Yes, with consent | **Decline.** We send sign-in links and service mail. Tracking opens on a sign-in link is indefensible. |
| Session replay and heatmaps | Yes in principle, with consent and strict masking | **Refuse.** These tools capture typed input by default, and our product has an essay view. One misconfiguration and we are storing a student's writing. |
| Device fingerprinting for fraud or duplicate detection | Gate B applies; consent needed for non-essential use | **Refuse.** Named in privacy as something we do not do. |
| Third party advertising or retargeting pixels | Yes, with consent | **Refuse.** We state we run no third party trackers and do not sell or share. That promise is worth more than the revenue, and it is load-bearing in the billing copy. |
| Buying or appending third party data about a person | Yes with consent in some jurisdictions; effectively never with valid consent at our scale | **Refuse.** CLAUDE.md forbids it outright. |
| Inferring demographics from behaviour or name | Consent does not make this accurate or safe | **Refuse.** Demographics are self-reported on the Account page or they do not exist. |
| Using practice data to train a foundation model | Would need its own basis and its own notice | **Not doing it.** If it is ever proposed, it needs counsel, a new notice, and an opt-in that is not bundled with anything else. |

## 5. The rules that fall out of this

1. **Identity is the thing to leave out.** Anything that can be answered from unlinkable
   rows gets collected that way, and no identifier gets added to `item_events` for
   convenience. If a future question genuinely needs linkage, it needs its own table, its
   own basis and its own notice, not a new column here.
2. **A refusal has to cost the visitor nothing.** The site behaves identically either way,
   the reject control sits beside accept at the same size, and a Global Privacy Control
   signal is a refusal we honour without asking. Verified in Chromium by
   `src/smoke_consent.js`.
3. **The choice has to be changeable.** Privacy Choices sits in the footer of every page,
   and withdrawing stops the beacon on the page you withdrew it from rather than at the
   next load.
4. **Nothing gets collected that we cannot describe in a sentence a student would
   understand.** The banner's detail panel is the test. If a field cannot be explained
   there, it does not ship.
5. **privacy.html moves in the same commit.** Not afterwards. CLAUDE.md already required
   this; it is repeated here because it is the rule most likely to slip.

## 6. Open, with an owner

- **Counsel review of this document and of privacy.html.** Owner: Hunter. Nothing here has
  been reviewed by a lawyer.
- **A retention period for `item_events`.** It has none today. It should: the rows stop
  being useful for item quality long before they stop accumulating, and "we keep it
  forever" is a bad answer even for data about nobody. Proposal: delete rows older than
  400 days, matching the query window cap already in `admin_item_diagnostics`.
- **Minors and the banner.** Gate D says a child's consent is not a sound basis. Today the
  only thing behind consent is page analytics, which we can afford to lose, so the exposure
  is small. It stays small only if nothing important ever moves behind that banner.
