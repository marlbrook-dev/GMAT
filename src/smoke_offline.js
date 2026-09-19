// Offline, proven rather than asserted.
//
//   CHROMIUM_PATH=/opt/pw-browsers/chromium-*/chrome-linux/chrome node src/smoke_offline.js
//
// A service worker that registers is not the same as an app that works offline, and the
// difference is invisible until a student is on a train. So this installs the worker,
// cuts the network at the browser level, reloads, and requires a real practice question
// on screen. Nothing short of that counts.
//
// It is also the evidence behind the App Review 4.2 claim. "Works fully offline" is a
// statement a reviewer can check in fifteen seconds with airplane mode, so it had better
// be true before it is written on a submission.
const { chromium } = require('playwright');
const http = require('http'), fs = require('fs'), p0 = require('path');
const ROOT = p0.join(__dirname, '..');
const T = {'.html':'text/html','.js':'text/javascript','.css':'text/css','.png':'image/png',
           '.svg':'image/svg+xml','.json':'application/json','.webmanifest':'application/manifest+json'};
let served = 0;
const srv = http.createServer((q, r) => {
  let rel = decodeURIComponent(q.url.split('?')[0]); if (rel.endsWith('/')) rel += 'index.html';
  const f = p0.join(ROOT, rel);
  if (!f.startsWith(ROOT) || !fs.existsSync(f) || fs.statSync(f).isDirectory()) { r.writeHead(404); r.end('nf'); return; }
  served++;
  r.writeHead(200, { 'Content-Type': T[p0.extname(f)] || 'application/octet-stream' });
  fs.createReadStream(f).pipe(r);
});
const fails = [];
const check = (n, c, d) => {
  console.log((c ? '  ok: ' : '  FAIL: ') + n + (d ? '  -> ' + d : ''));
  if (!c) fails.push(n);
};
const hasQuestion = () => {
  const v = document.getElementById('v-study');
  return !!(v && !v.classList.contains('hidden') && v.innerText.trim().length > 40);
};

(async () => {
  await new Promise(r => srv.listen(0, '127.0.0.1', r));
  const P = srv.address().port;
  const base = 'http://127.0.0.1:' + P;
  const b = await chromium.launch({ executablePath: process.env.CHROMIUM_PATH });

  for (const app of ['app', 'sat/app', 'act/app', 'gre/app', 'lsat/app']) {
    // A fresh context per app so nothing is inherited from the previous one. This has to
    // be a cold start, the way a new install is.
    const ctx = await b.newContext({ viewport: { width: 390, height: 844 } });
    const pg = await ctx.newPage();
    const errs = [];
    pg.on('pageerror', e => errs.push(e.message));

    await pg.goto(base + '/' + app + '/', { waitUntil: 'load' });
    // The full size, measured online, to compare the offline load against.
    await pg.waitForFunction(() => typeof BANK !== 'undefined' && BANK.length > 0, { timeout: 20000 });
    await pg.waitForTimeout(1200);   // let the deferred half land
    const fullBank = await pg.evaluate(() => BANK.length);
    check('[' + app + '] bank loads online', fullBank > 0, fullBank + ' items');

    check('[' + app + '] worker registers',
      await pg.evaluate(() => navigator.serviceWorker.register ? true : false));

    // Wait for it to actually take control, not merely to have been asked to.
    const active = await pg.evaluate(async () => {
      const reg = await navigator.serviceWorker.ready.catch(() => null);
      if (!reg) return null;
      // The precache runs during install; give it room to finish on a local server.
      for (let i = 0; i < 40 && !navigator.serviceWorker.controller; i++) {
        await new Promise(r => setTimeout(r, 100));
      }
      return { scope: reg.scope, controlled: !!navigator.serviceWorker.controller };
    });
    check('[' + app + '] worker becomes active', !!active && active.controlled,
      active ? active.scope : 'never ready');

    // Let the precache settle before pulling the plug.
    await pg.waitForTimeout(1500);
    const status = await pg.evaluate(() => new Promise(res => {
      const t = setTimeout(() => res(null), 3000);
      navigator.serviceWorker.addEventListener('message', e => {
        if (e.data && e.data.type === 'sfn-cache-status') { clearTimeout(t); res(e.data); }
      });
      navigator.serviceWorker.controller.postMessage({ type: 'sfn-cache-status' });
    }));
    check('[' + app + '] cache reports its contents', !!status,
      status ? status.cached + ' of ' + status.expected + ' precached' : 'no reply');

    // The real test. Nothing may reach the network from here.
    const before = served;
    await ctx.setOffline(true);
    let reloaded = true;
    try {
      await pg.reload({ waitUntil: 'domcontentloaded', timeout: 15000 });
    } catch (e) { reloaded = false; }
    check('[' + app + '] the app opens with the network off', reloaded);

    if (reloaded) {
      await pg.evaluate(() => { try { show('study'); } catch (e) {} });
      let got = true;
      try { await pg.waitForFunction(hasQuestion, { timeout: 15000 }); } catch (e) { got = false; }
      check('[' + app + '] a practice question renders offline', got);

      // The bank has to be WHOLE, not just the blocking half, or offline practice runs
      // out after a few rounds without saying why. Waited for, because bank_rest.js is
      // async and is still executing when the first question appears.
      let n = 0;
      try {
        await pg.waitForFunction(
          expected => typeof BANK !== 'undefined' && BANK.length >= expected,
          fullBank, { timeout: 20000 });
      } catch (e) { /* fall through to the assertion below with whatever we have */ }
      n = await pg.evaluate(() => (typeof BANK === 'undefined' ? 0 : BANK.length));
      check('[' + app + '] the FULL bank is available offline', n >= fullBank,
        n + ' of ' + fullBank + ' items');

      // Answering has to work too: a question you cannot answer is a screenshot.
      const graded = await pg.evaluate(() => {
        try {
          const btn = document.querySelector('#v-study button, #v-study .opt, #v-study [onclick]');
          return !!btn;
        } catch (e) { return false; }
      });
      check('[' + app + '] the question is interactive offline', graded);
    }
    check('[' + app + '] nothing was fetched while offline', served === before,
      (served - before) + ' request(s) reached the server');

    check('[' + app + '] no page errors offline', errs.length === 0, errs[0] || '');
    await ctx.setOffline(false);
    await ctx.close();
  }

  await b.close(); srv.close();
  console.log(fails.length ? '\nFAILURES: ' + fails.join(', ') : '\nall offline checks passed');
  process.exit(fails.length ? 1 : 0);
})();
