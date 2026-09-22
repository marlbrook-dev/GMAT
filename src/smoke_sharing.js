// The data sharing programme, checked against what the pages actually render.
//
// Run with:
//   CHROMIUM_PATH=/opt/pw-browsers/chromium-*/chrome-linux/chrome node src/smoke_sharing.js
//
// Three promises are load-bearing here, and all three are the kind that fail silently.
// Off by default is only true if the switch renders off for an account that has never
// touched it. Closed to under 18s is only true if the control is absent rather than
// present and disabled, because a disabled control is one attribute away from working.
// And the policy has to stop making the opposite promise: a page that says both "we
// never sell" and "we sell under these conditions" is worse than either, because the
// contradiction is what reads as intent to mislead.
//
// The database half of this (the view that excludes minors, the function that refuses a
// non-adult opt-in) is not testable from a browser and is asserted in SQL instead.
const { chromium } = require('playwright');
const { chromiumPath } = require('./chromium_path.js');
const http = require('http'), fs = require('fs'), p0 = require('path');
const ROOT = p0.join(__dirname, '..');
const T = {'.html':'text/html','.js':'text/javascript','.css':'text/css','.png':'image/png',
           '.svg':'image/svg+xml','.json':'application/json','.webmanifest':'application/manifest+json'};
const srv = http.createServer((q, r) => {
  let rel = decodeURIComponent(q.url.split('?')[0]); if (rel.endsWith('/')) rel += 'index.html';
  const f = p0.join(ROOT, rel);
  if (!f.startsWith(ROOT) || !fs.existsSync(f) || fs.statSync(f).isDirectory()) { r.writeHead(404); r.end('nf'); return; }
  r.writeHead(200, {'Content-Type': T[p0.extname(f)] || 'application/octet-stream'});
  fs.createReadStream(f).pipe(r);
});
const noise = t => /ERR_CERT_AUTHORITY_INVALID|fonts\.(googleapis|gstatic)\.com|Failed to fetch|net::ERR/.test(t);
const fails = [];
function check(name, cond, detail) {
  console.log((cond ? '  ok: ' : '  FAIL: ') + name + (detail ? '  -> ' + detail : ''));
  if (!cond) fails.push(name);
}

(async () => {
  await new Promise(r => srv.listen(0, '127.0.0.1', r));
  const P = srv.address().port;
  const url = p => 'http://127.0.0.1:' + P + '/' + String(p).replace(/^\//, '');
  const b = await chromium.launch({ executablePath: chromiumPath() });

  // --- the Account card, across the states the server can report -------------------
  // {sharing, basis, opted_out, tier} is what my_data_sharing returns. `sharing` is
  // computed server side from the export view, so the card never recomputes it.
  const cases = [
    ['never declared an age', {sharing: false, basis: 'opt_out', opted_out: false, tier: 'undeclared'},
     { control: false, says: /birth month and year/i, flag: 'Off' }],
    ['under 13', {sharing: false, basis: 'opt_out', opted_out: false, tier: 'under_13'},
     { control: false, says: /closed to your account/i, flag: 'Off' }],
    ['13 to 17', {sharing: false, basis: 'opt_out', opted_out: false, tier: '13_17'},
     { control: false, says: /closed to your account/i, flag: 'Off' }],
    // The default-on case. This is the one the whole change exists for.
    ['US adult, default on', {sharing: true, basis: 'opt_out', opted_out: false, tier: '18_plus'},
     { control: true, says: /It is on\./, flag: 'On', button: /Turn Data Sharing Off/ }],
    // A refusal is a stored fact, and must read differently from never having been asked.
    ['US adult who opted out', {sharing: false, basis: 'opt_out', opted_out: true, tier: '18_plus'},
     { control: true, says: /because you turned it off/i, flag: 'Off', button: /Turn Data Sharing Back On/ }],
    // GDPR: no opt out exists for this, so the card must not imply one was declined.
    ['EU adult, asked first', {sharing: false, basis: 'opt_in', opted_out: false, tier: '18_plus'},
     { control: true, says: /we have to ask before sharing/i, flag: 'Off', button: /Turn Data Sharing On/ }],
    ['EU adult who opted in', {sharing: true, basis: 'opt_in', opted_out: false, tier: '18_plus'},
     { control: true, says: /It is on\./, flag: 'On', button: /Turn Data Sharing Off/ }],
    // Predates the disclosure: the changed default must not reach back.
    ['account older than the policy', {sharing: false, basis: 'opt_out', opted_out: false, tier: '18_plus'},
     { control: true, says: /before we published the data sharing policy/i, flag: 'Off',
       button: /Turn Data Sharing On/ }],
  ];
  for (const [name, sharing, want] of cases) {
    const p = await b.newPage({ viewport: { width: 390, height: 844 } });
    const errs = [];
    p.on('pageerror', e => { if (!noise(e.message)) errs.push('pageerror: ' + e.message); });
    p.on('console', m => { if (m.type() === 'error' && !noise(m.text())) errs.push('console: ' + m.text()); });
    await p.addInitScript(s => { window.__sh = s; }, sharing);
    await p.goto(url('app/index.html'), { waitUntil: 'load' });
    await p.evaluate(() => {
      Cloud.user = { id: 'u', email: 'a@b.c' }; Cloud.plan = 'free'; Cloud.billing = null;
      // renderData keys off status, not user: the supabase CDN is unreachable from here
      // so init leaves it on local-only and every signed-in branch would be skipped.
      Cloud.status = 'signed-in';
      Cloud.sharing = window.__sh; show('data');
    });
    await p.waitForTimeout(150);
    const html = await p.evaluate(() => document.getElementById('v-data').innerHTML);
    const txt = await p.evaluate(() => document.getElementById('v-data').innerText);

    check('[' + name + '] no errors', errs.length === 0, errs.join(' | '));
    // Absent, not disabled. A disabled control is one attribute away from working.
    check('[' + name + '] switch ' + (want.control ? 'present' : 'absent'),
      /onclick="shareSet\(/.test(html) === want.control);
    check('[' + name + '] says the right thing', want.says.test(txt),
      want.says.test(txt) ? '' : txt.slice(0, 160).replace(/\n/g, ' '));
    // The badge has to read the state, because the badge is what people scan.
    const badge = await p.evaluate(() => {
      const c = [...document.querySelectorAll('#v-data .card')]
        .find(x => (x.querySelector('.card-title') || {}).textContent === 'Data Sharing');
      const bd = c && c.querySelector('.card-head .badge, .card-head span:not(.card-title)');
      return bd ? bd.textContent.trim() : '(none)';
    });
    check('[' + name + '] badge reads ' + want.flag, badge === want.flag, badge);
    // The age gate never asks for a day, on any path.
    check('[' + name + '] birth day is never asked for',
      !/bDay|birth day|Birth day/i.test(html));
    if (want.button) {
      const label = await p.evaluate(() => {
        const c = [...document.querySelectorAll('#v-data .card')]
          .find(x => (x.querySelector('.card-title') || {}).textContent === 'Data Sharing');
        const b = c && c.querySelector('button[onclick^="shareSet"]');
        return b ? b.textContent.trim() : '(none)';
      });
      check('[' + name + '] button offers the right action', want.button.test(label), label);
    }
    const wide = await p.evaluate(() => document.documentElement.scrollWidth > window.innerWidth + 2);
    check('[' + name + '] no horizontal overflow at 390px', !wide);
    await p.close();
  }

  // --- the Do Not Sell page --------------------------------------------------------
  for (const [who, gpc] of [['without GPC', false], ['with GPC', true]]) {
    const ctx = await b.newContext({ viewport: { width: 390, height: 844 } });
    const p = await ctx.newPage();
    const errs = [];
    p.on('pageerror', e => { if (!noise(e.message)) errs.push('pageerror: ' + e.message); });
    p.on('console', m => { if (m.type() === 'error' && !noise(m.text())) errs.push('console: ' + m.text()); });
    if (gpc) await p.addInitScript(() => {
      try { Object.defineProperty(navigator, 'globalPrivacyControl', { get: () => true }); } catch (e) {}
    });
    await p.goto(url('do-not-sell/'), { waitUntil: 'load' });
    await p.waitForTimeout(400);
    const txt = await p.evaluate(() => document.body.innerText);
    check('[do-not-sell ' + who + '] no errors', errs.length === 0, errs.join(' | '));
    check('[do-not-sell ' + who + '] no dashes', !/[–—]/.test(txt));
    check('[do-not-sell ' + who + '] states the under 18 exclusion',
      /under 18 under any circumstances/.test(txt));
    check('[do-not-sell ' + who + '] names what is excluded at every setting',
      /practice answers/.test(txt) && /payment details/.test(txt));
    check('[do-not-sell ' + who + '] says it cannot recall a delivered copy',
      /cannot recall a copy already delivered/.test(txt));
    check('[do-not-sell ' + who + '] no discrimination promise', /will not discriminate/.test(txt));
    check('[do-not-sell ' + who + '] covers purchased attributes too',
      /bought details about you from a data partner/.test(txt));
    check('[do-not-sell ' + who + '] the control resolved out of its loading state',
      !/Checking Your Current Setting/.test(txt), txt.slice(0, 120).replace(/\n/g, ' '));
    if (gpc) check('[do-not-sell with GPC] says the signal is being honoured',
      /sending a Global Privacy Control signal right now/.test(txt));
    const wide = await p.evaluate(() => document.documentElement.scrollWidth > window.innerWidth + 2);
    check('[do-not-sell ' + who + '] no horizontal overflow at 390px', !wide);
    await ctx.close();
  }

  // --- the policy has to stop saying the opposite ----------------------------------
  {
    const p = await b.newPage({ viewport: { width: 1280, height: 900 } });
    await p.goto(url('privacy.html'), { waitUntil: 'load' });
    const txt = await p.evaluate(() => document.body.innerText);
    const contradictions = [
      'We do not sell personal data and we do not run third-party ad trackers',
      'We do not sell or share personal information as those terms are defined',
      'we never sell or share personal data with data brokers',
      // The no-buy promises, removed when the owner decided we buy and append. If any of
      // them comes back, the page promises one thing and section 2 describes another.
      'never buy them, and never append them from a third party',
      'never buy it, and never append it from anywhere else',
      'We do not buy data about you',
      // The opt in wording, removed when the default flipped. A policy describing an opt
      // in while the database runs an opt out is the worst of both: the disclosure fails
      // AND the selling happens.
      'It is off unless you switch it on',
      'data sharing programme that is open only to adults who opt in',
    ];
    const found = contradictions.filter(c => txt.includes(c));
    check('privacy page no longer promises the opposite', found.length === 0, found.join(' | '));
    check('privacy page discloses the programme', /The Data Sharing Programme/.test(txt));
    check('privacy page states the under 18 exclusion',
      /closed to you and cannot be switched on/.test(txt));
    check('privacy page excludes data collected under the old promise',
      /you were told we would never sell your data/.test(txt));
    check('privacy page names the recipients', /may include data brokers/.test(txt));
    check('privacy page carries the California disclosure',
      /We do sell and share personal information as California law defines those words/.test(txt));
    check('privacy page links the opt out', /Do Not Sell or Share My Personal Information/.test(txt));
    check('privacy page no dashes', !/[–—]/.test(txt));
    // Buying is lawful on notice, so the notice has to be there and has to say the things
    // that make it one: that we buy, which categories, from whom, and who is excluded.
    check('privacy page discloses that we buy data',
      /we may buy attributes about you from data partners/.test(txt));
    check('privacy page names the categories bought',
      /education, field of study, career stage and industry/.test(txt));
    check('privacy page says nothing is bought about a minor',
      /We buy nothing about anyone under 18/.test(txt));
    check('privacy page keeps purchased values out of the declared fields',
      /never written into the fields you filled in/.test(txt));
    check('privacy page offers access and deletion of purchased data',
      /Ask what is attached to your account/.test(txt));
    check('privacy page rules out credit and employment uses',
      /credit, employment, housing or\s+insurance/.test(txt));
    check('the summary mentions buying too',
      /nothing about anyone\s+under 18 is ever bought/.test(txt));
    check('privacy page says sharing is on by default for most adults',
      /it is on unless you turn it off/i.test(txt));
    check('privacy page says the EEA, UK and Switzerland are asked first',
      /it is off until you switch it on/i.test(txt));
    check('privacy page still excludes accounts older than the policy',
      /Changing the default does not reach back to you/.test(txt));
    check('privacy page still states the under 18 exclusion under the new default',
      /closed to you entirely and cannot be switched on/.test(txt));
    await p.close();
  }

  // --- the link has to be on every page, which is what conspicuous means -----------
  {
    const pages = ['index.html', 'privacy.html', 'terms.html', 'pricing/index.html',
                   'colleges/index.html', 'schools/index.html', 'blog/index.html',
                   'exams/index.html', 'community/index.html', 'funding/index.html',
                   'scoring/index.html', 'international/index.html', 'apply/index.html'];
    for (const page of pages) {
      const f = p0.join(ROOT, page);
      if (!fs.existsSync(f)) { check('footer link on /' + page, false, 'page not built'); continue; }
      const p = await b.newPage({ viewport: { width: 1280, height: 900 } });
      await p.goto(url(page), { waitUntil: 'domcontentloaded' });
      const has = await p.evaluate(() =>
        !![...document.querySelectorAll('footer a')].find(a => a.getAttribute('href') === '/do-not-sell/'));
      check('footer link on /' + page, has);
      await p.close();
    }
  }

  await b.close(); srv.close();
  console.log(fails.length ? '\nFAILURES: ' + fails.join(', ')
                           : '\nall data sharing checks passed');
  process.exit(fails.length ? 1 : 0);
})();
