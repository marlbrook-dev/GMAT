/* Drives the ACT score calculator the way a student would and checks every number it prints.
 *
 * The page's arithmetic is ACT's published rule, so the check computes the same rule
 * independently (Math.round, which rounds halves up for positive numbers) and reads the
 * national ranks from the data file the page was built from, rather than trusting the
 * page to agree with itself. It also checks what only rendering shows: sideways scroll
 * at phone width, the superscore's add and remove limits, and that every citation on the
 * page points at act.org.
 */
const { chromium } = require('playwright');
const { chromiumPath } = require('./chromium_path.js');
const http = require('http');
const fs = require('fs');
const path = require('path');
const ROOT = path.resolve(__dirname, '..');
const URL_PATH = '/exams/act/score-calculator/';
const DATA = JSON.parse(fs.readFileSync(path.join(ROOT, 'data', 'act_national_ranks.json'), 'utf8'));
const RANK = DATA.ranks.composite.at_or_below;
const GRE_PATH = '/exams/gre/score-calculator/';
const GRE = JSON.parse(fs.readFileSync(path.join(ROOT, 'data', 'gre_percentiles.json'), 'utf8'));

const TYPES = { '.html': 'text/html', '.js': 'text/javascript', '.css': 'text/css',
                '.json': 'application/json', '.svg': 'image/svg+xml', '.png': 'image/png' };
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

const composite = (a, b, c) => Math.round((a + b + c) / 3);

(async () => {
  for (const u of [URL_PATH, GRE_PATH]) {
    if (!fs.existsSync(path.join(ROOT, u, 'index.html'))) {
      console.log('  FAIL: ' + u + ' was not built; run python3 src/build.py first');
      process.exit(1);
    }
  }
  await new Promise(r => server.listen(0, r));
  const base = 'http://127.0.0.1:' + server.address().port;
  const b = await chromium.launch({ executablePath: chromiumPath() });
  let fail = 0, ok = 0;
  const check = (name, pass, extra) => {
    if (pass) { ok++; console.log('  ok   ' + name); }
    else { fail++; console.log('  FAIL: ' + name + (extra ? ' -> ' + extra : '')); }
  };

  for (const width of [390, 1280]) {
    const ctx = await b.newContext({ viewport: { width, height: 900 } });
    const p = await ctx.newPage();
    const errs = [];
    p.on('pageerror', e => errs.push(String(e)));
    await p.goto(base + URL_PATH, { waitUntil: 'domcontentloaded' });
    if (await p.isVisible('#sfn-consent').catch(() => false)) await p.click('#sfn-consent .no');
    const at = width + 'px';

    // The Composite, over ordinary and edge cases, against the rule computed here.
    const cases = [[24, 25, 25], [24, 24, 25], [1, 1, 1], [36, 36, 36], [36, 36, 35],
                   [20, 21, 22], [12, 30, 19]];
    const wrong = [];
    for (const [e, m, r] of cases) {
      await p.fill('#cE', String(e)); await p.fill('#cM', String(m)); await p.fill('#cR', String(r));
      const got = await p.evaluate(() => {
        const v = document.getElementById('compVal');
        return { c: v ? +v.textContent : null, text: document.getElementById('compOut').textContent };
      });
      const want = composite(e, m, r);
      const rankLine = RANK[String(want)] + ' percent of ' + DATA.cohort;
      if (got.c !== want || !got.text.includes(rankLine)) {
        wrong.push([e, m, r].join('/') + ' gave ' + got.c + ', want ' + want);
      }
    }
    check(at + ' Composite and its national rank match ACT\'s rule and table', !wrong.length, wrong.join('; '));

    for (const bad of ['0', '37', '24.5']) {
      await p.fill('#cE', bad); await p.fill('#cM', '20'); await p.fill('#cR', '20');
      const err = await p.evaluate(() => ({ cls: document.getElementById('compOut').className,
                                            v: !!document.getElementById('compVal') }));
      check(at + ' refuses a section score of ' + bad, err.cls.includes('err') && !err.v);
    }

    // The superscore: best of each section across dates, averaged by the same rule.
    const fillRow = async (i, vals) => {
      const ins = await p.$$('#superGrid tbody tr:nth-child(' + i + ') input');
      for (let k = 0; k < 3; k++) await ins[k].fill(String(vals[k]));
    };
    await fillRow(1, [24, 22, 26]);
    await fillRow(2, [21, 27, 25]);
    const sup = await p.evaluate(() => ({ v: +(document.getElementById('superVal') || {}).textContent,
                                          text: document.getElementById('superOut').textContent,
                                          best: document.querySelectorAll('#superGrid td.best').length }));
    check(at + ' superscore takes the best of each section', sup.v === composite(24, 27, 26),
          sup.v + ' from ' + sup.text);
    check(at + ' superscore marks the three best scores', sup.best === 3, String(sup.best));
    check(at + ' superscore reports the best single test Composite',
          sup.text.includes('highest single test Composite is ' + Math.max(composite(24, 22, 26), composite(21, 27, 25))),
          sup.text);

    // Click only while enabled: Playwright waits out a disabled button rather than failing.
    for (let i = 0; i < 10 && !(await p.isDisabled('#addRow')); i++) await p.click('#addRow');
    const most = await p.evaluate(() => ({ n: document.querySelectorAll('#superGrid tbody tr').length,
                                           off: document.getElementById('addRow').disabled }));
    check(at + ' stops at six test dates', most.n === 6 && most.off, JSON.stringify(most));
    for (let i = 0; i < 10 && !(await p.isDisabled('#dropRow')); i++) await p.click('#dropRow');
    const least = await p.evaluate(() => ({ n: document.querySelectorAll('#superGrid tbody tr').length,
                                            off: document.getElementById('dropRow').disabled }));
    check(at + ' keeps at least two test dates', least.n === 2 && least.off, JSON.stringify(least));

    // The printed ranks table is the data file, row for row.
    const table = await p.evaluate(() => [...document.querySelectorAll('table.dt tbody tr:not(.foot)')]
      .map(tr => [...tr.cells].map(td => +td.textContent)));
    const cols = ['composite', 'english', 'math', 'reading', 'science'];
    const off = table.filter(row => cols.some((c, k) => DATA.ranks[c].at_or_below[String(row[0])] !== row[k + 1]));
    check(at + ' ranks table matches ACT\'s national ranks', table.length === 36 && !off.length,
          table.length + ' rows, ' + off.length + ' differ');

    const meta = await p.evaluate(() => {
      const de = document.documentElement;
      const ld = [...document.querySelectorAll('script[type="application/ld+json"]')].map(s => s.textContent);
      let faq = 0;
      ld.forEach(t => { try { const j = JSON.parse(t); if (j['@type'] === 'FAQPage') faq = j.mainEntity.length; } catch (e) { faq = -1; } });
      const cites = [...document.querySelectorAll('.src a')].map(a => a.href);
      return { scrollW: de.scrollWidth, clientW: de.clientWidth, faq, cites,
               h1: (document.querySelector('h1') || {}).textContent || '' };
    });
    check(at + ' does not scroll sideways', meta.scrollW <= meta.clientW + 1, meta.scrollW + ' > ' + meta.clientW);
    check(at + ' has an FAQ block search engines can read', meta.faq >= 3, String(meta.faq));
    check(at + ' cites only act.org', meta.cites.length > 0 && meta.cites.every(h => h.startsWith('https://www.act.org/')),
          meta.cites.filter(h => !h.startsWith('https://www.act.org/')).join(', '));
    check(at + ' threw no script error', errs.length === 0, errs[0]);
    await ctx.close();
  }

  // The GRE page: ETS's percentile ranks, read off the data file it was built from.
  const want = (label, v, table) => table[String(v)] == null
    ? label + ' ' + v + ': ETS reports no percentile'
    : label + ' ' + v + ': ' + table[String(v)] + ' percent of test takers scored lower';
  for (const width of [390, 1280]) {
    const ctx = await b.newContext({ viewport: { width, height: 900 } });
    const p = await ctx.newPage();
    const errs = [];
    p.on('pageerror', e => errs.push(String(e)));
    await p.goto(base + GRE_PATH, { waitUntil: 'domcontentloaded' });
    if (await p.isVisible('#sfn-consent').catch(() => false)) await p.click('#sfn-consent .no');
    const at = width + 'px GRE';
    const wrong = [];
    for (const [v, q, w] of [[160, 160, '4.0'], [170, 170, '6.0'], [130, 132, '0.5'], [151, 158, '3.5']]) {
      await p.fill('#gV', String(v)); await p.fill('#gQ', String(q)); await p.selectOption('#gW', w);
      const text = await p.evaluate(() => document.getElementById('greOut').textContent);
      for (const line of [want('Verbal', v, GRE.verbal), want('Quant', q, GRE.quant), want('Writing', w, GRE.writing)]) {
        if (!text.includes(line)) wrong.push(line);
      }
      if (!text.includes('Verbal plus Quant is ' + (v + q))) wrong.push('sum ' + (v + q));
    }
    check(at + ' percentiles match ETS\'s table, blanks included', !wrong.length, wrong.join('; '));
    for (const bad of ['129', '171', '150.5']) {
      await p.fill('#gV', bad); await p.fill('#gQ', '150');
      const cls = await p.evaluate(() => document.getElementById('greOut').className);
      check(at + ' refuses a Verbal score of ' + bad, cls.includes('err'));
    }
    const tables = await p.evaluate(() => ({
      vq: [...document.querySelectorAll('#vqTable tbody tr')].map(tr => [...tr.cells].map(td => td.textContent)),
      aw: [...document.querySelectorAll('#awTable tbody tr')].map(tr => [...tr.cells].map(td => td.textContent)) }));
    const cellOk = (txt, v) => v == null ? txt === 'not reported' : +txt === v;
    const vqBad = tables.vq.filter(r => !cellOk(r[1], GRE.verbal[r[0]]) || !cellOk(r[2], GRE.quant[r[0]]));
    const awBad = tables.aw.filter(r => !cellOk(r[1], GRE.writing[r[0]]));
    check(at + ' tables match ETS\'s percentile ranks', tables.vq.length === 41 && tables.aw.length === 13
          && !vqBad.length && !awBad.length, vqBad.concat(awBad).map(r => r.join(' ')).join('; '));
    const meta = await p.evaluate(() => {
      const de = document.documentElement;
      let faq = 0;
      document.querySelectorAll('script[type="application/ld+json"]').forEach(s => {
        try { const j = JSON.parse(s.textContent); if (j['@type'] === 'FAQPage') faq = j.mainEntity.length; } catch (e) { faq = -1; } });
      return { scrollW: de.scrollWidth, clientW: de.clientWidth, faq,
               cites: [...document.querySelectorAll('.src a')].map(a => a.href) };
    });
    check(at + ' does not scroll sideways', meta.scrollW <= meta.clientW + 1, meta.scrollW + ' > ' + meta.clientW);
    check(at + ' has an FAQ block search engines can read', meta.faq >= 3, String(meta.faq));
    check(at + ' cites only ets.org', meta.cites.length > 0 && meta.cites.every(h => h.startsWith('https://www.ets.org/')),
          meta.cites.filter(h => !h.startsWith('https://www.ets.org/')).join(', '));
    check(at + ' threw no script error', errs.length === 0, errs[0]);
    await ctx.close();
  }
  await b.close();
  server.close();
  console.log(fail ? '\n' + fail + ' calculator check(s) failed' : '\nall ' + ok + ' calculator checks passed');
  process.exit(fail ? 1 : 0);
})();
