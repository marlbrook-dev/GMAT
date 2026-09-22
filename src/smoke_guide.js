/* Renders the study guide pages and checks what only rendering reveals.
 *
 * Two failures this catches that reading the template cannot. The first is sideways
 * scroll on a phone: every grid and flex child on these pages holds formula cards and
 * long mono expressions, and a child without min-width:0 keeps its min-content width
 * and pushes the page over, which is exactly how pricing, the rankings controls and the
 * blog submit form broke. The second is a section that rendered empty: the formula
 * cards, worked examples and difficulty rungs are all built by joining strings, and a
 * join over an empty list is a valid page with nothing in it.
 *
 * Served over http rather than file:// so the pages load the same way they do live.
 */
const { chromium } = require('playwright');
const { chromiumPath } = require('./chromium_path.js');
const http = require('http');
const fs = require('fs');
const path = require('path');
const ROOT = path.resolve(__dirname, '..');

const TYPES = { '.html': 'text/html', '.js': 'text/javascript', '.css': 'text/css',
                '.json': 'application/json', '.svg': 'image/svg+xml', '.png': 'image/png',
                '.webmanifest': 'application/manifest+json' };
const server = http.createServer((req, res) => {
  let rel = decodeURIComponent(req.url.split('?')[0]);
  if (rel.endsWith('/')) rel += 'index.html';
  const f = path.join(ROOT, rel);
  if (!f.startsWith(ROOT) || !fs.existsSync(f) || fs.statSync(f).isDirectory()) {
    res.writeHead(404); return res.end('nope');
  }
  res.writeHead(200, { 'Content-Type': TYPES[path.extname(f)] || 'application/octet-stream' });
  res.end(fs.readFileSync(f));
});

// Which pages, and what each one has to have on it. Derived from the built tree rather
// than listed here, so a topic added later is covered without editing this file.
function targets() {
  const out = [['/guide/', 'hub']];
  const gdir = path.join(ROOT, 'guide');
  for (const exam of fs.readdirSync(gdir)) {
    const ed = path.join(gdir, exam);
    if (!fs.statSync(ed).isDirectory()) continue;
    for (const sec of fs.readdirSync(ed)) {
      const sd = path.join(ed, sec);
      if (!fs.statSync(sd).isDirectory()) continue;
      out.push(['/guide/' + exam + '/' + sec + '/', 'section']);
      for (const slug of fs.readdirSync(sd)) {
        if (fs.statSync(path.join(sd, slug)).isDirectory()) {
          out.push(['/guide/' + exam + '/' + sec + '/' + slug + '/', 'topic']);
        }
      }
    }
  }
  return out;
}

(async () => {
  await new Promise(r => server.listen(0, r));
  const base = 'http://127.0.0.1:' + server.address().port;
  const b = await chromium.launch({ executablePath: chromiumPath() });
  let fail = 0, pages = 0;
  const check = (name, ok, extra) => {
    if (!ok) { console.log('  FAIL: ' + name + (extra ? ' -> ' + extra : '')); fail++; }
  };
  const list = targets();

  for (const width of [390, 1280]) {
    const ctx = await b.newContext({ viewport: { width, height: 900 } });
    const p = await ctx.newPage();
    const errs = [];
    p.on('pageerror', e => errs.push(String(e)));
    for (const [url, kind] of list) {
      errs.length = 0;
      await p.goto(base + url, { waitUntil: 'domcontentloaded' });
      const m = await p.evaluate(() => {
        const de = document.documentElement;
        const over = [...document.querySelectorAll('body *')]
          .filter(e => e.getBoundingClientRect().right > de.clientWidth + 1)
          .map(e => e.tagName.toLowerCase() + '.' + String(e.className || '').slice(0, 30));
        return { scrollW: de.scrollWidth, clientW: de.clientWidth, over: over.slice(0, 4),
                 h1: ((document.querySelector('h1') || {}).textContent || '').trim(),
                 fx: document.querySelectorAll('.fx').length,
                 worked: document.querySelectorAll('.w').length,
                 rungs: document.querySelectorAll('.rung').length,
                 traps: document.querySelectorAll('ul.traps li').length,
                 cards: document.querySelectorAll('.tcard, .scard').length,
                 footer: !!document.querySelector('footer') };
      });
      const at = width + 'px ' + url;
      check(at + ' scrolls sideways', m.scrollW <= m.clientW + 1,
            m.scrollW + ' > ' + m.clientW + ' from ' + JSON.stringify(m.over));
      check(at + ' has a heading', m.h1.length > 0);
      check(at + ' has the site footer', m.footer);
      check(at + ' threw no script error', errs.length === 0, errs[0]);
      if (kind === 'topic') {
        check(at + ' has formula cards', m.fx > 0, 'fx=' + m.fx);
        check(at + ' has worked examples', m.worked > 0, 'worked=' + m.worked);
        check(at + ' has all five rungs', m.rungs === 5, 'rungs=' + m.rungs);
        check(at + ' has traps', m.traps >= 2, 'traps=' + m.traps);
      } else {
        check(at + ' has cards', m.cards > 0, 'cards=' + m.cards);
      }
      pages++;
    }
    await ctx.close();
  }
  await b.close();
  server.close();
  console.log(fail ? '\n' + fail + ' guide check(s) failed'
                   : '\nall guide pages render: ' + (pages / 2) + ' pages at 390px and 1280px');
  process.exit(fail ? 1 : 0);
})();
