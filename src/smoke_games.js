// The games, played. Run after a build:
//   NODE_PATH=/opt/node22/lib/node_modules node src/smoke_games.js
//
// Seven games shipped with no suite that ever started one. Each has its own render, its own
// timers and its own record in state.games, and a game that throws on its third question or
// never saves a best is invisible to every data check. So this plays the three that use real
// bank questions to their end screens in every trainer, starts and quits the four card games,
// and checks the order, the personal bests, phone width and page errors.
const { chromium } = require('playwright');
const { chromiumPath } = require('./chromium_path.js');
const http = require('http');
const fs = require('fs');
const path = require('path');
const ROOT = path.resolve(__dirname, '..');

const TYPES = { '.html': 'text/html', '.js': 'text/javascript', '.json': 'application/json', '.png': 'image/png', '.svg': 'image/svg+xml' };
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
const APPS = [['app', 'GMAT'], ['sat/app', 'SAT'], ['gre/app', 'GRE'], ['lsat/app', 'LSAT'], ['act/app', 'ACT']];

(async () => {
  await new Promise(r => server.listen(0, r));
  const base = 'http://127.0.0.1:' + server.address().port;
  const browser = await chromium.launch({ executablePath: chromiumPath() });

  for (const [app, label] of APPS) {
    console.log('\n=== ' + label + ' ===');
    const ctx = await browser.newContext({ viewport: { width: 390, height: 844 } });
    await ctx.route('**/rest/v1/**', r => r.fulfill({ status: 201, contentType: 'application/json', body: '[]' }));
    await ctx.route('**/auth/v1/**', r => r.fulfill({ status: 200, contentType: 'application/json', body: '{}' }));
    const page = await ctx.newPage();
    const errs = [];
    page.on('pageerror', e => errs.push(e.message));
    // The games wait on setTimeout between questions; a controlled clock lets the suite
    // advance through them instead of sleeping.
    await page.clock.install();
    await page.goto(base + '/' + app + '/index.html', { waitUntil: 'load' });
    await page.waitForFunction(() => typeof BANK !== 'undefined' && BANK.length > 0, null, { timeout: 30000 });
    await page.evaluate(() => { if (document.getElementById('onb')) finishOnboarding(true); if (window.sfnConsent) sfnConsent(false); });

    // The hub: every game in the exam's own order, and nothing pushed sideways.
    const hub = await page.evaluate(() => {
      show('games'); renderGames();
      const titles = [...document.querySelectorAll('#v-games .gcard .card-title')].map(e => e.textContent.trim());
      return { titles, order: (EXAM.gameplan || {}).order || [], over: document.documentElement.scrollWidth - innerWidth };
    });
    ok(hub.order.length === 7 && hub.titles.length >= 7, 'the hub shows all ' + hub.order.length + ' games (' + hub.titles.slice(0, 7).join(', ') + ')');
    ok(hub.over <= 0, 'the games hub has no sideways scroll at 390px');

    // Survival: five right, then three wrong. Score is the count right; the time spent is
    // not part of it.
    await page.evaluate(() => gmStartSurvival());
    for (let k = 0; k < 8; k++) {
      const q = await page.evaluate(() => gm.q && { id: gm.q.id, answer: gm.q.answer, n: gm.q.choices.length });
      if (!q) break;
      await page.evaluate(([right, a, n]) => gmSurvivalAnswer(right ? a : (a + 1) % n), [k < 5, q.answer, q.n]);
      await page.clock.runFor(2000);
    }
    const sv = await page.evaluate(() => ({ best: (state.games.survival || {}).best, plays: (state.games.survival || {}).plays,
      text: document.getElementById('v-games').innerText, on: gm.on }));
    ok(!sv.on && sv.best === 5 && sv.plays === 1, 'Survival ends at the third miss with a best of 5 (' + sv.best + ')');
    ok(/New Personal Best/.test(sv.text), 'the first finished run is announced as a personal best');

    // Boss round: five right clears it and records a best.
    await page.evaluate(() => gmStartBoss());
    for (let k = 0; k < 5; k++) {
      const a = await page.evaluate(() => gm.on && gm.kind === 'boss' ? gm.qs[gm.i].answer : null);
      if (a === null) break;
      await page.evaluate(x => gmBossAnswer(x), a);
      await page.clock.runFor(1600);
    }
    const bo = await page.evaluate(() => ({ best: (state.games.boss || {}).best, wins: (state.games.boss || {}).wins, text: document.getElementById('v-games').innerText }));
    ok(bo.wins === 1 && bo.best > 0 && /Boss Cleared/.test(bo.text), 'Boss Round clears on five right and records a best (' + bo.best + ')');

    // The Ladder: eight rungs, all right.
    await page.evaluate(() => gmStartLadder());
    for (let k = 0; k < 8; k++) {
      const a = await page.evaluate(() => gm.on && gm.kind === 'ladder' && gm.q ? gm.q.answer : null);
      if (a === null) break;
      await page.evaluate(x => gmLadderAnswer(x), a);
      await page.clock.runFor(1600);
    }
    const ld = await page.evaluate(() => ({ plays: (state.games.ladder || {}).plays, peak: (state.games.ladder || {}).peak, text: document.getElementById('v-games').innerText }));
    ok(ld.plays === 1 && ld.peak === 5 && /Clean Climb/.test(ld.text), 'The Ladder climbs eight rungs to level 5 (peak ' + ld.peak + ')');

    // The card games start and quit cleanly.
    for (const [start, name] of [["gmStartMatch('ALL')", 'Match'], ["gmStartMemory('ALL')", 'Memory'], ["gmStartBlitz('ALL')", 'Blitz'], ['gmStartCrunch()', 'Number Crunch']]) {
      const r = await page.evaluate(s => { try { eval(s); const on = gm.on; const over = document.documentElement.scrollWidth - innerWidth; gmQuit(); return { on, over }; } catch (e) { return { err: e.message }; } }, start);
      ok(!r.err && r.on && r.over <= 0, name + ' starts, fits the phone and quits' + (r.err ? ': ' + r.err : ''));
    }

    // Bests survive a reload, which is the whole point of a personal best.
    await page.evaluate(() => persist());
    await page.reload({ waitUntil: 'load' });
    await page.waitForFunction(() => typeof state !== 'undefined' && state.games, null, { timeout: 30000 });
    const kept = await page.evaluate(() => ({ s: (state.games.survival || {}).best, b: (state.games.boss || {}).best }));
    ok(kept.s === 5 && kept.b === bo.best, 'personal bests survive a reload');
    ok(errs.length === 0, 'no page errors' + (errs.length ? ': ' + errs.slice(0, 2).join(' | ') : ''));
    await ctx.close();
  }

  await browser.close();
  server.close();
  console.log(failures ? '\n' + failures + ' FAILED' : '\nall game checks passed');
  process.exit(failures ? 1 : 0);
})().catch(e => { console.error(e); process.exit(1); });
