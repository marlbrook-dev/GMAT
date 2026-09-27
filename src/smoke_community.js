// The community page at phone width (INC-0164). Run with:
//   NODE_PATH=/opt/node22/lib/node_modules node src/smoke_community.js
//
// Signed out, the page says which pseudonym a post from this device will carry. The
// pseudonym is drawn at random, one of 20 adjectives, one of 20 birds and a number from 2
// to 98, and the line naming it could not wrap, so a visitor who drew a long name got a
// page that slid sideways on a phone and one who drew a short name did not. A check that
// loads the page with whatever name comes up passes or fails by luck, so this pins the
// longest name the page can draw, and the shortest, and checks both.
//
// Supabase is answered locally the way it answers a visitor with nothing to show: an
// empty list. Where the network fails outright the page replaces the line with a short
// notice, which is why no run without Supabase ever drew it.
const { chromium } = require('playwright');
const { chromiumPath } = require('./chromium_path.js');
const http = require('http');
const fs = require('fs');
const path0 = require('path');
const ROOT = path0.resolve(__dirname, '..');

const TYPES = { '.html': 'text/html', '.js': 'text/javascript', '.css': 'text/css',
                '.json': 'application/json', '.svg': 'image/svg+xml', '.png': 'image/png',
                '.woff2': 'font/woff2' };
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

// The longest and shortest names anonName() in src/community.html can produce. Read from
// the page's own lists at run time, so a list that grows cannot leave this behind.
function extremes(src) {
  const list = name => JSON.parse(src.match(new RegExp('var ' + name + ' = (\\[[^\\]]*\\])'))[1]);
  const adj = list('adj'), bird = list('bird');
  const by = (a, f) => a.slice().sort((x, y) => f(x.length, y.length))[0];
  return [by(adj, (a, b) => b - a) + ' ' + by(bird, (a, b) => b - a) + ' 98',
          by(adj, (a, b) => a - b) + ' ' + by(bird, (a, b) => a - b) + ' 2'];
}

let fail = 0;
function check(name, ok, detail) {
  console.log((ok ? '  ok   ' : '  FAIL ') + name + (ok || !detail ? '' : ': ' + detail));
  if (!ok) fail++;
}

(async () => {
  const src = fs.readFileSync(path0.join(ROOT, 'src', 'community.html'), 'utf8');
  const page = path0.join(ROOT, 'community', 'index.html');
  if (!fs.existsSync(page)) { console.log('community/index.html is not built; run python3 src/build.py'); process.exit(1); }
  await new Promise(r => server.listen(0, r));
  const base = 'http://127.0.0.1:' + server.address().port;
  const b = await chromium.launch({ executablePath: chromiumPath() });
  for (const name of extremes(src)) {
    for (const width of [390, 1280]) {
      const ctx = await b.newContext({ viewport: { width, height: 844 } });
      await ctx.addInitScript(n => {
        try {
          localStorage.setItem('sfn_consent_v1', JSON.stringify({ analytics: false, ts: '', v: 1 }));
          localStorage.setItem('sfn_anon_name', n);
        } catch (e) {}
      }, name);
      await ctx.route('**/rest/v1/**', r => r.fulfill({ status: 200, contentType: 'application/json', body: '[]' }));
      await ctx.route('**/auth/v1/**', r => r.fulfill({ status: 200, contentType: 'application/json', body: '{}' }));
      const p = await ctx.newPage();
      const errs = [];
      p.on('pageerror', e => errs.push(e.message));
      await p.goto(base + '/community/', { waitUntil: 'networkidle' });
      await p.evaluate(() => document.fonts.ready);
      const r = await p.evaluate(() => {
        const who = document.getElementById('who'), nm = who && who.querySelector('b');
        const lines = nm ? nm.getClientRects().length : 0;
        return { text: who ? who.textContent : '', name: nm ? nm.textContent : '', lines,
                 sideways: document.documentElement.scrollWidth - window.innerWidth };
      });
      const tag = '[' + name + ', ' + width + 'px] ';
      check(tag + 'the page names the pseudonym', r.name === name, JSON.stringify(r.text));
      check(tag + 'no sideways scroll', r.sideways <= 0, r.sideways + 'px');
      check(tag + 'the name is not broken across lines', r.lines === 1, r.lines + ' lines');
      check(tag + 'no page errors', errs.length === 0, errs.join(' | '));
      await ctx.close();
    }
  }
  await b.close();
  server.close();
  console.log(fail ? '\nFAILED (' + fail + ')' : '\nall community checks passed');
  process.exit(fail ? 1 : 0);
})().catch(e => { console.error(e); process.exit(1); });
