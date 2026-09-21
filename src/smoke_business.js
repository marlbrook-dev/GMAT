// The Business tab, validated by rendering it. Run with:
//   CHROMIUM_PATH=/opt/pw-browsers/chromium-*/chrome-linux/chrome node src/smoke_business.js
//
// A dashboard is the one kind of page where "it rendered" is not the test. A tile that
// says $0.00 when the answer is $49.99 renders perfectly. So this feeds admin_business a
// response whose every figure is known in advance and asserts the page prints those
// figures, in both themes and at phone width.
//
// The arithmetic under test is the part that is easy to get quietly wrong:
//   MRR from an annual price is the price divided by twelve, not the price.
//   ARR is MRR times twelve, so an annual subscriber's ARR is their annual price back.
//   Trial money is never in MRR.
//   Net new MRR is new plus expansion less contraction less churn.
//   Trial conversion counts DECIDED cohorts only; a trial still running is not a failure.
//   Refunds are shown beside charges, never subtracted from them.
const { chromium } = require('playwright');
const http = require('http');
const fs = require('fs');
const path0 = require('path');
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
const ok = (cond, label) => { if (!cond) { fails++; console.log('  FAIL ' + label); } else console.log('  ok   ' + label); };

// One monthly Plus at $4.99 and one annual Pro at $99.99. Every derived figure below was
// worked out by hand from these two rows, which is the point: the test knows the answer
// before the page does.
//   MRR   = 499 + round(9999/12) = 499 + 833 = 1332  -> $13.32
//   ARR   = 1332 * 12 = 15984 cents                  -> $159.84
//   net   = new 1332 + expansion 200 - contraction 50 - churn 499 = 983 -> $9.83
//   conv  = 3 converted of (3 + 1 lapsed) decided = 75.0%, with 2 pending excluded
const FIXTURE = {
  generated_at: '2026-09-21T00:00:00Z', days: 90, since: '2026-06-23T00:00:00Z',
  log: { events: 42, first_at: '2026-08-15T00:00:00Z', last_at: '2026-09-21T00:00:00Z', covers_window: false },
  snapshot: { mrr_cents: 1332, trial_mrr_cents: 998, paying: 2, trialing: 2,
              past_due: 1, cancelling: 1, accounts_total: 128, ever_subscribed: 16 },
  movement: [
    { d: '2026-09-18', new_cents: 1332, expansion_cents: 200, contraction_cents: 50, churned_cents: 0, net_cents: 1482 },
    { d: '2026-09-19', new_cents: 0, expansion_cents: 0, contraction_cents: 0, churned_cents: 499, net_cents: -499 }
  ],
  cash: [
    { d: '2026-09-18', charged_cents: 10498, refunded_cents: 0, net_cents: 10498, charges: 2, refunds: 0 },
    { d: '2026-09-20', charged_cents: 0, refunded_cents: 499, net_cents: -499, charges: 0, refunds: 1 }
  ],
  window: { new_mrr_cents: 1332, expansion_mrr_cents: 200, contraction_mrr_cents: 50,
            churned_mrr_cents: 499, charged_cents: 10498, refunded_cents: 499, refunds: 1,
            failed_payments: 0, trials_started: 6, trials_converted: 3,
            subscriptions_started: 1, cancellations: 1, renewals: 2 },
  trial_cohorts: [
    { w: '2026-09-07', started: 4, converted: 3, lapsed: 1, pending: 0, conv_pct: 75.0 },
    { w: '2026-09-14', started: 2, converted: 0, lapsed: 0, pending: 2, conv_pct: null }
  ],
  recent_churn: [{ at: '2026-09-19T00:00:00Z', plan: 'plus', interval: 'month', mrr_cents: 499, source: 'stripe' }],
  recent_refunds: [{ at: '2026-09-20T00:00:00Z', cents: 499, plan: 'plus', source: 'stripe' }],
  by_source: { stripe: 41, apple: 1 }
};

(async () => {
  await new Promise(r => server.listen(0, '127.0.0.1', r));
  PORT = server.address().port;
  const exe = process.env.CHROMIUM_PATH ||
    (fs.readdirSync('/opt/pw-browsers').filter(d => d.startsWith('chromium-'))
       .map(d => '/opt/pw-browsers/' + d + '/chrome-linux/chrome').find(p => fs.existsSync(p)));
  const browser = await chromium.launch({ executablePath: exe });

  for (const theme of ['light', 'dark']) {
    for (const [w, h, wide] of [[1280, 900, true], [390, 844, false]]) {
      const label = theme + ' ' + w + 'px';
      console.log('\n' + label);
      const ctx = await browser.newContext({ viewport: { width: w, height: h },
        colorScheme: theme, deviceScaleFactor: 1 });
      const page = await ctx.newPage();
      const errs = [];
      page.on('console', m => { if (m.type() === 'error' && !noise(m.text())) errs.push(m.text()); });
      page.on('pageerror', e => errs.push(String(e)));

      // Stand in for Supabase before any script runs. The page must never reach the
      // network in a test; what it asked for is the thing under test, not what a server
      // happened to answer.
      await page.addInitScript(fx => {
        window.__rpcCalls = [];
        window.__fixture = fx;
      }, FIXTURE);
      await page.goto(url('/app/#admin-preview'), { waitUntil: 'domcontentloaded' });
      await page.waitForFunction(() => typeof window.renderAdminBusiness === 'function', { timeout: 15000 });

      // The dispatcher and the tab button are part of the deliverable, so assert them
      // before reaching past them to the renderer.
      ok(await page.evaluate(() => /'business','Business'/.test(adminTabsHtml.toString())),
        'Business appears in the admin tab list');

      // The page declares Cloud and adminTab with const/let at script top level, so they
      // are lexical globals and NOT properties of window. Assigning window.Cloud would
      // create a second, unread object; these have to be mutated by name.
      //
      // The hash also has to stop saying admin-preview, because preview mode renders the
      // all-zero sample and would pass every assertion below by accident.
      await page.evaluate(() => {
        const fx = window.__fixture;
        history.replaceState(null, '', '#admin');
        Cloud.client = {
          rpc: async (name, args) => {
            window.__rpcCalls.push([name, args]);
            if (name === 'admin_business') return { data: fx, error: null };
            if (name === 'admin_traffic') return { data: { days: 90, pageviews: 900, sessions: 300,
              by_day: [{ d: '2026-09-18', n: 40, u: 12 }, { d: '2026-09-19', n: 55, u: 19 }],
              funnel: [{ step: 'visit', label: 'Visited', sessions: 300 },
                       { step: 'start', label: 'Started a Session', sessions: 90 }] }, error: null };
            if (name === 'admin_funnel') return { data: [
              { step: 'visit', label: 'Visited', sessions: 300, share_of_visits: 100, share_of_previous: null },
              { step: 'start', label: 'Started a Session', sessions: 90, share_of_visits: 30, share_of_previous: 30 }], error: null };
            return { data: null, error: { message: 'not stubbed: ' + name } };
          }
        };
        Cloud.user = { id: 'u1' };
        Cloud.isAdmin = true;
        adminTab = 'business';
        // A first run opens the onboarding wizard over everything, and leaves every other
        // view hidden. A hidden element still answers innerText and getComputedStyle, so
        // without this the layout assertions below would measure a box that was never
        // laid out and pass on a page nobody could read.
        finishOnboarding(true);
        show('admin');
      });
      await page.evaluate(() => renderAdmin());
      await page.waitForFunction(() => {
        const n = document.getElementById('bizTile0');
        return n && n.textContent.indexOf('$') >= 0;
      }, { timeout: 15000 });

      const text = await page.evaluate(() => document.getElementById('v-admin').innerText);
      const called = await page.evaluate(() => window.__rpcCalls.map(c => c[0]));

      ok(called.indexOf('admin_business') >= 0, 'reads admin_business');
      // 499 monthly + round(9999/12)=833 annual. Printing $109.98 would mean an annual
      // price was counted as a month of revenue, which is the classic version of this bug.
      ok(/\$13\.32/.test(text), 'MRR is $13.32, annual price divided by twelve');
      ok(!/\$109\.98/.test(text), 'annual price is not counted as monthly MRR');
      ok(/\$159\.84/.test(text), 'ARR is MRR times twelve, in cents not dollars');
      ok(/\$9\.83/.test(text), 'net new MRR is new plus expansion less contraction less churn');
      ok(/\$4\.99/.test(text), 'churned MRR is what the leaver was paying');
      ok(/\$104\.98/.test(text), 'cash collected is gross');
      ok(/75%/.test(text), 'trial conversion counts decided cohorts only');
      ok(!/50%/.test(text), 'pending trials are not counted as failures');
      // The provenance line is load bearing: without it every figure silently claims to
      // cover 90 days when the ledger only has 37.
      ok(/Aug 15, 2026/.test(text), 'states the date the ledger begins');
      ok(/less than the window/i.test(text), 'says the ledger is shorter than the window');
      ok(/Churn rate is not shown/i.test(text), 'declines to print a churn rate it cannot compute');
      ok(/\$9\.98/.test(text), 'trial pipeline is stated separately from MRR');

      const svgs = await page.evaluate(() =>
        ['bizMove', 'bizCash', 'bizCoh', 'bizTraf', 'bizFunnel']
          .map(id => { const n = document.getElementById(id); return [id, !!(n && n.innerHTML.trim().length > 40)]; }));
      svgs.forEach(([id, filled]) => ok(filled, 'chart ' + id + ' rendered'));

      // Every chart has a table view, which is the accessibility backstop and also the
      // thing a person wants when copying a figure out.
      const toggles = await page.evaluate(() =>
        document.querySelectorAll('#v-admin .sfnc-tgl').length);
      ok(toggles >= 3, 'charts ship table views (' + toggles + ')');

      const vis = await page.evaluate(() => {
        const n = document.getElementById('v-admin');
        return { shown: !n.classList.contains('hidden'), h: n.getBoundingClientRect().height };
      });
      ok(vis.shown && vis.h > 400, 'the admin view is actually on screen (' + Math.round(vis.h) + 'px tall)');

      const overflow = await page.evaluate(() => {
        const doc = document.documentElement.scrollWidth - document.documentElement.clientWidth;
        const n = document.getElementById('v-admin');
        return Math.max(doc, n.scrollWidth - n.clientWidth);
      });
      ok(overflow <= 1, 'no sideways scroll (' + overflow + 'px)');

      // A chart that hardcodes a colour breaks in the other theme. Read what was painted
      // rather than trusting the token.
      const ink = await page.evaluate(() => {
        const t = document.getElementById('bizTile0');
        const v = t && t.querySelector('div:nth-child(2)');
        const bg = getComputedStyle(document.body).backgroundColor;
        return { fg: v ? getComputedStyle(v).color : '', bg };
      });
      const lum = s => { const m = /rgba?\((\d+),\s*(\d+),\s*(\d+)/.exec(s || '');
        return m ? (0.2126 * +m[1] + 0.7152 * +m[2] + 0.0722 * +m[3]) / 255 : null; };
      const lf = lum(ink.fg), lb = lum(ink.bg);
      ok(lf !== null && lb !== null && Math.abs(lf - lb) > 0.3,
        'tile figure contrasts with the page in ' + theme + ' (fg ' + (lf || 0).toFixed(2) + ' vs bg ' + (lb || 0).toFixed(2) + ')');

      ok(errs.length === 0, 'no console errors' + (errs.length ? ': ' + errs[0] : ''));
      if (wide && theme === 'light') {
        await page.locator('#v-admin').screenshot({ path: '/tmp/business-tab.png' });
      }
      await ctx.close();
    }
  }
  await browser.close();
  server.close();
  console.log('\n' + (fails ? fails + ' FAILED' : 'all business dashboard checks passed'));
  process.exit(fails ? 1 : 0);
})().catch(e => { console.error(e); process.exit(1); });
