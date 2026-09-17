// Generated item rendering. Run with:
//   CHROMIUM_PATH=/opt/pw-browsers/chromium-*/chrome-linux/chrome \
//   NODE_PATH=/opt/node22/lib/node_modules node src/smoke_items.js
//
// src/test.js checks the banks as data: keys in range, choices distinct, no answer
// position or length bias. What it cannot check is whether the trainer can actually put
// an item on screen. Those are different failures. A two part item whose columns never
// render, a multi source item whose sources are dropped, a passage that pushes the page
// sideways on a phone: every one of them passes the data checks and is still a broken
// question for the person sitting in front of it.
//
// So this walks every generator schema in every exam's bank, renders one of its items
// through the real session path, and grades the computed key through the real submit
// path. A schema that cannot survive that round trip fails the build rather than the
// student.
const { chromium } = require('playwright');
const http = require('http');
const fs = require('fs');
const path0 = require('path');
const ROOT = path0.resolve(__dirname, '..');

const APPS = [['app', 5], ['sat/app', 4], ['gre/app', 5], ['lsat/app', 5], ['act/app', 4]];
const TYPES = { '.html': 'text/html', '.js': 'text/javascript', '.css': 'text/css',
                '.json': 'application/json', '.svg': 'image/svg+xml', '.png': 'image/png',
                '.webmanifest': 'application/manifest+json' };
const server = http.createServer((req, res) => {
  let rel = decodeURIComponent(req.url.split('?')[0]);
  if (rel.endsWith('/')) rel += 'index.html';
  const file = path0.join(ROOT, rel);
  if (!file.startsWith(ROOT) || !fs.existsSync(file) || fs.statSync(file).isDirectory()) {
    res.writeHead(404); res.end('not found'); return;
  }
  res.writeHead(200, { 'Content-Type': TYPES[path0.extname(file)] || 'application/octet-stream' });
  fs.createReadStream(file).pipe(res);
});
let PORT = 0;
const noise = t => /ERR_CERT_AUTHORITY_INVALID|fonts\.(googleapis|gstatic)\.com|Failed to fetch|net::ERR/.test(t);

(async () => {
  await new Promise(r => server.listen(0, '127.0.0.1', r));
  PORT = server.address().port;
  const b = await chromium.launch({ executablePath: process.env.CHROMIUM_PATH });
  let fail = 0, schemas = 0;
  const check = (name, ok, extra) => {
    if (!ok) { console.log('  FAIL: ' + name + (extra ? ' -> ' + extra : '')); fail++; }
  };

  for (const [app, nchoices] of APPS) {
    const ctx = await b.newContext({ viewport: { width: 390, height: 844 } });
    // Nothing in this test should reach the network, and telemetry least of all.
    await ctx.route('**/rest/v1/**', r => r.fulfill({ status: 201, contentType: 'application/json', body: '[]' }));
    await ctx.route('**/auth/v1/**', r => r.fulfill({ status: 200, contentType: 'application/json', body: '{}' }));
    const p = await ctx.newPage();
    const errs = [];
    p.on('pageerror', e => { if (!noise(e.message)) errs.push('pageerror: ' + e.message); });
    p.on('console', m => { if (m.type() === 'error' && !noise(m.text())) errs.push('console: ' + m.text()); });
    await p.goto('http://127.0.0.1:' + PORT + '/' + app + '/index.html', { waitUntil: 'load' });
    await p.waitForFunction(() => typeof BANK !== 'undefined' && BANK.length > 0, null, { timeout: 30000 });
    await p.evaluate(() => { if (document.getElementById('onb')) finishOnboarding(true); });
    await p.evaluate(() => { if (window.sfnConsent) sfnConsent(false); });

    const gens = await p.evaluate(() => {
      const seen = {};
      BANK.forEach(q => { if (q.gen && !seen[q.gen]) seen[q.gen] = q.id; });
      return seen;
    });
    const names = Object.keys(gens).sort();
    // A bank with no generated items has nothing for this test to walk. That is the LSAT
    // today: every item is hand written and carries no schema tag. Say so and move on,
    // rather than reporting an absence as a failure.

    for (const gen of names) {
      schemas++;
      const info = await p.evaluate((g) => {
        const q = BANK.find(x => x.gen === g);
        beginSession([q], 'drill');
        return { id: q.id, at: q.answerType || null, passage: !!q.passageHtml,
                 n: Array.isArray(q.choices) ? q.choices.length : 0 };
      }, gen);
      await p.waitForTimeout(90);
      const view = await p.evaluate(() => {
        const el = document.getElementById('v-study');
        return { stem: (el.querySelector('.stem') || {}).innerText || '',
                 opts: el.querySelectorAll('.opt').length,
                 radios: el.querySelectorAll('.tpa input[type=radio]').length,
                 selects: el.querySelectorAll('select').length,
                 spr: !!el.querySelector('#sprIn'),
                 tables: el.querySelectorAll('table.dtable').length,
                 submit: !!document.getElementById('submitBtn') };
      });
      const label = app + ' ' + gen + ' (' + info.id + ')';
      check(label + ' shows a stem', view.stem.trim().length > 10);
      check(label + ' offers a way to answer',
            view.opts > 0 || view.radios > 0 || view.selects > 0 || view.spr,
            JSON.stringify(view));
      check(label + ' offers a submit control', view.submit);
      if (!info.at) {
        check(label + ' offers ' + nchoices + ' options', view.opts === nchoices, 'opts ' + view.opts);
        check(label + ' bank row has ' + nchoices + ' choices', info.n === nchoices, 'choices ' + info.n);
      }
      if (info.at === 'tpa') {
        check(label + ' renders both columns', view.radios === info.n * 2, 'radios ' + view.radios);
      }
      if (info.passage) check(label + ' renders its source', view.tables >= 1, 'tables ' + view.tables);

      // The key the generator computed has to grade as correct through the real path.
      const graded = await p.evaluate(() => {
        const q = session.qs[0];
        if (q.answerType === 'tpa') session.tpa = [q.answer[0], q.answer[1]];
        else if (q.answerType === 'spr') session.spr = String(q.answer);
        else if (q.answerType === 'gi') session.gi = q.statements.map(s => s.answer);
        else if (q.answerType === 'ta') session.ta = q.statements.map(s => s.answer);
        else selectChoice(q.answer);
        submitAnswer();
        return session.pending ? session.pending.correct : null;
      });
      check(label + ' grades its own key as correct', graded === true, String(graded));

      // A passage that scrolls the page sideways on a phone is a broken question.
      const wide = await p.evaluate(() => document.documentElement.scrollWidth > window.innerWidth + 2);
      check(label + ' fits a 390px screen', !wide);
    }
    // Second pass: every ANSWER TYPE in the bank, generated or hand written. A schema
    // sweep misses hand written items entirely, and that is how sentence equivalence
    // shipped unanswerable: it rendered as six single pick buttons, currentAnswer handed
    // back one index, and the grader wanted a pair, so the item was marked wrong however
    // well it was answered. This asserts that the keyed answer grades as correct for one
    // item of every type the bank actually contains.
    const kinds = await p.evaluate(() => {
      const seen = {};
      BANK.forEach(q => { const k = q.answerType || 'mc'; if (!seen[k]) seen[k] = q.id; });
      return seen;
    });
    for (const kind of Object.keys(kinds).sort()) {
      const graded = await p.evaluate((k) => {
        const q = BANK.find(x => (x.answerType || 'mc') === k);
        beginSession([q], 'drill');
        if (k === 'tpa') session.tpa = [q.answer[0], q.answer[1]];
        else if (k === 'se') q.answer.forEach(i => toggleSE(i));
        else if (k === 'spr') session.spr = String(q.answer);
        else if (k === 'gi') session.gi = q.statements.map(s => s.answer);
        else if (k === 'ta') session.ta = q.statements.map(s => s.answer);
        else selectChoice(q.answer);
        const before = JSON.stringify(currentAnswer(q));
        submitAnswer();
        return { id: q.id, read: before, correct: session.pending ? session.pending.correct : null };
      }, kind);
      check(app + ' answer type ' + kind + ' reads the learner\'s answer back',
            graded.read !== 'null' && graded.read !== undefined, graded.id + ' -> ' + graded.read);
      check(app + ' answer type ' + kind + ' grades its key as correct (' + graded.id + ')',
            graded.correct === true, String(graded.correct));
    }
    check(app + ' threw no console errors across ' + names.length + ' schemas',
          errs.length === 0, errs.slice(0, 3).join(' | '));
    console.log('  ' + app + ': ' + names.length + ' schemas and '
                + Object.keys(kinds).length + ' answer types rendered and graded');
    await ctx.close();
  }

  await b.close();
  server.close();
  console.log(fail ? '\nFAILED (' + fail + ') across ' + schemas + ' schemas'
                   : '\nall ' + schemas + ' generated schemas render and grade correctly');
  process.exit(fail ? 1 : 0);
})();
