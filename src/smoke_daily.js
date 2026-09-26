// The daily question, played end to end in a browser. Run after a build:
//   NODE_PATH=/opt/node22/lib/node_modules node src/smoke_daily.js
//
// What only a browser can show: that the live page picks the question for the visitor's
// own date, that answering records the day and draws the explanation, that a second visit
// cannot re-answer, that the share text never carries the question or the answer, that the
// hub and the trainer read the same streak, and that none of it pushes a phone sideways.
const { chromium } = require('playwright');
const { chromiumPath } = require('./chromium_path.js');
const http = require('http');
const fs = require('fs');
const path = require('path');
const ROOT = path.resolve(__dirname, '..');

const TYPES = { '.html': 'text/html', '.js': 'text/javascript', '.css': 'text/css', '.json': 'application/json',
                '.xml': 'application/xml', '.svg': 'image/svg+xml', '.png': 'image/png' };
const server = http.createServer((req, res) => {
  let rel = decodeURIComponent(req.url.split('?')[0]);
  if (rel.endsWith('/')) rel += 'index.html';
  const file = path.join(ROOT, rel);
  if (!file.startsWith(ROOT) || !fs.existsSync(file) || fs.statSync(file).isDirectory()) { res.writeHead(404); res.end(); return; }
  res.writeHead(200, { 'Content-Type': TYPES[path.extname(file)] || 'application/octet-stream' });
  fs.createReadStream(file).pipe(res);
});

let failures = 0;
const ok = (cond, msg) => { console.log('  ' + (cond ? 'ok  ' : 'FAIL') + ' ' + msg); if (!cond) failures++; };

(async () => {
  if (!fs.existsSync(path.join(ROOT, 'daily', 'gmat', 'index.html'))) {
    console.log('no built daily/; run python3 src/build.py first'); process.exit(1);
  }
  await new Promise(r => server.listen(0, r));
  const base = 'http://127.0.0.1:' + server.address().port;
  const browser = await chromium.launch({ executablePath: chromiumPath() });

  // The date to play on: one the live page actually carries, read from its own data.
  const livePath = path.join(ROOT, 'daily', 'gmat', 'index.html');
  const liveHtml = fs.readFileSync(livePath, 'utf8');
  const payload = JSON.parse(liveHtml.match(/<script type="application\/json" id="daily-data">([\s\S]*?)<\/script>/)[1]);
  const day = payload.days[Math.min(1, payload.days.length - 1)];
  const item = day.item;
  console.log('\nplaying the GMAT question for ' + day.date + ' (' + item.id + ')');

  for (const width of [390, 1280]) {
    console.log('\n=== viewport ' + width + ' ===');
    const ctx = await browser.newContext({ viewport: { width, height: 900 } });
    // A returning visitor who has already made a consent choice, so the modal does not sit
    // over the page (INC-0110).
    await ctx.addInitScript(() => {
      try { localStorage.setItem('sfn_consent_v1', JSON.stringify({ analytics: false, ts: '', v: 1 })); } catch (e) {}
    });
    // Telemetry never leaves a test. The posted rows are kept so their shape can be checked.
    const posted = [];
    await ctx.route('**/rest/v1/**', r => { try { posted.push({ url: r.request().url(), body: JSON.parse(r.request().postData() || 'null') }); } catch (e) {}
      r.fulfill({ status: 201, contentType: 'application/json', body: '[]' }); });
    const page = await ctx.newPage();
    const errs = [];
    page.on('pageerror', e => errs.push(e.message));
    page.on('console', m => { if (m.type() === 'error' && !/fonts\.(googleapis|gstatic)|ERR_CERT|Failed to fetch|net::ERR/.test(m.text())) errs.push(m.text()); });
    await page.clock.setFixedTime(new Date(day.date + 'T12:00:00'));
    // Capture the share text instead of opening a share sheet.
    await page.addInitScript(() => {
      window.__shared = null;
      navigator.share = t => { window.__shared = t.text; return Promise.resolve(); };
    });

    await page.goto(base + '/daily/gmat/');
    const dateLabel = await page.textContent('#qdate');
    ok(/^Today, /.test(dateLabel), 'the live page shows today\'s question (' + dateLabel.trim() + ')');
    const stem = await page.textContent('#q .stem');
    ok(stem.trim() === item.stem.trim(), 'it is the scheduled question for the visitor\'s date');
    const opts = await page.$$('#q .opt');
    ok(opts.length === item.choices.length, opts.length + ' answer buttons');

    if (width === 390) {
      // Answer wrong on purpose on the phone, so the missed path and the streak rule are
      // both exercised: a wrong answer still counts as a day.
      const wrongIdx = item.answer === 0 ? 1 : 0;
      await opts[wrongIdx].click();
      await page.waitForSelector('.result');
      ok(await page.$('.result.no') !== null, 'a wrong answer is marked wrong');
      ok((await page.textContent('#res')).includes('The answer is ' + 'ABCDE'[item.answer]), 'the correct letter is shown after answering');
      ok((await page.textContent('#res')).includes(item.expl.slice(0, 40)), 'the explanation is shown');
      ok((await page.textContent('#streak')).includes('1'), 'the day counts toward the streak even though it was wrong');
      // One unlinkable telemetry row, and nothing in it that could identify anyone.
      const rows = posted.filter(x => /item_events/.test(x.url));
      const allowed = ['exam', 'qid', 'skill', 'section', 'diff', 'chosen', 'correct', 'secs', 'mode'];
      const extra = rows.length ? Object.keys(rows[0].body).filter(k => !allowed.includes(k)) : ['(none posted)'];
      ok(rows.length === 1 && rows[0].body.qid === item.id && rows[0].body.mode === 'daily' && extra.length === 0,
         'one unlinkable item_events row is posted' + (extra.length ? ' (unexpected: ' + extra.join(', ') + ')' : ''));
      await page.click('#share');
      const shared = await page.evaluate(() => window.__shared);
      ok(!!shared && shared.includes('startfromnowhere.com/daily/gmat/'), 'share text is produced and links the page');
      const leaks = item.choices.filter(c => c.length > 3 && shared.includes(c)).length + (shared.includes(item.stem.slice(0, 30)) ? 1 : 0)
        + (/answer is|correct answer/i.test(shared) ? 1 : 0);
      ok(leaks === 0, 'share text carries no question, choice or answer');
      // A second visit cannot re-answer and shows the recorded result.
      await page.reload();
      await page.waitForSelector('.result');
      const disabled = await page.$$eval('#q .opt', bs => bs.every(b => b.disabled));
      ok(disabled, 'returning the same day shows the recorded answer and does not allow another');
      // The hub reads the same record.
      await page.goto(base + '/daily/');
      const st = await page.textContent('#ex-gmat .st');
      ok(/Answered today/.test(st), 'the hub shows the GMAT card as answered (' + st.trim() + ')');
      const sat = await page.textContent('#ex-sat .st');
      ok(/Not answered/.test(sat), 'and the SAT card as not yet answered');
    } else {
      await opts[item.answer].click();
      await page.waitForSelector('.result.ok');
      ok(true, 'a right answer is marked right');
    }

    // An archive page: the question, and the answer behind a disclosure. A build dated
    // before the schedule's first day has none yet, which is correct rather than a failure.
    const archive = fs.readdirSync(path.join(ROOT, 'daily', 'gmat')).filter(d => /^\d{4}-\d{2}-\d{2}$/.test(d)).sort()[0];
    if (archive) {
      await page.goto(base + '/daily/gmat/' + archive + '/');
      ok(await page.$('details.ans') !== null, 'archive page ' + archive + ' carries its answer and explanation');
      ok((await page.textContent('h1')).includes('Question of the Day'), 'archive page is titled');
    } else {
      console.log('  note no archive pages yet: this build predates the first scheduled day');
    }

    for (const p of ['/daily/', '/daily/gmat/', '/daily/act/', '/daily/lsat/'].concat(archive ? ['/daily/gmat/' + archive + '/'] : [])) {
      await page.goto(base + p);
      const over = await page.evaluate(() => document.documentElement.scrollWidth - window.innerWidth);
      ok(over <= 0, p + ' has no sideways scroll at ' + width + 'px' + (over > 0 ? ' (' + over + 'px over)' : ''));
    }
    ok(errs.length === 0, 'no page errors' + (errs.length ? ': ' + errs.slice(0, 3).join(' | ') : ''));
    await ctx.close();
  }

  // The trainer's Question of the Day is the same scheduled question, and a day answered
  // in the app is a day answered on /daily/: one streak, not two.
  console.log('\n=== trainer question of the day ===');
  const schedule = JSON.parse(fs.readFileSync(path.join(ROOT, 'data', 'daily', 'schedule.json'), 'utf8'));
  for (const [app, examId, slug] of [['app', 'gmat-focus', 'gmat'], ['act/app', 'act', 'act']]) {
    const ctx = await browser.newContext({ viewport: { width: 390, height: 844 } });
    await ctx.route('**/rest/v1/**', r => r.fulfill({ status: 201, contentType: 'application/json', body: '[]' }));
    await ctx.route('**/auth/v1/**', r => r.fulfill({ status: 200, contentType: 'application/json', body: '{}' }));
    const page = await ctx.newPage();
    const errs = [];
    page.on('pageerror', e => errs.push(e.message));
    await page.clock.setFixedTime(new Date(day.date + 'T12:00:00'));
    await page.goto(base + '/' + app + '/index.html', { waitUntil: 'load' });
    await page.waitForFunction(() => typeof BANK !== 'undefined' && BANK.length > 0, null, { timeout: 30000 });
    await page.evaluate(() => { if (document.getElementById('onb')) finishOnboarding(true); });
    await page.evaluate(() => { if (window.sfnConsent) sfnConsent(false); });
    const want = (schedule.days[day.date] || {})[examId];
    const got = await page.evaluate(() => { const p = qotdPick(); return { id: p.q && p.q.id, today: p.today, scheduled: p.scheduled }; });
    ok(got.id === want && got.today && got.scheduled, app + ' serves the scheduled ' + examId + ' question for ' + day.date + ' (' + got.id + ')');
    const graded = await page.evaluate(() => {
      startQotd();
      const q = session.qs[0];
      selectChoice(q.answer);
      submitAnswer();
      return session.pending ? session.pending.correct : null;
    });
    ok(graded === true, app + ' grades the scheduled key as correct');
    const rec = await page.evaluate(s => SFNDaily.days(s)[SFNDaily.today()] || null, slug);
    ok(rec && rec.c === 1, app + ' records the day where /daily/ reads it');
    await page.goto(base + '/daily/');
    const st = await page.textContent('#ex-' + slug + ' .st');
    ok(/Solved today/.test(st), 'the /daily/ hub shows the ' + slug + ' day answered in the trainer (' + st.trim() + ')');
    ok(errs.length === 0, app + ' raised no page errors' + (errs.length ? ': ' + errs.slice(0, 2).join(' | ') : ''));
    await ctx.close();
  }

  // Every exam's feed is XML, with one item per archived day (none before the first day).
  for (const slug of ['gmat', 'sat', 'gre', 'lsat', 'act']) {
    const xml = fs.readFileSync(path.join(ROOT, 'daily', slug, 'feed.xml'), 'utf8');
    const days = fs.readdirSync(path.join(ROOT, 'daily', slug)).filter(d => /^\d{4}-\d{2}-\d{2}$/.test(d)).length;
    const items = (xml.match(/<item>/g) || []).length;
    ok(/^<\?xml/.test(xml) && items === Math.min(30, days), slug + ' feed carries ' + items + ' item(s) for ' + days + ' archived day(s)');
  }

  await browser.close();
  server.close();
  console.log(failures ? '\n' + failures + ' FAILED' : '\nall daily checks passed');
  process.exit(failures ? 1 : 0);
})().catch(e => { console.error(e); process.exit(1); });
