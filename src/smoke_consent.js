// Consent and item-telemetry validation. Run with:
//   CHROMIUM_PATH=/opt/pw-browsers/chromium-*/chrome-linux/chrome \
//   NODE_PATH=/opt/node22/lib/node_modules node src/smoke_consent.js
//
// A consent banner that is present but not valid is worse than no banner: it collects
// the data anyway and fails the law as well. So this asserts the behaviour, not the
// markup.
//
//   Nothing analytic is sent before a visitor chooses.
//   Rejecting is one click in the same place as accepting, and it sends nothing.
//   Accepting sends, and the choice survives a reload without asking again.
//   Withdrawing consent stops the beacon on the page you withdrew it from.
//   A Global Privacy Control signal counts as a rejection and the banner never shows.
//   Every page can reopen the choice from the footer.
//
// It also asserts the other half of the design: item telemetry fires when a question is
// answered, and the body it posts carries no user, session, device or address field. That
// absence is the whole reason it is allowed to run without consent, so it is tested rather
// than assumed.
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
const noise = t => /ERR_CERT_AUTHORITY_INVALID|fonts\.(googleapis|gstatic)\.com|Failed to fetch|net::ERR/.test(t);

// Supabase is not reachable from a test run and must not be called from one either.
// Every REST write is intercepted, recorded and answered locally, so the assertions are
// about what the page tried to send rather than about what a server happened to accept.
async function instrument(ctx) {
  const sent = { site: [], item: [], other: [] };
  await ctx.route('**/rest/v1/**', route => {
    const u = route.request().url();
    let body = null;
    try { body = JSON.parse(route.request().postData() || 'null'); } catch (e) {}
    if (/site_events/.test(u)) sent.site.push(body);
    else if (/item_events/.test(u)) sent.item.push(body);
    else sent.other.push(u);
    route.fulfill({ status: 201, contentType: 'application/json', body: '[]' });
  });
  await ctx.route('**/auth/v1/**', route =>
    route.fulfill({ status: 200, contentType: 'application/json', body: '{}' }));
  return sent;
}

// --- the dialog itself -------------------------------------------------------------
// Rebuilt as a centred modal rather than a bottom bar. These check the properties that
// make it a dialog rather than a div that looks like one, plus the two states that must
// agree with the Do Not Sell page.
async function checkDialog(b, base, check) {
  const ctx = await b.newContext({ viewport: { width: 390, height: 844 } });
  const pg = await ctx.newPage();
  await pg.goto(base + '/', { waitUntil: 'domcontentloaded' });
  await pg.waitForTimeout(400);

  const d = await pg.evaluate(() => {
    const el = document.getElementById('sfn-consent');
    if (!el) return null;
    const cs = getComputedStyle(el);
    const t = document.getElementById('sfn-nosell');
    return {
      shown: !el.hidden,
      role: el.getAttribute('role'),
      modal: el.getAttribute('aria-modal'),
      labelled: !!el.getAttribute('aria-labelledby'),
      position: cs.position,
      centred: cs.alignItems === 'center' && cs.justifyContent === 'center',
      hasToggle: !!t,
      toggleIsRealCheckbox: t ? t.type === 'checkbox' : false,
    };
  });
  check('dialog is present on first visit', !!d && d.shown);
  check('dialog is a dialog', !!d && d.role === 'dialog' && d.modal === 'true' && d.labelled,
    d ? d.role + '/' + d.modal : 'missing');
  check('dialog is centred', !!d && d.position === 'fixed' && d.centred);
  // A styled span is not focusable and is not announced. The switch has to be drawn from
  // a real checkbox or it is unusable with a keyboard or a screen reader.
  check('the sell toggle is a real checkbox', !!d && d.hasToggle && d.toggleIsRealCheckbox);

  // It has to go away on a choice, and stay gone on the next page load.
  await pg.evaluate(() => sfnConsent(true));
  await pg.waitForTimeout(150);
  check('dialog closes on a choice',
    await pg.evaluate(() => document.getElementById('sfn-consent').hidden));
  await pg.reload({ waitUntil: 'domcontentloaded' });
  await pg.waitForTimeout(400);
  check('dialog stays closed on the next visit',
    await pg.evaluate(() => document.getElementById('sfn-consent').hidden));

  // The toggle and the Do Not Sell page share one key, so a choice made in one is true in
  // the other. Two controls over one decision that disagree is worse than either alone.
  await pg.evaluate(() => { sfnConsentReopen(); sfnNoSellToggle(true); });
  await pg.waitForTimeout(150);
  check('the toggle writes the Do Not Sell key',
    await pg.evaluate(() => {
      try { return !!JSON.parse(localStorage.getItem('sfn_no_sell_v1') || 'null').optOut; }
      catch (e) { return false; }
    }));
  check('sfnNoSell agrees with it', await pg.evaluate(() => sfnNoSell() === true));
  await pg.evaluate(() => sfnNoSellToggle(false));
  await pg.waitForTimeout(100);
  check('turning it back off clears the key',
    await pg.evaluate(() => localStorage.getItem('sfn_no_sell_v1') === null));
  await ctx.close();

  // GPC must lock the toggle on rather than offer to undo a refusal the browser made.
  const g = await b.newContext({ viewport: { width: 390, height: 844 } });
  const gp = await g.newPage();
  await gp.addInitScript(() => {
    try { Object.defineProperty(navigator, 'globalPrivacyControl', { get: () => true }); } catch (e) {}
  });
  await gp.goto(base + '/', { waitUntil: 'domcontentloaded' });
  await gp.waitForTimeout(300);
  await gp.evaluate(() => sfnConsentReopen());
  await gp.waitForTimeout(200);
  const gs = await gp.evaluate(() => {
    const t = document.getElementById('sfn-nosell');
    return t ? { checked: t.checked, disabled: t.disabled } : null;
  });
  check('GPC locks the toggle on', !!gs && gs.checked && gs.disabled,
    gs ? JSON.stringify(gs) : 'no toggle');
  await g.close();
}

(async () => {
  await new Promise(r => server.listen(0, '127.0.0.1', r));
  PORT = server.address().port;
  const b = await chromium.launch({ executablePath: process.env.CHROMIUM_PATH });
  let fail = 0;
  const check = (name, ok, extra) => {
    console.log((ok ? '  ok: ' : '  FAIL: ') + name + (extra ? ' -> ' + extra : ''));
    if (!ok) fail++;
  };
  const settle = p => p.waitForTimeout(350);

  // 1. First visit: the banner asks, and nothing analytic has been sent.
  {
    const ctx = await b.newContext({ viewport: { width: 1280, height: 900 } });
    const sent = await instrument(ctx);
    const p = await ctx.newPage();
    const errs = [];
    p.on('pageerror', e => { if (!noise(e.message)) errs.push('pageerror: ' + e.message); });
    p.on('console', m => { if (m.type() === 'error' && !noise(m.text())) errs.push('console: ' + m.text()); });
    await p.goto(url('index.html'), { waitUntil: 'load' });
    await settle(p);
    check('landing has no console errors', errs.length === 0, errs.join(' | '));
    check('banner is shown on a first visit', await p.isVisible('#sfn-consent'));
    check('nothing analytic sent before a choice', sent.site.length === 0, JSON.stringify(sent.site));

    // Refusing must be exactly as easy as accepting: same container, same kind of control.
    const geo = await p.evaluate(() => {
      const y = document.querySelector('#sfn-consent .yes').getBoundingClientRect();
      const n = document.querySelector('#sfn-consent .no').getBoundingClientRect();
      return { dy: Math.abs(y.top - n.top), ratio: n.width * n.height / (y.width * y.height) };
    });
    check('reject sits beside accept, same size', geo.dy < 4 && geo.ratio > 0.6 && geo.ratio < 1.7,
          JSON.stringify(geo));

    await p.click('#sfn-consent .no');
    await settle(p);
    check('banner closes on reject', !(await p.isVisible('#sfn-consent')));
    check('reject sends nothing', sent.site.length === 0, JSON.stringify(sent.site));

    await p.goto(url('pricing/index.html'), { waitUntil: 'load' });
    await settle(p);
    check('reject is remembered across pages', !(await p.isVisible('#sfn-consent')));
    check('reject still sends nothing on the next page', sent.site.length === 0, JSON.stringify(sent.site));

    // The choice has to be changeable, or it is not a choice.
    check('footer offers Privacy Choices', await p.isVisible('.sfn-consent-open'));
    await p.click('.sfn-consent-open');
    await settle(p);
    check('footer control reopens the banner', await p.isVisible('#sfn-consent'));
    const now = (await p.textContent('#sfn-consent-now')) || '';
    check('reopened banner states the choice in force', /off right now/.test(now), now.slice(0, 80));
    await ctx.close();
  }

  // 2. Accepting sends a pageview, and does not ask again.
  {
    const ctx = await b.newContext({ viewport: { width: 1280, height: 900 } });
    const sent = await instrument(ctx);
    const p = await ctx.newPage();
    await p.goto(url('index.html'), { waitUntil: 'load' });
    await settle(p);
    await p.click('#sfn-consent .yes');
    await settle(p);
    check('accept sends exactly one pageview', sent.site.length === 1 && sent.site[0].kind === 'pageview',
          JSON.stringify(sent.site));
    const pv = sent.site[0] || {};
    check('pageview carries no raw address and no account', !('ip' in pv) && !('email' in pv) && !('user_id' in pv),
          Object.keys(pv).join(','));
    await p.goto(url('index.html'), { waitUntil: 'load' });
    await settle(p);
    check('accept is remembered, no second ask', !(await p.isVisible('#sfn-consent')));
    check('second visit sends its own pageview', sent.site.filter(x => x && x.kind === 'pageview').length === 2,
          String(sent.site.length));

    // Withdrawing has to bite immediately, not at the next page load.
    const before = sent.site.length;
    await p.click('.sfn-consent-open');
    await settle(p);
    await p.click('#sfn-consent .no');
    await p.evaluate(() => document.dispatchEvent(new Event('visibilitychange')));
    await settle(p);
    check('withdrawing stops the beacon on this page', sent.site.length === before,
          JSON.stringify(sent.site.slice(before)));
    await ctx.close();
  }

  // 3. Global Privacy Control is a refusal in law. Asking after it is the dark pattern.
  {
    const ctx = await b.newContext({ viewport: { width: 1280, height: 900 } });
    const sent = await instrument(ctx);
    await ctx.addInitScript(() => {
      Object.defineProperty(navigator, 'globalPrivacyControl', { get: () => true });
    });
    const p = await ctx.newPage();
    await p.goto(url('index.html'), { waitUntil: 'load' });
    await settle(p);
    check('GPC suppresses the banner', !(await p.isVisible('#sfn-consent')));
    check('GPC sends nothing', sent.site.length === 0, JSON.stringify(sent.site));
    await ctx.close();
  }

  // 4. Item telemetry: fires on an answer, and carries nothing that identifies anyone.
  {
    const ctx = await b.newContext({ viewport: { width: 1280, height: 900 } });
    const sent = await instrument(ctx);
    const p = await ctx.newPage();
    const errs = [];
    p.on('pageerror', e => { if (!noise(e.message)) errs.push('pageerror: ' + e.message); });
    p.on('console', m => { if (m.type() === 'error' && !noise(m.text())) errs.push('console: ' + m.text()); });
    await p.goto(url('app/index.html'), { waitUntil: 'load' });
    // BANK is a top-level const, so it lives in the global lexical scope rather than on
    // window; evaluate sees it, window.BANK does not.
    await p.waitForFunction(() => typeof BANK !== 'undefined' && BANK.length > 0, null,
                            { timeout: 30000 });
    await settle(p);
    check('trainer has no console errors', errs.length === 0, errs.join(' | '));
    // A first run opens the onboarding wizard over everything, including the banner.
    await p.evaluate(() => { if (document.getElementById('onb')) finishOnboarding(true); });
    await settle(p);
    check('trainer shows the banner too', await p.isVisible('#sfn-consent'));

    // Reject first, so what follows proves telemetry is independent of the analytics choice.
    await p.click('#sfn-consent .no');
    await settle(p);

    // Drive one question to a graded, recorded answer through the real UI. The round is
    // seeded with a plain multiple choice item so the path is select, submit, then next;
    // grid-in and two-part items have their own inputs and are not what is under test.
    const qid = await p.evaluate(() => {
      const q = BANK.find(x => !x.answerType && Array.isArray(x.choices) && x.choices.length > 1);
      if (!q) return null;
      beginSession([q], 'drill');
      return q.id;
    });
    check('bank has a plain multiple choice item to drive', !!qid);
    await p.waitForSelector('.opt', { timeout: 10000 });
    await p.click('.opt');
    await p.click('#submitBtn');
    await p.waitForSelector('#fb .why', { timeout: 10000 });
    // A missed question needs a reason tagged before the engine will record the attempt.
    if (await p.isVisible('.reason button')) await p.click('.reason button');
    await p.click('#actionBtn button');
    await settle(p);

    check('answering posts one item event', sent.item.length === 1, JSON.stringify(sent.item).slice(0, 200));
    const ev = sent.item[0] || {};
    check('item event names the item and the option chosen',
          ev.qid === qid && typeof ev.chosen === 'number'
          && typeof ev.correct === 'boolean' && typeof ev.secs === 'number' && ev.mode === 'drill',
          JSON.stringify(ev));
    const forbidden = ['user_id', 'sid', 'session_id', 'device', 'ip', 'ip_hash', 'email', 'ua', 'ref'];
    const leaked = Object.keys(ev).filter(k => forbidden.indexOf(k) > -1);
    check('item event carries nothing that identifies anyone',
          sent.item.length > 0 && leaked.length === 0,
          leaked.join(',') || (sent.item.length ? 'clean' : 'no event to inspect'));
    check('item telemetry does not depend on the analytics choice', sent.site.length === 0,
          JSON.stringify(sent.site));
    await ctx.close();
  }

  // 5. The privacy page has to describe what actually happens, or the banner is a lie.
  {
    const ctx = await b.newContext({ viewport: { width: 1280, height: 900 } });
    await instrument(ctx);
    const p = await ctx.newPage();
    await p.goto(url('privacy.html'), { waitUntil: 'load' });
    const txt = await p.evaluate(() => document.body.innerText);
    check('privacy page discloses the consent gate', /only with your consent/i.test(txt));
    check('privacy page discloses item telemetry', /item telemetry/i.test(txt));
    check('privacy page names Global Privacy Control', /Global Privacy Control/.test(txt));
    check('privacy page says how to change the choice', /Privacy Choices/.test(txt));
    check('privacy page has no dashes', !/[\u2013\u2014]/.test(txt));
    await ctx.close();
  }

  // 6. The admin Items tab is the only thing that reads item telemetry back. A tab that
  //    throws, or that renders the flag rules into nothing, means the data is collected
  //    and never looked at, which is the worst of both worlds.
  for (const app of ['app', 'sat/app', 'act/app']) {
    const ctx = await b.newContext({ viewport: { width: 1400, height: 1000 } });
    await instrument(ctx);
    const p = await ctx.newPage();
    const errs = [];
    p.on('pageerror', e => { if (!noise(e.message)) errs.push('pageerror: ' + e.message); });
    p.on('console', m => { if (m.type() === 'error' && !noise(m.text())) errs.push('console: ' + m.text()); });
    await p.goto(url(app + '/index.html#admin-preview'), { waitUntil: 'load' });
    await p.waitForFunction(() => typeof BANK !== 'undefined' && BANK.length > 0, null, { timeout: 30000 });
    await p.evaluate(() => { if (document.getElementById('onb')) finishOnboarding(true); });
    await p.evaluate(() => { adminTab = 'items'; show('admin'); });
    await p.waitForTimeout(600);
    const txt = await p.evaluate(() => document.getElementById('v-admin').innerText);
    check(app + ' items tab renders', /Items/.test(txt) && /Every Item With/.test(txt));
    // The flag labels are uppercased by CSS, so innerText reports them uppercase.
    check(app + ' items tab applies the flag rules',
          /check the key/i.test(txt) && /no discrimination/i.test(txt) && /dead option/i.test(txt));
    // Read Item has to resolve a qid back to the stem people actually saw, or a flag is
    // a number with nothing behind it.
    const qid = await p.evaluate(() => {
      const q = BANK.find(x => Array.isArray(x.choices) && x.choices.length > 1);
      itOpen(q.id); return q.id;
    });
    await p.waitForTimeout(250);
    const modal = await p.evaluate(() => document.body.innerText.slice(0, 4000));
    check(app + ' Read Item shows the stem and marks the key',
          modal.indexOf(qid) > -1 && /\(key\)/.test(modal));
    check(app + ' items tab has no console errors', errs.length === 0, errs.join(' | '));
    const wide = await p.evaluate(() => document.documentElement.scrollWidth > window.innerWidth + 2);
    check(app + ' items tab has no horizontal overflow', !wide);
    await ctx.close();
  }

  await checkDialog(b, 'http://127.0.0.1:' + PORT, check);

  await b.close();
  server.close();
  console.log(fail ? '\nFAILED (' + fail + ')' : '\nall consent and telemetry checks passed');
  process.exit(fail ? 1 : 0);
})();
