/* Drives the ACT, GRE, SAT, PSAT/NMSQT and LSAT calculators the way a student would and
 * checks every number they print.
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
const SAT_PATH = '/exams/sat/score-calculator/';
const SAT = JSON.parse(fs.readFileSync(path.join(ROOT, 'data', 'sat_percentiles.json'), 'utf8'));
const PSAT_PATH = '/exams/sat/psat-calculator/';
const PSAT = JSON.parse(fs.readFileSync(path.join(ROOT, 'data', 'psat_percentiles.json'), 'utf8'));
const LSAT_PATH = '/exams/lsat/percentile-calculator/';
const LSAT = JSON.parse(fs.readFileSync(path.join(ROOT, 'data', 'lsat_percentiles.json'), 'utf8'));

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
  for (const u of [URL_PATH, GRE_PATH, SAT_PATH, PSAT_PATH, LSAT_PATH]) {
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
  // The SAT page: the total is the sum of the two sections, and every percentile is read
  // off the data file the page was built from, 99+ and 1- included.
  const satLine = (label, v, t) => label + ' ' + v + ': nationally representative percentile '
    + t.national[String(v)] + ', user group percentile ' + t.user[String(v)] + '.';
  for (const width of [390, 1280]) {
    const ctx = await b.newContext({ viewport: { width, height: 900 } });
    const p = await ctx.newPage();
    const errs = [];
    p.on('pageerror', e => errs.push(String(e)));
    await p.goto(base + SAT_PATH, { waitUntil: 'domcontentloaded' });
    if (await p.isVisible('#sfn-consent').catch(() => false)) await p.click('#sfn-consent .no');
    const at = width + 'px SAT';
    const read = () => p.evaluate(() => ({ text: document.getElementById('satOut').textContent,
                                           cls: document.getElementById('satOut').className }));
    const wrong = [];
    for (const [rw, m] of [[600, 600], [800, 800], [200, 200], [510, 690], [730, 540]]) {
      await p.fill('#sT', ''); await p.fill('#sRW', String(rw)); await p.fill('#sM', String(m));
      const { text } = await read();
      const t = rw + m;
      if (!text.includes(rw + ' + ' + m + ' = ' + t)) wrong.push('sum ' + rw + '+' + m);
      for (const line of [satLine('Total', t, SAT.total), satLine('Reading and Writing', rw, SAT.rw),
                          satLine('Math', m, SAT.math)]) {
        if (!text.includes(line)) wrong.push(line);
      }
    }
    check(at + ' totals and percentiles match College Board\'s tables, 99+ and 1- included', !wrong.length, wrong.join('; '));
    await p.fill('#sRW', ''); await p.fill('#sM', ''); await p.fill('#sT', '1350');
    let r = await read();
    check(at + ' looks up a total typed on its own', r.text.includes(satLine('Total', 1350, SAT.total)) && !r.cls.includes('err'), r.text);
    await p.fill('#sRW', '600'); await p.fill('#sM', '600'); await p.fill('#sT', '1300');
    r = await read();
    check(at + ' sets aside a typed total that is not the sum', r.text.includes('1300, is not the sum') && r.text.includes(satLine('Total', 1200, SAT.total)), r.text);
    for (const [sel, bad] of [['#sRW', '805'], ['#sRW', '195'], ['#sM', '555'], ['#sT', '1605']]) {
      await p.fill('#sRW', '600'); await p.fill('#sM', '600'); await p.fill('#sT', '');
      await p.fill(sel, bad);
      r = await read();
      check(at + ' refuses ' + bad + ' in ' + sel, r.cls.includes('err'), r.text);
    }
    const tables = await p.evaluate(() => ({
      tot: [...document.querySelectorAll('#totTable tbody tr')].map(tr => [...tr.cells].map(td => td.textContent)),
      rw: [...document.querySelectorAll('#rwTable tbody tr')].map(tr => [...tr.cells].map(td => td.textContent)),
      m: [...document.querySelectorAll('#mTable tbody tr')].map(tr => [...tr.cells].map(td => td.textContent)) }));
    const off = (rows, t) => rows.filter(c => c[1] !== t.national[c[0]] || c[2] !== t.user[c[0]]);
    const bad = off(tables.tot, SAT.total).concat(off(tables.rw, SAT.rw), off(tables.m, SAT.math));
    check(at + ' tables match College Board\'s percentiles', tables.tot.length === 121 && tables.rw.length === 61
          && tables.m.length === 61 && !bad.length, bad.map(c => c.join(' ')).join('; '));
    const meta = await p.evaluate(() => {
      const de = document.documentElement;
      let faq = 0;
      document.querySelectorAll('script[type="application/ld+json"]').forEach(s => {
        try { const j = JSON.parse(s.textContent); if (j['@type'] === 'FAQPage') faq = j.mainEntity.length; } catch (e) { faq = -1; } });
      return { scrollW: de.scrollWidth, clientW: de.clientWidth, faq,
               cites: [...document.querySelectorAll('.src a')].map(a => a.href) };
    });
    const cb = h => h.startsWith('https://research.collegeboard.org/') || h.startsWith('https://satsuite.collegeboard.org/');
    check(at + ' does not scroll sideways', meta.scrollW <= meta.clientW + 1, meta.scrollW + ' > ' + meta.clientW);
    check(at + ' has an FAQ block search engines can read', meta.faq >= 3, String(meta.faq));
    check(at + ' cites only collegeboard.org', meta.cites.length > 0 && meta.cites.every(cb),
          meta.cites.filter(h => !cb(h)).join(', '));
    check(at + ' threw no script error', errs.length === 0, errs[0]);
    await ctx.close();
  }
  // The PSAT/NMSQT page: the total, the Selection Index worked the way College Board states
  // it, each grade's percentiles and its benchmarks, all against the data file.
  const psatLine = (label, v, t, g) => label + ' ' + v + ': nationally representative percentile '
    + t[g].national[String(v)] + ', user group percentile ' + t[g].user[String(v)] + '.';
  const benchLine = (label, v, key, g) => label + ' ' + v + (v >= PSAT.benchmarks[key][g] ? ' meets' : ' is below')
    + " College Board's " + g + 'th grade benchmark of ' + PSAT.benchmarks[key][g] + '.';
  for (const width of [390, 1280]) {
    const ctx = await b.newContext({ viewport: { width, height: 900 } });
    const p = await ctx.newPage();
    const errs = [];
    p.on('pageerror', e => errs.push(String(e)));
    await p.goto(base + PSAT_PATH, { waitUntil: 'domcontentloaded' });
    if (await p.isVisible('#sfn-consent').catch(() => false)) await p.click('#sfn-consent .no');
    const at = width + 'px PSAT';
    const read = () => p.evaluate(() => ({ text: document.getElementById('psatOut').textContent,
                                           cls: document.getElementById('psatOut').className }));
    const wrong = [];
    for (const g of ['10', '11']) {
      await p.selectOption('#pG', g);
      for (const [rw, m] of [[640, 680], [760, 760], [160, 160], [450, 520], [460, 510]]) {
        await p.fill('#pRW', String(rw)); await p.fill('#pM', String(m));
        const { text } = await read();
        const want = [rw + ' + ' + m + ' = ' + (rw + m), '(2 \u00d7 ' + rw + ' + ' + m + ') \u00f7 10 = ' + (2 * rw + m) / 10,
                      psatLine('Total', rw + m, PSAT.total, g), psatLine('Reading and Writing', rw, PSAT.rw, g),
                      psatLine('Math', m, PSAT.math, g), benchLine('Reading and Writing', rw, 'rw', g), benchLine('Math', m, 'math', g)];
        want.filter(w => !text.includes(w)).forEach(w => wrong.push('grade ' + g + ': ' + w));
      }
    }
    check(at + ' totals, Selection Index, percentiles and benchmarks match College Board for both grades', !wrong.length, wrong.slice(0, 4).join('; '));
    await p.selectOption('#pG', ''); await p.fill('#pRW', '600'); await p.fill('#pM', '600');
    let r = await read();
    check(at + ' gives the total and index before a grade is chosen, and no percentile', r.text.includes('600 + 600 = 1200')
          && r.text.includes('= 180') && r.text.includes('Choose your grade') && !r.text.includes('representative percentile'), r.text);
    for (const [sel, bad] of [['#pRW', '770'], ['#pRW', '150'], ['#pM', '555']]) {
      await p.fill('#pRW', '600'); await p.fill('#pM', '600');
      await p.fill(sel, bad);
      r = await read();
      check(at + ' refuses ' + bad + ' in ' + sel, r.cls.includes('err'), r.text);
    }
    const tables = await p.evaluate(() => Object.fromEntries(['tot10', 'tot11', 'rw10', 'rw11', 'm10', 'm11'].map(id =>
      [id, [...document.querySelectorAll('#' + id + ' tbody tr')].map(tr => [...tr.cells].map(td => td.textContent))])));
    const want = { tot10: [PSAT.total, '10', 121], tot11: [PSAT.total, '11', 121], rw10: [PSAT.rw, '10', 61],
                   rw11: [PSAT.rw, '11', 61], m10: [PSAT.math, '10', 61], m11: [PSAT.math, '11', 61] };
    const tbad = Object.entries(want).flatMap(([id, [t, g, n]]) => tables[id].length !== n ? [id + ' has ' + tables[id].length + ' rows']
      : tables[id].filter(c => c[1] !== t[g].national[c[0]] || c[2] !== t[g].user[c[0]]).map(c => id + ' ' + c.join(' ')));
    check(at + " tables match College Board's percentiles for both grades", !tbad.length, tbad.slice(0, 4).join('; '));
    const meta = await p.evaluate(() => {
      const de = document.documentElement;
      let faq = 0;
      document.querySelectorAll('script[type="application/ld+json"]').forEach(s => {
        try { const j = JSON.parse(s.textContent); if (j['@type'] === 'FAQPage') faq = j.mainEntity.length; } catch (e) { faq = -1; } });
      return { scrollW: de.scrollWidth, clientW: de.clientWidth, faq,
               cites: [...document.querySelectorAll('.src a')].map(a => a.href) };
    });
    const cb = h => h.startsWith('https://research.collegeboard.org/') || h.startsWith('https://satsuite.collegeboard.org/');
    check(at + ' does not scroll sideways', meta.scrollW <= meta.clientW + 1, meta.scrollW + ' > ' + meta.clientW);
    check(at + ' has an FAQ block search engines can read', meta.faq >= 3, String(meta.faq));
    check(at + ' cites only collegeboard.org', meta.cites.length > 0 && meta.cites.every(cb),
          meta.cites.filter(h => !cb(h)).join(', '));
    check(at + ' threw no script error', errs.length === 0, errs[0]);
    await ctx.close();
  }
  // The LSAT page: LSAC's table looked up both ways, against the data file.
  const lowestAt = p => { for (let v = 120; v <= 180; v++) if (+LSAT.ranks[String(v)].hundredths >= p) return v; return null; };
  for (const width of [390, 1280]) {
    const ctx = await b.newContext({ viewport: { width, height: 900 } });
    const p = await ctx.newPage();
    const errs = [];
    p.on('pageerror', e => errs.push(String(e)));
    await p.goto(base + LSAT_PATH, { waitUntil: 'domcontentloaded' });
    if (await p.isVisible('#sfn-consent').catch(() => false)) await p.click('#sfn-consent .no');
    const at = width + 'px LSAT';
    const read = () => p.evaluate(() => ({ text: document.getElementById('lsatOut').textContent,
                                           cls: document.getElementById('lsatOut').className }));
    const wrong = [];
    await p.fill('#lP', '');
    for (const s of [120, 150, 160, 170, 180]) {
      await p.fill('#lS', String(s));
      const { text } = await read();
      const want = s + ': ' + LSAT.ranks[String(s)].hundredths + ' percent of test scores were lower';
      if (!text.includes(want)) wrong.push(want);
    }
    await p.fill('#lS', '');
    for (const t of ['50', '90', '99', '75.5', '0']) {
      await p.fill('#lP', t);
      const { text } = await read();
      const v = lowestAt(+t);
      const want = 'at least ' + t + ' percent of test scores below it is ' + v + ' (' + LSAT.ranks[String(v)].hundredths + ' percent)';
      if (!text.includes(want)) wrong.push(want);
    }
    await p.fill('#lP', '99.9');
    let r = await read();
    if (!r.text.includes('No score in LSAC')) wrong.push('99.9 beyond the table');
    check(at + " looks up scores and percentiles both ways in LSAC's table", !wrong.length, wrong.join('; '));
    for (const [sel, bad] of [['#lS', '119'], ['#lS', '181'], ['#lS', '150.5'], ['#lP', '100'], ['#lP', '-5']]) {
      await p.fill('#lS', ''); await p.fill('#lP', '');
      await p.fill(sel, bad).catch(() => {});
      r = await read();
      check(at + ' refuses ' + bad + ' in ' + sel, r.cls.includes('err'), r.text);
    }
    const rows = await p.evaluate(() => [...document.querySelectorAll('#lsatTable tbody tr')].map(tr => [...tr.cells].map(td => td.textContent)));
    const off = rows.filter(c => { const x = LSAT.ranks[c[0]]; return !x || c[1] !== x.hundredths || c[2] !== x.tenths || c[3] !== x.whole; });
    check(at + " table matches LSAC's percentiles", rows.length === 61 && !off.length, off.map(c => c.join(' ')).join('; '));
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
    check(at + ' cites only lsac.org', meta.cites.length > 0 && meta.cites.every(h => h.startsWith('https://www.lsac.org/')),
          meta.cites.filter(h => !h.startsWith('https://www.lsac.org/')).join(', '));
    check(at + ' threw no script error', errs.length === 0, errs[0]);
    await ctx.close();
  }
  await b.close();
  server.close();
  console.log(fail ? '\n' + fail + ' calculator check(s) failed' : '\nall ' + ok + ' calculator checks passed');
  process.exit(fail ? 1 : 0);
})();
