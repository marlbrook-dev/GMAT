// Billing validation. Run with:
//   CHROMIUM_PATH=/opt/pw-browsers/chromium-*/chrome-linux/chrome \
//   NODE_PATH=/opt/node22/lib/node_modules node src/smoke_billing.js
//
// Two things it guards.
//
// 1. The free tier never asks for a card. Not "does not today": the free tile must render
//    no checkout control at all, for a signed-out visitor and for a signed-in free user
//    alike, and the page must say so in words. If someone ever adds a Stripe button to the
//    free tile, or the promise copy drifts away from the behaviour, this fails.
//
// 2. The Account card tells the truth about money in every subscription state, and Cancel
//    Plan is reachable whenever there is something to cancel.
const { chromium } = require('playwright');
const path = require('path');
const http = require('http');
const fs = require('fs');
const path0 = require('path');
const ROOT = path0.resolve(__dirname, '..');

// Served over HTTP rather than read off disk, because the trainer loads its item bank
// from /app/bank.js. An absolute path like that has no meaning under file://, so a
// file:// run would test a page whose bank never arrives, which is not the page anyone
// visits. This also matches how Cloudflare serves the built site.
const TYPES = { '.html': 'text/html', '.js': 'text/javascript', '.css': 'text/css',
                '.json': 'application/json', '.svg': 'image/svg+xml', '.png': 'image/png',
                '.webmanifest': 'application/manifest+json', '.txt': 'text/plain' };
const server = http.createServer((req, res) => {
  let rel = decodeURIComponent(req.url.split('?')[0]);
  if (rel.endsWith('/')) rel += 'index.html';
  const file = path0.join(ROOT, rel);
  if (!file.startsWith(ROOT) || !fs.existsSync(file) || fs.statSync(file).isDirectory()) {
    if(process.env.SMOKE_DEBUG) console.log('404 ->', rel);
    res.writeHead(404); res.end('not found'); return;
  }
  res.writeHead(200, { 'Content-Type': TYPES[path0.extname(file)] || 'application/octet-stream' });
  fs.createReadStream(file).pipe(res);
});
let PORT = 0;
const url = p => 'http://127.0.0.1:' + PORT + '/' + String(p).replace(/^\//, '');
const noise = t => /ERR_CERT_AUTHORITY_INVALID|fonts\.(googleapis|gstatic)\.com|Failed to fetch|net::ERR/.test(t);

(async () => {
  await new Promise(r => server.listen(0, '127.0.0.1', r));
  PORT = server.address().port;
  const b = await chromium.launch({ executablePath: process.env.CHROMIUM_PATH });
  let fail = 0;
  const check = (name, ok, extra) => { console.log((ok ? '  ok: ' : '  FAIL: ') + name + (extra ? ' -> ' + extra : '')); if (!ok) fail++; };

  for (const page of ['terms.html', 'privacy.html', 'pricing/index.html']) {
    const p = await b.newPage({ viewport: { width: 1280, height: 900 } });
    const errs = [];
    p.on('pageerror', e => { if (!noise(e.message)) errs.push('pageerror: ' + e.message); });
    p.on('console', m => { if (m.type() === 'error' && !noise(m.text())) errs.push('console: ' + m.text()); });
    await p.goto(url(page), { waitUntil: 'load' });
    const txt = await p.evaluate(() => document.body.innerText);
    check(page + ' no console errors', errs.length === 0, errs.join(' | '));
    check(page + ' no dashes', !/[–—]/.test(txt));
    if (page !== 'privacy.html') check(page + ' mentions the 7-day trial', /7-day free trial/.test(txt));
    if (page === 'privacy.html') check(page + ' names Stripe as processor', /Stripe/.test(txt) && /72/.test(txt) === false);
    if (page !== 'privacy.html') check(page + ' mentions one-click cancel', /Cancel Plan/.test(txt));
    const wide = await p.evaluate(() => document.documentElement.scrollWidth > window.innerWidth + 2);
    check(page + ' no horizontal overflow', !wide);
    await p.close();
  }

  // Account view across subscription states. Cloud is stubbed before the app boots so the
  // card renders without a network round trip.
  const states = [
    ['free, never subscribed', { plan: 'free', billing: null }, { cancel: false, portal: false, line: '' }],
    ['trialing', { plan: 'plus', billing: { status: 'trialing', trialEnd: '2026-09-23T00:00:00Z', periodEnd: '2026-09-23T00:00:00Z', cancelAtEnd: false, hasCustomer: true } }, { cancel: true, portal: true, line: 'Free trial through' }],
    ['trial cancelled', { plan: 'plus', billing: { status: 'trialing', trialEnd: '2026-09-23T00:00:00Z', periodEnd: '2026-09-23T00:00:00Z', cancelAtEnd: true, hasCustomer: true } }, { cancel: false, portal: true, line: 'will not convert' }],
    ['active', { plan: 'pro', billing: { status: 'active', trialEnd: null, periodEnd: '2026-10-16T00:00:00Z', cancelAtEnd: false, hasCustomer: true } }, { cancel: true, portal: true, line: 'renews on' }],
    ['active, cancelling', { plan: 'pro', billing: { status: 'active', trialEnd: null, periodEnd: '2026-10-16T00:00:00Z', cancelAtEnd: true, hasCustomer: true } }, { cancel: false, portal: true, line: 'Cancelled.' }],
    ['past due', { plan: 'plus', billing: { status: 'past_due', trialEnd: null, periodEnd: '2026-10-16T00:00:00Z', cancelAtEnd: false, hasCustomer: true } }, { cancel: true, portal: true, line: 'did not go through' }],
  ];
  for (const [name, stub, want] of states) {
    const p = await b.newPage({ viewport: { width: 1280, height: 900 } });
    const errs = [];
    p.on('pageerror', e => { if (!noise(e.message)) errs.push('pageerror: ' + e.message); });
    p.on('console', m => { if (m.type() === 'error' && !noise(m.text())) errs.push('console: ' + m.text()); });
    await p.addInitScript(s => { window.__stub = s; }, stub);
    await p.goto(url('app/index.html'), { waitUntil: 'load' });
    await p.evaluate(() => {
      Cloud.plan = window.__stub.plan; Cloud.billing = window.__stub.billing;
      Cloud.user = window.__stub.billing ? { id: 'u', email: 'a@b.c' } : null;
      show('data');
    });
    await p.waitForTimeout(150);
    const html = await p.evaluate(() => document.getElementById('v-data').innerHTML);
    const txt = await p.evaluate(() => document.getElementById('v-data').innerText);
    check('[' + name + '] no errors', errs.length === 0, errs.join(' | '));
    check('[' + name + '] Cancel Plan button ' + (want.cancel ? 'present' : 'absent'), /onclick="cancelPlan\(\)"/.test(html) === want.cancel);
    check('[' + name + '] Manage Billing ' + (want.portal ? 'present' : 'absent'), /onclick="openBillingPortal\(\)"/.test(html) === want.portal);
    if (want.line) check('[' + name + '] status line', txt.includes(want.line), (await p.evaluate(() => { const ps=[...document.querySelectorAll('#v-data p.small strong')]; return ps.length?ps[0].innerText:'(no status paragraph)'; })));
    check('[' + name + '] free plan no-card promise', /never asks for a card/.test(txt));
    await p.close();
  }
  // The free tier never asks for a card. Checked head on, in both auth states, because
  // this is a promise printed on the pricing page, in the Account card and in the Terms.
  for (const [who, signIn] of [['signed out', false], ['signed in, free plan', true]]) {
    const p = await b.newPage({ viewport: { width: 1280, height: 900 } });
    const errs = [];
    p.on('pageerror', e => { if (!noise(e.message)) errs.push('pageerror: ' + e.message); });
    p.on('console', m => { if (m.type() === 'error' && !noise(m.text())) errs.push('console: ' + m.text()); });
    await p.goto(url('app/index.html'), { waitUntil: 'load' });
    await p.evaluate(s => {
      Cloud.plan = 'free'; Cloud.billing = null;
      Cloud.user = s ? { id: 'u', email: 'a@b.c' } : null;
      show('data');
    }, signIn);
    await p.waitForTimeout(150);
    const tiles = await p.evaluate(() => {
      const t = [...document.querySelectorAll('#v-data .tile')].find(x => /^free\b/i.test(x.innerText));
      return t ? { html: t.innerHTML, text: t.innerText } : null;
    });
    check('[free tier, ' + who + '] tile rendered', !!tiles);
    if (tiles) {
      check('[free tier, ' + who + '] no checkout control', !/startCheckout|openBillingPortal/.test(tiles.html), tiles.html.slice(0, 160));
      check('[free tier, ' + who + '] no card wording', !/card number|payment method|enter your card/i.test(tiles.text));
    }
    const body = await p.evaluate(() => document.getElementById('v-data').innerText);
    check('[free tier, ' + who + '] states the promise', /never asks for a card/.test(body));
    check('[free tier, ' + who + '] no errors', errs.length === 0, errs.join(' | '));
    await p.close();
  }

  await b.close();
  server.close();
  console.log(fail ? '\n' + fail + ' CHECK(S) FAILED' : '\nall billing checks passed');
  process.exit(fail ? 1 : 0);
})();
