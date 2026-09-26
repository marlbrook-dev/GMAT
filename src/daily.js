// The daily question: one per exam per date, the same for everyone, never changing once
// scheduled.
//
//   node src/daily.js extend [--days 120]   append days to data/daily/schedule.json
//   node src/daily.js check                 validate the schedule against the banks
//   node src/daily.js export FROM TO        print the scheduled items for FROM..TO as JSON
//
// Why a committed schedule rather than a hash of the date. The trainer's first Question of
// the Day was pool[hash(date) % pool.length], and pool was the live BANK, which grows when
// the async bank chunk arrives. Two students opening the app on the same morning, one
// before the chunk loaded and one after, were served different questions under a card
// that said "picked for everyone today", and any deploy that changed the bank changed the
// day's question under anyone who had already answered it. A published archive makes both
// worse: a page for September 30 must show the same question in December.
//
// So the schedule is data. Each date names one item per exam, it is written once and only
// ever appended to, and the build fails if a scheduled item disappears from its bank.
//
// Only hand-written items are scheduled. A generated item's id is a position in a seeded
// run, and changing a generator can put different content behind the same id; a
// hand-written id is the item. Items are chosen in a fixed order derived from a hash of
// the item id, rotating through the exam's sections, taking at most one question per
// passage until every passage has been used, and never repeating an item. When a section
// runs out it is skipped; when every section has run out, extend stops and says so rather
// than quietly starting over, because a repeat on a dated public page is a duplicate page.
const fs = require('fs');
const path = require('path');
const harness = require('./exam_harness.js');

const ROOT = path.resolve(__dirname, '..');
const FILE = path.join(ROOT, 'data', 'daily', 'schedule.json');

// URL slug per exam id, matching data/exams.json and the rest of the site.
const SLUG = { 'gmat-focus': 'gmat', sat: 'sat', gre: 'gre', lsat: 'lsat', act: 'act' };

// A daily question stands alone on a public page, so it needs one answer to grade, an
// explanation to show, and any passage or figure it depends on carried on the item itself.
// Multi-part formats (two-part analysis, table analysis, grid-ins, multi-source tabs) need
// the trainer's interface and stay there.
function eligible(q) {
  return Array.isArray(q.choices) && q.choices.length >= 4 && typeof q.answer === 'number'
    && !q.answerType && q.type !== 'MSR' && !!q.expl
    && (!q.passageId || !!q.passage || !!q.passageHtml);
}

// FNV-1a with a murmur3 finalizer, so the order is a pure function of the item id and
// survives any reshuffle of the bank files. FNV-1a alone barely separates ids that differ
// in their last character, and the first schedule it produced walked Q220, Q221, V221,
// V220 in near sequence; the finalizer spreads those apart.
function hash(s) {
  let h = 0x811c9dc5;
  for (let i = 0; i < s.length; i++) { h ^= s.charCodeAt(i); h = Math.imul(h, 0x01000193) >>> 0; }
  h ^= h >>> 16; h = Math.imul(h, 0x85ebca6b) >>> 0;
  h ^= h >>> 13; h = Math.imul(h, 0xc2b2ae35) >>> 0;
  h ^= h >>> 16;
  return h >>> 0;
}

function loadHandWritten(examId) {
  const spec = Object.assign({}, harness.byId[examId], { gen: null });
  return harness.load(spec);
}

function readSchedule() {
  if (!fs.existsSync(FILE)) return null;
  return JSON.parse(fs.readFileSync(FILE, 'utf8'));
}

function writeSchedule(s) {
  fs.mkdirSync(path.dirname(FILE), { recursive: true });
  // One date per line keeps a diff readable when days are appended.
  const dates = Object.keys(s.days).sort();
  const body = dates.map(d => '  ' + JSON.stringify(d) + ': ' + JSON.stringify(s.days[d])).join(',\n');
  const head = Object.keys(s).filter(k => k !== 'days')
    .map(k => ' ' + JSON.stringify(k) + ': ' + JSON.stringify(s[k]) + ',').join('\n');
  fs.writeFileSync(FILE, '{\n' + head + '\n "days": {\n' + body + '\n }\n}\n');
}

const addDays = (iso, n) => {
  const d = new Date(iso + 'T00:00:00Z'); d.setUTCDate(d.getUTCDate() + n);
  return d.toISOString().slice(0, 10);
};

function extend(days) {
  let s = readSchedule();
  if (!s) {
    s = { _note: 'Written by src/daily.js extend and only ever appended to. One hand-written item per exam per date; see that file for why.',
          start: process.env.DAILY_START || new Date().toISOString().slice(0, 10), days: {} };
  }
  const exams = Object.keys(SLUG);
  const banks = {};
  exams.forEach(id => { banks[id] = loadHandWritten(id); });
  const last = Object.keys(s.days).sort().pop();
  let date = last ? addDays(last, 1) : s.start;
  const stopped = [];
  for (let n = 0; n < days; n++, date = addDays(date, 1)) {
    const row = {};
    for (const id of exams) {
      const api = banks[id];
      const used = new Set(Object.values(s.days).map(r => r[id]).filter(Boolean));
      const passUse = {};
      api.BANK.forEach(q => { if (used.has(q.id) && q.passageId) passUse[q.passageId] = (passUse[q.passageId] || 0) + 1; });
      const index = Object.keys(s.days).length;
      // Rotate through sections in the exam's own order, skipping any with nothing left.
      const secs = api.SECTIONS.filter(sec => api.BANK.some(q => q.section === sec && eligible(q) && !used.has(q.id)));
      if (!secs.length) { stopped.push(SLUG[id]); continue; }
      const order = api.SECTIONS.filter(sec => secs.includes(sec));
      const sec = order[index % order.length];
      const cands = api.BANK.filter(q => q.section === sec && eligible(q) && !used.has(q.id))
        .sort((a, b) => ((passUse[a.passageId] || 0) - (passUse[b.passageId] || 0))
          || (hash(id + ':' + a.id) - hash(id + ':' + b.id)));
      row[id] = cands[0].id;
    }
    if (stopped.length) {
      console.log('daily: stopped at ' + date + '; no unscheduled items left for ' + stopped.join(', ') +
        '. Write more hand-written items for that exam, then extend again.');
      break;
    }
    s.days[date] = row;
  }
  writeSchedule(s);
  const all = Object.keys(s.days).sort();
  console.log('daily: schedule runs ' + all[0] + ' to ' + all[all.length - 1] + ' (' + all.length + ' days)');
}

// Every scheduled id must still be an eligible hand-written item. Returns problems, and a
// runway figure: how many scheduled days remain after `today`.
function check(today) {
  const s = readSchedule();
  if (!s) return { problems: ['no data/daily/schedule.json; run node src/daily.js extend'], runway: 0 };
  const problems = [];
  const byExam = {};
  for (const id of Object.keys(SLUG)) {
    const api = loadHandWritten(id);
    byExam[id] = new Map(api.BANK.map(q => [q.id, q]));
  }
  const seen = {};
  for (const [date, row] of Object.entries(s.days)) {
    if (!/^\d{4}-\d{2}-\d{2}$/.test(date)) problems.push('bad date ' + date);
    for (const id of Object.keys(SLUG)) {
      const qid = row[id];
      if (!qid) { problems.push(date + ': no ' + id + ' item'); continue; }
      const q = byExam[id].get(qid);
      if (!q) problems.push(date + ': ' + id + ' item ' + qid + ' is not in the hand-written bank');
      else if (!eligible(q)) problems.push(date + ': ' + id + ' item ' + qid + ' can no longer stand alone');
      const k = id + ':' + qid;
      if (seen[k]) problems.push(date + ': ' + id + ' item ' + qid + ' was already used on ' + seen[k]);
      seen[k] = date;
    }
  }
  const runway = Object.keys(s.days).filter(d => d > today).length;
  return { problems, runway, start: s.start, last: Object.keys(s.days).sort().pop() };
}

function exportRange(from, to) {
  const s = readSchedule();
  if (!s) throw new Error('no schedule');
  const out = { start: s.start, exams: {}, days: [] };
  const apis = {};
  for (const id of Object.keys(SLUG)) {
    const api = loadHandWritten(id);
    apis[id] = { byId: new Map(api.BANK.map(q => [q.id, q])), api };
    const skills = {};
    api.SKILLS.forEach(k => { skills[k.id] = k.label; });
    const sections = {};
    Object.keys(api.SECTION_META).forEach(k => { sections[k] = api.SECTION_META[k].name; });
    out.exams[id] = { slug: SLUG[id], name: api.EXAM.name, short: api.EXAM.short,
                      appPath: api.EXAM.appPath, choices: api.EXAM.choices, skills, sections };
  }
  for (const date of Object.keys(s.days).sort()) {
    if (date < from || date > to) continue;
    const row = { date, items: {} };
    for (const id of Object.keys(SLUG)) {
      const q = apis[id].byId.get(s.days[date][id]);
      if (!q) continue;
      row.items[id] = { id: q.id, section: q.section, type: q.type, sub: q.sub || null,
        skill: q.skill, diff: q.diff, stem: q.stem, choices: q.choices, answer: q.answer,
        expl: q.expl, wrong: q.wrong || '', passage: q.passage || '', passageHtml: q.passageHtml || '' };
    }
    out.days.push(row);
  }
  return out;
}

if (require.main === module) {
  const [cmd, a, b] = process.argv.slice(2);
  if (cmd === 'extend') {
    const i = process.argv.indexOf('--days');
    extend(i > 0 ? Number(process.argv[i + 1]) : 120);
  } else if (cmd === 'check') {
    const r = check(new Date().toISOString().slice(0, 10));
    r.problems.forEach(p => console.log('  FAIL ' + p));
    console.log('daily: ' + (r.problems.length ? r.problems.length + ' problem(s)' : 'schedule clean') +
      ', ' + r.runway + ' days scheduled after today');
    process.exit(r.problems.length ? 1 : 0);
  } else if (cmd === 'export') {
    process.stdout.write(JSON.stringify(exportRange(a, b)));
  } else {
    console.log('usage: node src/daily.js extend [--days N] | check | export FROM TO');
    process.exit(2);
  }
}

module.exports = { eligible, check, exportRange, SLUG };
