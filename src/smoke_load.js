// What the bank actually costs a visitor, measured rather than assumed.
//
// Run with:
//   CHROMIUM_PATH=/opt/pw-browsers/chromium-*/chrome-linux/chrome node src/smoke_load.js
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

const BUDGET_MS = 4000;   // time to first question, cold, on a fast connection
const fails = [];
const check = (n, c, d) => {
  console.log((c ? '  ok: ' : '  FAIL: ') + n + (d ? '  -> ' + d : ''));
  if (!c) fails.push(n);
};

(async () => {
  await new Promise(r => srv.listen(0, '127.0.0.1', r));
  const P = srv.address().port;
  const b = await chromium.launch({ executablePath: process.env.CHROMIUM_PATH });

  for (const [app, label] of [['app', 'GMAT'], ['act/app', 'ACT'], ['sat/app', 'SAT'],
                              ['gre/app', 'GRE'], ['lsat/app', 'LSAT']]) {
    const ctx = await b.newContext({ viewport: { width: 390, height: 844 } });
    const pg = await ctx.newPage();
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
    await pg.goto('http://127.0.0.1:' + P + '/' + app + '/', { waitUntil: 'load' });
    // Start a round and wait for a real question to be on screen. Anything earlier than
    // that is measuring paint, not usefulness.
    await pg.evaluate(() => { try { show('study'); } catch (e) {} });
    let ok = true;
    try {
      await pg.waitForFunction(() => {
        const v = document.getElementById('v-study');
        return v && !v.classList.contains('hidden') && v.innerText.trim().length > 40;
      }, { timeout: BUDGET_MS * 3 });
    } catch (e) { ok = false; }
    const ms = Date.now() - t0;

    const kb = n => (n / 1024).toFixed(0) + ' KB';
    check('[' + label + '] no page errors', errs.length === 0, errs[0] || '');
    check('[' + label + '] a question is reachable', ok);
    check('[' + label + '] ready within ' + BUDGET_MS + 'ms', ms <= BUDGET_MS, ms + 'ms');
    console.log('        over the wire: shell ' + kb(bytes.shell) + ', bank ' + kb(bytes.bank)
      + ', other ' + kb(bytes.other) + '  (total ' + kb(bytes.shell + bytes.bank + bytes.other) + ')');
    await ctx.close();
  }

  await b.close(); srv.close();
  console.log(fails.length ? '\nFAILURES: ' + fails.join(', ') : '\nall load budget checks passed');
  process.exit(fails.length ? 1 : 0);
})();
