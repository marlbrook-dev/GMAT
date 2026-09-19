// The funnel beacon, checked against what it actually sends.
//
// A beacon that silently does not fire is worse than no beacon: it produces a funnel
// full of zeros that reads as "nobody converts" rather than "nothing is recorded".
// So this intercepts the requests rather than trusting the code to be wired.
const { chromium } = require('playwright');
const http = require('http'), fs = require('fs'), p0 = require('path');
const ROOT = p0.join(__dirname, '..');
const T = {'.html':'text/html','.js':'text/javascript','.css':'text/css','.png':'image/png','.svg':'image/svg+xml','.json':'application/json','.webmanifest':'application/manifest+json'};
const srv = http.createServer((q, r) => {
  let rel = decodeURIComponent(q.url.split('?')[0]); if (rel.endsWith('/')) rel += 'index.html';
  const f = p0.join(ROOT, rel);
  if (!fs.existsSync(f) || fs.statSync(f).isDirectory()) { r.writeHead(404); r.end('nf'); return; }
  r.writeHead(200, {'Content-Type': T[p0.extname(f)] || 'application/octet-stream'});
  fs.createReadStream(f).pipe(r);
});
const fails = [];
function check(name, cond, detail) {
  console.log((cond ? '  ok: ' : '  FAIL: ') + name + (detail ? '  ' + detail : ''));
  if (!cond) fails.push(name);
}

(async () => {
  await new Promise(r => srv.listen(0, '127.0.0.1', r));
  const P = srv.address().port;
  const b = await chromium.launch({ executablePath: process.env.CHROMIUM_PATH });

  // --- with consent granted: the milestones must actually be sent ----------------
  {
    const ctx = await b.newContext();
    const sent = [];
    // The real endpoint is off-origin and unreachable from here, so capture and
    // fulfil it rather than letting it fail and hide a wiring mistake.
    await ctx.route('**/rest/v1/site_events**', async route => {
      try { sent.push(JSON.parse(route.request().postData() || '{}')); } catch (e) {}
      await route.fulfill({ status: 201, body: '[]', contentType: 'application/json' });
    });
    const pg = await ctx.newPage();
    await pg.addInitScript(() => {
      try {
        localStorage.setItem('sfn_consent_v1', JSON.stringify(
          { analytics: true, ts: new Date().toISOString(), v: 1 }));
      } catch (e) {}
    });
    const errs = [];
    pg.on('pageerror', e => errs.push(e.message));
    await pg.goto('http://127.0.0.1:' + P + '/app/', { waitUntil: 'load' });
    await pg.waitForTimeout(900);

    check('no page errors on the trainer', errs.length === 0, errs[0] || '');
    check('sfnStep is defined once consent is given',
      await pg.evaluate(() => typeof window.sfnStep === 'function'));

    const kinds = sent.map(o => o.kind + (o.step ? ':' + o.step : ''));
    check('a pageview is sent', kinds.some(k => k === 'pageview'), kinds.join(', '));
    check('app_open fires on boot', kinds.includes('milestone:app_open'), kinds.join(', '));

    // Every milestone row must carry the session and nothing new beyond the step.
    const ms = sent.filter(o => o.kind === 'milestone');
    check('milestone rows carry a session id', ms.length > 0 && ms.every(o => !!o.sid));
    check('milestone rows carry a path', ms.every(o => !!o.path));
    const allowed = new Set(['kind', 'step', 'sid', 'path']);
    const stray = ms.flatMap(o => Object.keys(o)).filter(k => !allowed.has(k));
    check('milestone rows add no other fields', stray.length === 0, stray.join(', '));

    // Firing the same step twice must not produce two rows.
    const before = sent.filter(o => o.step === 'app_open').length;
    await pg.evaluate(() => { window.sfnStep('app_open'); window.sfnStep('app_open'); });
    await pg.waitForTimeout(250);
    check('a step fires once per session',
      sent.filter(o => o.step === 'app_open').length === before,
      'count stayed at ' + before);

    // The vocabulary the database constraint accepts.
    const VOCAB = ['app_open', 'first_answer', 'round_done', 'account_created', 'trial_started'];
    const used = [...new Set(sent.filter(o => o.step).map(o => o.step))];
    check('every step sent is in the accepted vocabulary',
      used.every(s => VOCAB.includes(s)), used.join(', '));
    await ctx.close();
  }

  // --- with consent refused: nothing may be sent --------------------------------
  {
    const ctx = await b.newContext();
    const sent = [];
    await ctx.route('**/rest/v1/site_events**', async route => {
      sent.push(route.request().postData());
      await route.fulfill({ status: 201, body: '[]', contentType: 'application/json' });
    });
    const pg = await ctx.newPage();
    await pg.addInitScript(() => {
      try {
        localStorage.setItem('sfn_consent_v1', JSON.stringify(
          { analytics: false, ts: new Date().toISOString(), v: 1 }));
      } catch (e) {}
    });
    const errs = [];
    pg.on('pageerror', e => errs.push(e.message));
    await pg.goto('http://127.0.0.1:' + P + '/app/', { waitUntil: 'load' });
    await pg.waitForTimeout(900);
    check('nothing is sent when analytics consent is refused', sent.length === 0,
      sent.length + ' request(s)');
    check('calling sfnStep after a refusal does not throw', errs.length === 0, errs[0] || '');
    await pg.evaluate(() => { try { window.sfnStep('first_answer'); } catch (e) { throw e; } });
    await pg.waitForTimeout(200);
    check('and still sends nothing', sent.length === 0, sent.length + ' request(s)');
    await ctx.close();
  }

  // --- item telemetry must stay unlinkable --------------------------------------
  {
    const ctx = await b.newContext();
    const items = [];
    await ctx.route('**/rest/v1/item_events**', async route => {
      try { items.push(JSON.parse(route.request().postData() || '{}')); } catch (e) {}
      await route.fulfill({ status: 201, body: '[]', contentType: 'application/json' });
    });
    await ctx.route('**/rest/v1/site_events**', r => r.fulfill({ status: 201, body: '[]' }));
    const pg = await ctx.newPage();
    await pg.addInitScript(() => {
      try {
        localStorage.setItem('sfn_consent_v1', JSON.stringify({ analytics: true, ts: '', v: 1 }));
      } catch (e) {}
    });
    await pg.goto('http://127.0.0.1:' + P + '/app/', { waitUntil: 'load' });
    await pg.waitForTimeout(600);
    const banned = ['sid', 'user_id', 'device', 'ip', 'ip_hash', 'path', 'ref', 'utm'];
    const leaked = items.flatMap(o => Object.keys(o)).filter(k => banned.includes(k));
    check('item telemetry still carries no session or device', leaked.length === 0,
      leaked.join(', ') || (items.length + ' item rows seen'));
    await ctx.close();
  }

  await b.close(); srv.close();
  console.log(fails.length ? '\nFAILURES: ' + fails.join(', ')
                           : '\nall funnel beacon checks passed');
  process.exit(fails.length ? 1 : 0);
})();
