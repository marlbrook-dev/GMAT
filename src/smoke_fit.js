// The fit view, validated against figures worked out by hand first.
//
// A fit view is the highest-stakes surface on this site that is not money: a student
// reads it and decides where to apply. So the test asserts the four things that would
// each be a quiet lie, rather than that the card rendered.
//
//   A published average is shown as an average, with its source and year.
//   A figure the school does not publish renders as "not published", never as a zero.
//   Nothing on the page is a probability, a score or a composite.
//   Focus and Classic are never converted into one another.
const { chromium } = require('playwright');
const http = require('http');
const fs = require('fs');
const path0 = require('path');
const { chromiumPath } = require('./chromium_path');
const ROOT = path0.resolve(__dirname, '..');

const TYPES = { '.html': 'text/html', '.js': 'text/javascript', '.css': 'text/css',
                '.json': 'application/json', '.svg': 'image/svg+xml', '.png': 'image/png',
                '.webmanifest': 'application/manifest+json', '.txt': 'text/plain' };
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
const url = p => 'http://127.0.0.1:' + PORT + '/' + String(p).replace(/^\//, '');
const noise = t => /ERR_CERT_AUTHORITY_INVALID|fonts\.(googleapis|gstatic)\.com|Failed to fetch|net::ERR|supabase/i.test(t);

let fails = 0;
const ok = (c, label) => { if (!c) { fails++; console.log('  FAIL ' + label); } else console.log('  ok   ' + label); };

// Two schools chosen so every branch is exercised. The first publishes everything; the
// second publishes almost nothing, which is the case that must not render as zeros.
// Worked out by hand before the page existed:
//   GPA 3.40 against 3.76 average         -> below  (difference 0.36, margin 0.05)
//   Work 5.0 yrs against 4.80 average     -> at about (difference 0.20, margin 0.50)
//   Budget 120,000 against 84,996 a year  -> 169,992 over two years.
//     120000/169992 = 0.7059 of the programme, and 0.7059 * 24 = 16.9, so 17 months.
const SAVED = {
  order: ['alpha-gsb', 'beta-school'],
  meta: {
    'alpha-gsb': {
      tag: 'reach', note: '', name: 'Alpha Graduate School of Business',
      gmat: { v: 689, ed: 'Focus', stat: 'average, observed range 615-785' },
      fit: {
        gpa: { v: 3.76, stat: 'average GPA', src: 'Alpha GSB class profile', year: 2025, url: 'https://example.invalid/alpha' },
        work_exp_years: { v: 4.8, stat: 'average', src: 'Alpha GSB class profile', year: 2025, url: 'https://example.invalid/alpha' },
        tuition_usd: { v: 84996, stat: 'per year', src: 'Alpha GSB tuition page', year: 2025, url: 'https://example.invalid/alpha-t' },
        accept_rate_pct: { v: 6.8, stat: '', src: 'Alpha GSB', year: 2026, url: 'https://example.invalid/alpha-a' },
      },
    },
    'beta-school': {
      tag: 'safety', note: '', name: 'Beta School of Management',
      gmat: null, fit: {},
    },
  },
};

(async () => {
  await new Promise(r => server.listen(0, '127.0.0.1', r));
  PORT = server.address().port;
  const browser = await chromium.launch({ executablePath: chromiumPath() });

  for (const [w, h] of [[1280, 900], [390, 844]]) {
    console.log('\n' + w + 'px');
    const ctx = await browser.newContext({ viewport: { width: w, height: h } });
    const page = await ctx.newPage();
    const errs = [];
    page.on('console', m => { if (m.type() === 'error' && !noise(m.text())) errs.push(m.text()); });
    page.on('pageerror', e => errs.push(String(e)));

    await page.addInitScript(saved => {
      localStorage.setItem('sfn_school_list_v1', JSON.stringify(saved));
    }, SAVED);
    await page.goto(url('/app/'), { waitUntil: 'domcontentloaded' });
    await page.waitForFunction(() => typeof window.fitCard === 'function', { timeout: 15000 });

    await page.evaluate(() => {
      finishOnboarding(true);
      const ab = state.settings.about || (state.settings.about = {});
      ab.gpa = 3.40; ab.work_exp_years = 5; ab.tuition_budget_usd = 120000;
      persist();
      show('data');
    });
    await page.waitForFunction(() => /Fit Against Your Target Schools/.test(
      document.getElementById('v-data').innerText), { timeout: 15000 });

    const text = await page.evaluate(() => document.getElementById('v-data').innerText);

    ok(/Alpha Graduate School of Business/.test(text), 'the shortlist drives the card');
    ok(/3\.40/.test(text) && /3\.76/.test(text), 'shows your GPA and the published one');
    ok(/Below the average/.test(text), 'GPA 3.40 against 3.76 reads as below');
    ok(/At about the average/.test(text), 'work 5.0 against 4.8 reads as at about, inside the margin');
    ok(/\$84,996/.test(text), 'published tuition is shown as published');
    ok(/\$169,992/.test(text), 'two years is computed, not typed');
    ok(/17 months of tuition/.test(text), 'a budget short of two years says how far it goes');
    ok(/Alpha GSB class profile/.test(text) && /2025/.test(text), 'the source and year travel with the figure');

    // The school that publishes nothing is the case that must not invent anything.
    //
    // Slice from the fit card, not from the first mention of the school: the Target
    // Schools card above lists the same names, and anchoring on the name alone reads the
    // wrong section entirely, which is how the first version of this assertion failed
    // against a page that was behaving correctly.
    const card = text.slice(text.indexOf('Fit Against Your Target Schools'));
    ok(/Beta School of Management/.test(card), 'a school with no published figures still appears');
    const beta = card.slice(card.indexOf('Beta School of Management'));
    // Anchored on a boundary that is not a decimal point: \b0 yrs\b matches inside
    // "5.0 yrs", so the first version of this failed on a page rendering correctly.
    ok(!/\$0(\D|$)|(^|\s)0\.00(\s|$)|(^|\s)0 yrs/m.test(beta.slice(0, 400)),
      'a school that publishes nothing shows no zeros');
    ok(/not published/.test(beta.slice(0, 600)),
      'and says not published against the measures the reader did enter');

    // The honesty rules, asserted as text because they are the product.
    ok(/An average is not a cutoff/.test(text), 'says an average is not a cutoff');
    ok(/no probability here and there will not be one/i.test(text), 'declines to compute a probability');
    ok(!/% chance|likelihood|odds of admission|probability of admission/i.test(text),
      'prints no admission probability anywhere');
    ok(/never converted here/.test(text), 'says Focus and Classic are not converted');
    ok(/not a predicted score/i.test(text), 'the range is not called a predicted score');

    const overflow = await page.evaluate(() => {
      const n = document.getElementById('v-data');
      return Math.max(document.documentElement.scrollWidth - document.documentElement.clientWidth,
                      n.scrollWidth - n.clientWidth);
    });
    ok(overflow <= 1, 'no sideways scroll (' + overflow + 'px)');
    ok(errs.length === 0, 'no console errors' + (errs.length ? ': ' + errs[0] : ''));

    if (w === 1280) await page.locator('#v-data').screenshot({ path: '/tmp/fit-view.png' });
    await ctx.close();
  }

  // With nothing filled in, the card must invite rather than compare, and must still not
  // show a zero where a number would go.
  {
    console.log('\nnothing filled in');
    const ctx = await browser.newContext({ viewport: { width: 1280, height: 900 } });
    const page = await ctx.newPage();
    await page.addInitScript(saved => {
      localStorage.setItem('sfn_school_list_v1', JSON.stringify(saved));
    }, SAVED);
    await page.goto(url('/app/'), { waitUntil: 'domcontentloaded' });
    await page.waitForFunction(() => typeof window.fitCard === 'function', { timeout: 15000 });
    await page.evaluate(() => { finishOnboarding(true); show('data'); });
    const t = await page.evaluate(() => document.getElementById('v-data').innerText);
    ok(/not set/.test(t), 'an unanswered field says not set rather than showing a zero');
    ok(/in About You, further down this page/.test(t),
      'and points at where the inputs actually are, which is below it and not above');
    ok(!/Below the average|Above the average/.test(t), 'and bands nothing it cannot band');
    // With no inputs and no published figures there is genuinely nothing to compare, and
    // the card says that rather than printing a table of dashes.
    const card0 = t.slice(t.indexOf('Fit Against Your Target Schools'));
    ok(/publishes none of the figures/.test(card0.slice(card0.indexOf('Beta School of Management'))),
      'a school with nothing published and nothing entered says so in words');
    await ctx.close();
  }

  await browser.close();
  server.close();
  console.log('\n' + (fails ? fails + ' FAILED' : 'all fit checks passed'));
  process.exit(fails ? 1 : 0);
})().catch(e => { console.error(e); process.exit(1); });
