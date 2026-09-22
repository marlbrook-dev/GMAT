// One independent review bot per exam. Each one sits the exam it owns, over and over,
// and reports what it found.
//
//   node src/review_bot.js            all five exams
//   node src/review_bot.js sat gre    just those
//   node src/review_bot.js --quick    fewer simulated students, for a fast loop
//   node src/review_bot.js --seed 7   reproduce an exact run
//
// Why this exists, and why it is not another unit test. test.js checks that the bank is
// well formed and that the engine's parts return sane values when poked one at a time.
// Neither of those catches the failure that actually matters to a student: the trainer
// runs, every function returns something plausible, and the estimate it spends forty
// questions building is wrong, or the adaptive selection is not adapting, or a third of
// the bank is unreachable so practice goes in circles. Those are emergent. You only see
// them by playing the thing.
//
// So each bot plays. It answers with the engine's OWN response model, pCorrect at the
// item's own difficulty, which is the honest way to do this: the bot is not allowed a
// private theory of how hard an item is. It drives the real pickQuestions, the real
// recordAttempt and the real scoreEstimate. If the engine and the bot disagree about
// what a student of ability theta would score, the engine is wrong, because the bot is
// only replaying the engine's own assumptions back at it.
//
// What each bot knows about its exam is read from the engine, never written down here.
// EXAM, SECTIONS, SECTION_META and SKILLS all resolve from EXAM_ID. A bot with 'Q' or
// 'RW' hardcoded would be asserting the structure it is supposed to be checking, and it
// would keep passing after somebody changed the real thing.
//
// The output is meant to be read by a person deciding what to fix next, so a finding
// carries the number that produced it. "coverage 41 percent" is actionable. "FAIL" is not.
const harness = require('./exam_harness.js');

const argv = process.argv.slice(2);
const has = f => argv.includes(f);
const QUICK = has('--quick');
const SEED = (() => { const i = argv.indexOf('--seed'); return i >= 0 ? Number(argv[i + 1]) : 20260921; })();
const wanted = argv.filter(a => !a.startsWith('--') && !/^\d+$/.test(a));

// How much practice a simulated student does before we judge the estimate. Deliberately
// above every exam's minAttempts floor, because the interesting question is whether the
// estimate is right once it is allowed to exist, not whether it refuses to exist early.
const ROUND = 10;
const ROUNDS = QUICK ? 6 : 14;
const PER_TIER = QUICK ? 2 : 5;

// The ability grid. Spread wide enough that an estimate which ignores the student
// entirely cannot accidentally pass the ordering check.
const TIERS = [
 { name: 'struggling', theta: -1.2 },
 { name: 'below average', theta: -0.5 },
 { name: 'average', theta: 0.0 },
 { name: 'strong', theta: 0.7 },
 { name: 'very strong', theta: 1.4 },
];

const findings = [];
function note(exam, level, label, detail) {
 findings.push({ exam, level, label, detail });
 const tag = level === 'fail' ? 'FAIL' : level === 'warn' ? 'warn' : 'ok';
 console.log('  ' + tag.padEnd(4) + ' ' + label + (detail ? '  -> ' + detail : ''));
}

const mean = a => a.length ? a.reduce((t, x) => t + x, 0) / a.length : 0;
const pct = (a, b) => b ? Math.round(100 * a / b) : 0;

/**
 * Sit one session. Returns everything observed, so the checks below can be written
 * against what happened rather than against what the engine says happened.
 */
function sit(api, theta, deficitSection, rng) {
 const { BANK, newState, pickQuestions, recordAttempt, scoreEstimate, pCorrect, eloToTheta, DIFF_ELO } = api;
 const c = 1 / (api.EXAM.choices || 4);
 const state = newState();
 const served = [];
 const seenThisSession = new Set();
 // A repeat is only a defect if an unserved item existed at the time. The LSAT bank is
 // 65 items and a sitting is 140, so repeating is arithmetic, not a bug. Counting those
 // as failures would train us to ignore the check on the one exam that needs it.
 const bySection = {};
 BANK.forEach(q => { bySection[q.section] = (bySection[q.section] || 0) + 1; });
 const seenInSection = {};
 let repeats = 0, avoidable = 0;
 let earlyReady = null;
 let floorEst = null;

 for (let r = 0; r < ROUNDS; r++) {
  const qs = pickQuestions(BANK, state, { count: ROUND });
  if (!qs.length) break;
  for (const q of qs) {
   const sec = seenInSection[q.section] || (seenInSection[q.section] = new Set());
   if (seenThisSession.has(q.id)) {
    repeats++;
    if (sec.size < (bySection[q.section] || 0)) avoidable++;
   }
   sec.add(q.id);
   seenThisSession.add(q.id);
   served.push(q);
   // The student's ability for THIS item's section. A deficit student is strong
   // everywhere except one section, which is how a real diagnostic case looks.
   const ability = (deficitSection && q.section === deficitSection) ? theta - 1.6 : theta;
   const d = eloToTheta(DIFF_ELO[q.diff] || 1100);
   const correct = rng() < pCorrect(ability, d, c);
   // Time is not what this bot is testing, so it answers at the section's own pace and
   // never trips the fast or slow flags into the result.
   const allot = (api.SECTION_META[q.section] || {}).allot || 90;
   recordAttempt(state, q, 0, correct, allot, null, false, 'bot');
  }
  // The evidence floor is a promise: no estimate before minAttempts. Check it while
  // crossing the floor rather than after, which is the only moment it can break.
  const est = scoreEstimate(state);
  if (est.ready && state.attempts.length < (api.EXAM.scale.minAttempts || 0) && earlyReady === null) {
   earlyReady = state.attempts.length;
  }
  // The first band a student is ever shown. This is the one that has to be right: it is
  // the number they screenshot and plan around, and by then we have promised them the
  // evidence floor was enough.
  if (est.ready && floorEst === null) floorEst = est;
 }
 return { state, served, repeats, avoidable, earlyReady, floorEst, est: scoreEstimate(state) };
}

function reviewExam(spec) {
 const api = harness.load(spec, { random: harness.seeded(SEED) });
 const { BANK, SKILLS, SECTIONS, SECTION_META, EXAM, sectionAbility } = api;
 const rng = harness.seeded(SEED + 1);
 const sc = EXAM.scale;

 // ---- what this bot knows it is sitting -------------------------------------------
 console.log('\n=== ' + EXAM.name + ' (' + EXAM.id + ') ===');
 console.log('  structure: ' + SECTIONS.length + ' sections ' + JSON.stringify(SECTIONS) +
  ', ' + SKILLS.length + ' skills, ' + EXAM.choices + ' choices, ' + EXAM.adaptive + ' adaptive');
 console.log('  scored ' + EXAM.scoreScale + ' in steps of ' + sc.step +
  ', band floor ' + sc.minBand + ', evidence floor ' + sc.minAttempts + ' items');
 const outside = SECTIONS.filter(s => (SECTION_META[s] || {}).inComposite === false);
 if (outside.length) console.log('  rated but outside the headline score: ' + outside.join(', '));
 console.log('  bank ' + BANK.length + ' items');

 // ---- play ------------------------------------------------------------------------
 const runs = [];
 for (const tier of TIERS) {
  for (let i = 0; i < PER_TIER; i++) runs.push({ tier, ...sit(api, tier.theta, null, rng) });
 }

 // ---- 1. does the estimate recover the student? -----------------------------------
 const byTier = TIERS.map(t => {
  const rs = runs.filter(r => r.tier === t && r.est.ready);
  return { t, n: rs.length, score: mean(rs.map(r => r.est.score)), runs: rs };
 });
 const usable = byTier.filter(b => b.n);
 if (usable.length < TIERS.length) {
  note(EXAM.id, 'fail', 'every ability tier produces an estimate',
   usable.length + ' of ' + TIERS.length + ' tiers reached the evidence floor in ' +
   (ROUNDS * ROUND) + ' items');
 } else {
  const ordered = usable.every((b, i) => i === 0 || b.score > usable[i - 1].score);
  const spread = usable[usable.length - 1].score - usable[0].score;
  const shape = usable.map(b => b.t.name + ' ' + Math.round(b.score)).join(', ');
  if (!ordered) {
   note(EXAM.id, 'fail', 'the estimate ranks students in the right order', shape);
  } else if (spread < (sc.max - sc.min) * 0.15) {
   note(EXAM.id, 'warn', 'the estimate separates strong from weak students',
    'only ' + Math.round(spread) + ' points between weakest and strongest: ' + shape);
  } else {
   note(EXAM.id, 'ok', 'the estimate ranks and separates students', shape);
  }
 }

 // ---- 2. is the published band honest? --------------------------------------------
 // The band is one standard error either side, so a correct band contains the truth
 // about 68 percent of the time. Much less and we are promising a precision we do not
 // have, which is the one claim /scoring/ makes in public.
 const ready = runs.filter(r => r.est.ready);
 let covered = 0;
 ready.forEach(r => {
  const truth = sc.center + sc.slope * r.tier.theta;
  if (truth >= r.est.lo && truth <= r.est.hi) covered++;
 });
 const cov = pct(covered, ready.length);
 const halfMean = Math.round(mean(ready.map(r => (r.est.hi - r.est.lo) / 2)));
 if (cov < 50) {
  note(EXAM.id, 'fail', 'the reported band contains the true score',
   cov + ' percent of ' + ready.length + ' sittings, expected about 68; mean half width ' + halfMean);
 } else if (cov < 60) {
  note(EXAM.id, 'warn', 'the reported band contains the true score',
   cov + ' percent of ' + ready.length + ' sittings, expected about 68; mean half width ' + halfMean);
 } else {
  note(EXAM.id, 'ok', 'the reported band contains the true score',
   cov + ' percent of ' + ready.length + ' sittings, mean half width ' + halfMean);
 }

 // ---- 2b. is the FIRST band we show a student right? ------------------------------
 // Separated from the check above because it is a different promise. minAttempts says
 // "this much practice is enough to report a range". If the estimate is still sitting on
 // its starting value at that point, we are not reporting a measurement, we are
 // reporting the prior with a confident looking interval drawn around it.
 const atFloor = runs.filter(r => r.floorEst);
 if (atFloor.length) {
  const errs = atFloor.map(r => (r.floorEst.score - (sc.center + sc.slope * r.tier.theta)));
  const inBand = atFloor.filter(r => {
   const truth = sc.center + sc.slope * r.tier.theta;
   return truth >= r.floorEst.lo && truth <= r.floorEst.hi;
  }).length;
  const absErr = Math.round(mean(errs.map(Math.abs)));
  const fcov = pct(inBand, atFloor.length);
  // Signed error by tier, because the shape is the diagnosis: if weak students read high
  // and strong students read low, the estimate is being pulled to the centre and the
  // cause is convergence, not noise.
  const shape = TIERS.map(t => {
   const rs = atFloor.filter(r => r.tier === t);
   return rs.length ? t.name + ' ' + (mean(rs.map(r => r.floorEst.score - (sc.center + sc.slope * t.theta))) > 0 ? '+' : '') +
    Math.round(mean(rs.map(r => r.floorEst.score - (sc.center + sc.slope * t.theta)))) : null;
  }).filter(Boolean).join(', ');
  if (fcov < 50) {
   note(EXAM.id, 'fail', 'the first band shown at the evidence floor contains the truth',
    fcov + ' percent; mean error ' + absErr + ' points against a half band of ' +
    Math.round(mean(atFloor.map(r => (r.floorEst.hi - r.floorEst.lo) / 2))) + '; by tier: ' + shape);
  } else {
   note(EXAM.id, 'ok', 'the first band shown at the evidence floor contains the truth',
    fcov + ' percent; mean error ' + absErr + ' points');
  }
 }

 // ---- 3. is the adaptive selection adapting? --------------------------------------
 const diffLow = mean(runs.filter(r => r.tier === TIERS[0]).flatMap(r => r.served.map(q => q.diff)));
 const diffHigh = mean(runs.filter(r => r.tier === TIERS[TIERS.length - 1]).flatMap(r => r.served.map(q => q.diff)));
 if (diffHigh <= diffLow) {
  note(EXAM.id, 'fail', 'stronger students are served harder items',
   'mean difficulty ' + diffLow.toFixed(2) + ' for the weakest tier, ' +
   diffHigh.toFixed(2) + ' for the strongest: selection is not adapting');
 } else {
  note(EXAM.id, 'ok', 'stronger students are served harder items',
   diffLow.toFixed(2) + ' -> ' + diffHigh.toFixed(2) + ' mean difficulty');
 }

 // ---- 4. the evidence floor is a promise ------------------------------------------
 const broke = runs.filter(r => r.earlyReady !== null);
 if (broke.length) {
  note(EXAM.id, 'fail', 'no score is shown before the evidence floor',
   broke.length + ' sittings reported a score at ' + broke[0].earlyReady +
   ' items, floor is ' + sc.minAttempts);
 } else {
  note(EXAM.id, 'ok', 'no score is shown before the evidence floor', sc.minAttempts + ' items');
 }

 // ---- 5. does practice repeat itself? ---------------------------------------------
 const rep = runs.reduce((t, r) => t + r.repeats, 0);
 const avoid = runs.reduce((t, r) => t + r.avoidable, 0);
 const totalServed = runs.reduce((t, r) => t + r.served.length, 0);
 if (avoid) {
  note(EXAM.id, 'fail', 'no item repeats while fresh ones are available',
   avoid + ' avoidable repeats of ' + rep + ' total, in ' + totalServed + ' items served' +
   // The avoidable count widens with the pool: a repeat counts as avoidable until the
   // student has exhausted that section, so a bigger bank keeps the condition true for
   // longer and the figure can rise while the student sees fewer repeats. Doubling the
   // LSAT reading bank cut repeats from 1875 to 1006 and pushed avoidable from 258 to
   // 309 (INC-0061). The rate below is the number a student actually experiences, and it
   // is printed next to the diagnostic one so neither can be read alone.
   ' (' + Math.round(rep / totalServed * 100) + ' percent of served items were repeats)');
 } else {
  note(EXAM.id, 'ok', 'no item repeats while fresh ones are available',
   rep ? (rep + ' repeats, all forced by bank size, in ' + totalServed + ' served')
       : (totalServed + ' items served'));
 }

 // ---- 6. how much of the bank can a student actually reach? -----------------------
 // An item that selection never reaches is an item we paid to write and nobody sees.
 // A skill that never gets served is worse: it is a hole in the diagnosis.
 const servedIds = new Set(runs.flatMap(r => r.served.map(q => q.id)));
 const reach = pct(servedIds.size, BANK.length);
 const servedSkills = new Set(runs.flatMap(r => r.served.map(q => q.skill)));
 const starved = SKILLS.filter(s => !servedSkills.has(s.id));
 note(EXAM.id, 'ok', 'bank reach across ' + runs.length + ' sittings',
  servedIds.size + ' of ' + BANK.length + ' items (' + reach + ' percent), ' +
  servedSkills.size + ' of ' + SKILLS.length + ' skills');
 if (starved.length) {
  note(EXAM.id, 'warn', 'every skill is reachable by practice',
   starved.length + ' never served: ' + starved.slice(0, 6).map(s => s.id).join(', '));
 }

 // Thin skills are the content gap this bot exists to surface. The count is what makes
 // it actionable: a skill with 3 items repeats inside a single session.
 const perSkill = {};
 BANK.forEach(q => { perSkill[q.skill] = (perSkill[q.skill] || 0) + 1; });
 const thin = SKILLS.map(s => ({ id: s.id, n: perSkill[s.id] || 0 }))
  .filter(s => s.n < 25).sort((a, b) => a.n - b.n);
 if (thin.length) {
  note(EXAM.id, 'warn', 'every skill has enough items to practise without repeating',
   thin.length + ' skills under 25 items: ' +
   thin.slice(0, 6).map(s => s.id + ' ' + s.n).join(', '));
 }

 // ---- 7. does the diagnosis actually diagnose? ------------------------------------
 // The product's real claim is not the score, it is "here is what to work on". So put in
 // a student who is strong everywhere except one section and ask the engine which section
 // is weakest. Getting this wrong sends a student to study the thing they are good at.
 // It sits SITTINGS students per section, not one. With one the verdict was three
 // coin flips: the diagnosis is right on 179 of 180 sittings measured across 60 seeds,
 // so at three sittings the check warned on about three percent of seeds by sampling
 // alone, and it did exactly that on a change to the GMAT verbal corpora that could not
 // have affected it (INC-0077). Every other check here already averages over 25
 // sittings. A check that flips on unrelated work is not strict, it is noisy, and the
 // cost is the real alarm nobody reads.
 //
 // The 90 percent bar is placed against a measurement rather than a feeling. Halving
 // the planted deficit from 1.6 to 0.8 takes the rate from 99 percent to 88, and 0.4
 // takes it to 64, so the bar sits between a diagnosis that works and one that has
 // visibly degraded, with the margin stated instead of implied.
 if (SECTIONS.length > 1) {
  const SITTINGS = 5;
  let right = 0, tried = 0;
  const missed = {};
  for (const target of SECTIONS) {
   for (let i = 0; i < SITTINGS; i++) {
    const r = sit(api, 0.6, target, rng);
    const abil = SECTIONS.map(s => ({ s, th: sectionAbility(r.state, s).theta }))
     .sort((a, b) => a.th - b.th);
    tried++;
    if (abil[0].s === target) right++;
    else missed[target] = (missed[target] || 0) + 1;
   }
  }
  const rate = right / tried;
  const detail = right + ' of ' + tried + ' sittings across ' + SECTIONS.length +
   ' sections' + (right < tried ? ', missed on ' +
    Object.entries(missed).map(([s, n]) => s + ' ' + n + 'x').join(', ') : '');
  if (rate >= 0.9) note(EXAM.id, 'ok', 'a planted weakness is found by the diagnosis', detail);
  else note(EXAM.id, rate < 0.5 ? 'fail' : 'warn',
   'a planted weakness is found by the diagnosis', detail);
 }
}

const specs = wanted.length
 ? wanted.map(w => harness.byId[w] || harness.byId[w === 'gmat' ? 'gmat-focus' : w])
 : harness.EXAM_FILES;
if (specs.some(s => !s)) {
 console.error('unknown exam; known: ' + harness.EXAM_FILES.map(e => e.id).join(', '));
 process.exit(2);
}

console.log('review bots, seed ' + SEED + (QUICK ? ' (quick)' : '') +
 ', ' + (TIERS.length * PER_TIER) + ' sittings of ' + (ROUNDS * ROUND) + ' items per exam');
specs.forEach(reviewExam);

const fails = findings.filter(f => f.level === 'fail');
const warns = findings.filter(f => f.level === 'warn');
console.log('\n' + '-'.repeat(60));
if (fails.length) {
 console.log(fails.length + ' FAILURE(S):');
 fails.forEach(f => console.log('  [' + f.exam + '] ' + f.label + ': ' + f.detail));
}
if (warns.length) {
 console.log(warns.length + ' warning(s):');
 warns.forEach(f => console.log('  [' + f.exam + '] ' + f.label + ': ' + f.detail));
}
if (!fails.length && !warns.length) console.log('every bot passed with nothing to report');
process.exit(fails.length ? 1 : 0);
