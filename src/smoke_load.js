// What the bank actually costs a visitor, measured rather than assumed.
//
// Run with:
//   node src/smoke_load.js   (the browser is resolved by src/chromium_path.js)
//
// The raw bank files are large and getting larger, and the instinct is to treat that as
// the load problem. It is not, and this file exists so that stays a measurement instead
// of a belief.
//
// Generated items are variations on a few hundred templates, so they share enormous
// amounts of structure and gzip collapses them about twelve to one. The bank grew 37
// percent raw when the per category target went from 500 to 704; over the wire it moved
// by under one percent. The shell, which does not compress nearly as well, is the larger
// share of a cold start.
//
// The number that would actually justify splitting the bank out is time to first
// question, so that is what this measures: serve everything gzipped, the way Cloudflare
// does, and wait until an item is on screen.
const { chromium } = require('playwright');
const { chromiumPath } = require('./chromium_path.js');
const http = require('http'), fs = require('fs'), p0 = require('path'), zlib = require('zlib');
const ROOT = p0.join(__dirname, '..');
const T = {'.html':'text/html','.js':'text/javascript','.css':'text/css','.png':'image/png',
           '.svg':'image/svg+xml','.json':'application/json','.webmanifest':'application/manifest+json'};

// Gzip everything compressible, because serving these uncompressed would measure a
// configuration nobody is running.
const srv = http.createServer((q, r) => {
  let rel = decodeURIComponent(q.url.split('?')[0]); if (rel.endsWith('/')) rel += 'index.html';
  const f = p0.join(ROOT, rel);
  if (!f.startsWith(ROOT) || !fs.existsSync(f) || fs.statSync(f).isDirectory()) { r.writeHead(404); r.end('nf'); return; }
  const type = T[p0.extname(f)] || 'application/octet-stream';
  const body = fs.readFileSync(f);
  if (/html|javascript|css|json/.test(type)) {
    const gz = zlib.gzipSync(body, { level: 6 });
    r.writeHead(200, { 'Content-Type': type, 'Content-Encoding': 'gzip', 'Content-Length': gz.length });
    r.end(gz);
  } else {
    r.writeHead(200, { 'Content-Type': type, 'Content-Length': body.length });
    r.end(body);
  }
});

const BUDGET_MS = 4000;      // time to first question, cold, unthrottled
// And the number that actually matters. Unthrottled on localhost measures parse and
// execute and almost no transfer, which flatters a megabyte badly. Regular 3G is what a
// lot of this audience is on: high school students on phones, and applicants abroad. A
// bank that is fine at 500ms on a desktop can be twenty seconds there, and the only way
// to know which is to make the browser actually wait for the bytes.
// 15s, not the 20s this started at. The two stage load put GMAT at 11s and everything
// else under 8, so a 20s budget would no longer catch the regression it was written for.
// A budget set above what the code actually does stops being a budget.
const SLOW_BUDGET_MS = 15000;
const SLOW_3G = { offline: false, latency: 400,
                  downloadThroughput: 400 * 1024 / 8, uploadThroughput: 400 * 1024 / 8 };
const fails = [];
const check = (n, c, d) => {
  console.log((c ? '  ok: ' : '  FAIL: ') + n + (d ? '  -> ' + d : ''));
  if (!c) fails.push(n);
};

(async () => {
  await new Promise(r => srv.listen(0, '127.0.0.1', r));
  const P = srv.address().port;
  const b = await chromium.launch({ executablePath: chromiumPath() });

  for (const [app, label] of [['app', 'GMAT'], ['act/app', 'ACT'], ['sat/app', 'SAT'],
                              ['gre/app', 'GRE'], ['lsat/app', 'LSAT']]) {
   for (const slow of [false, true]) {
    const tag = label + (slow ? ' on 3G' : '');
    const ctx = await b.newContext({ viewport: { width: 390, height: 844 } });
    const pg = await ctx.newPage();
    if (slow) {
      const cdp = await ctx.newCDPSession(pg);
      await cdp.send('Network.enable');
      await cdp.send('Network.emulateNetworkConditions', SLOW_3G);
    }
    const bytes = { shell: 0, bank: 0, other: 0 };
    pg.on('response', async res => {
      const u = res.url();
      let n = 0;
      try { n = Number(res.headers()['content-length'] || 0); } catch (e) {}
      if (/bank\.js/.test(u)) bytes.bank += n;
      else if (/index\.html|\/$/.test(u)) bytes.shell += n;
      else bytes.other += n;
    });
    const errs = [];
    pg.on('pageerror', e => errs.push(e.message));

    const t0 = Date.now();
    // domcontentloaded, not load. The 'load' event waits for every resource including
    // the async bank remainder, so waiting on it would time exactly the download the
    // split exists to stop blocking on, and would report no improvement from a change
    // that made the page usable nine times sooner. An async script does not hold up
    // DOMContentLoaded, which is why that is the right edge to measure from.
    await pg.goto('http://127.0.0.1:' + P + '/' + app + '/', { waitUntil: 'domcontentloaded' });
    // Start a round and wait for a real question to be on screen. Anything earlier than
    // that is measuring paint, not usefulness.
    await pg.evaluate(() => { try { show('study'); } catch (e) {} });
    const budget = slow ? SLOW_BUDGET_MS : BUDGET_MS;
    let ok = true;
    try {
      await pg.waitForFunction(() => {
        const v = document.getElementById('v-study');
        return v && !v.classList.contains('hidden') && v.innerText.trim().length > 40;
      }, { timeout: budget * 2 });
    } catch (e) { ok = false; }
    const ms = Date.now() - t0;

    const kb = n => (n / 1024).toFixed(0) + ' KB';
    check('[' + tag + '] no page errors', errs.length === 0, errs[0] || '');
    check('[' + tag + '] a question is reachable', ok);
    check('[' + tag + '] ready within ' + budget + 'ms', ms <= budget, ms + 'ms');
    if (!slow) {
      console.log('        over the wire: shell ' + kb(bytes.shell) + ', bank ' + kb(bytes.bank)
        + ', other ' + kb(bytes.other) + '  (total ' + kb(bytes.shell + bytes.bank + bytes.other) + ')');
    }
    await ctx.close();
   }
  }

  await b.close(); srv.close();
  console.log(fails.length ? '\nFAILURES: ' + fails.join(', ') : '\nall load budget checks passed');
  process.exit(fails.length ? 1 : 0);
})();
