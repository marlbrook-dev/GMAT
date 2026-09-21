// The hostname redirect, asserted as a table. Pure logic, no browser and no network, so
// it runs in the fast part of the audit.
//
//   node src/smoke_redirect.js
//
// This exists because the failure it guards against is silent. A redirect that is
// configured but never invoked still serves 200, and the only symptoms are the cookie
// dialog reappearing and the ranking signal staying split across two hostnames. The
// wrangler guard at the bottom is the important half: the redirect logic is easy and the
// routing configuration that decides whether it ever runs is the part that breaks.
const fs = require('fs');
const path = require('path');
const { pathToFileURL } = require('url');

let failures = 0;
function fail(msg) { failures++; console.log('  FAIL: ' + msg); }
function ok(msg) { console.log('  ok: ' + msg); }

// [ request url, expected redirect target, or null meaning serve it normally ]
const CASES = [
  ['https://www.startfromnowhere.com/', 'https://startfromnowhere.com/'],
  ['https://www.startfromnowhere.com/exams/gmat/', 'https://startfromnowhere.com/exams/gmat/'],
  // Deep link with a query string: the utm parameters have to survive or the redirect
  // destroys the attribution it was partly meant to protect.
  ['https://www.startfromnowhere.com/exams/gmat/?utm_source=x&b=2',
   'https://startfromnowhere.com/exams/gmat/?utm_source=x&b=2'],
  // Handed straight through to the asset router afterwards, which then does its own
  // .html redirect. Two hops, both correct.
  ['https://www.startfromnowhere.com/terms.html', 'https://startfromnowhere.com/terms.html'],
  // Scheme is upgraded, not preserved.
  ['http://www.startfromnowhere.com/app/', 'https://startfromnowhere.com/app/'],
  // Hostnames are case insensitive.
  ['https://WWW.STARTFROMNOWHERE.COM/app/', 'https://startfromnowhere.com/app/'],

  // Everything below must be served, never redirected.
  ['https://startfromnowhere.com/', null],
  ['https://startfromnowhere.com/app/bank.js', null],
  ['https://startfromnowhere.com/exams/gmat/?utm_source=x', null],
  ['https://gmat.workers.dev/', null],
  // Lookalikes. A prefix or substring test would redirect these off the site.
  ['https://wwwxstartfromnowhere.com/', null],
  ['https://www.startfromnowhere.com.evil.test/', null],
  ['https://evil.test/?next=https://www.startfromnowhere.com/', null],
  ['not a url at all', null],
];

(async () => {
  console.log('\n=== hostname redirect ===');
  const mod = await import(pathToFileURL(path.join(__dirname, 'worker.mjs')).href);

  for (const [input, expected] of CASES) {
    const got = mod.canonicalTarget(input);
    if (got !== expected) {
      fail(input + '\n        expected ' + JSON.stringify(expected) +
           '\n        got      ' + JSON.stringify(got));
    }
  }
  if (!failures) ok(CASES.length + ' redirect cases');

  // The handler itself, against a stub assets binding, so a refactor cannot quietly stop
  // calling through to the static site.
  if (typeof Response === 'undefined') {
    console.log('  skipped: handler check needs a runtime with a global Response');
  } else {
    let passedThrough = null;
    const env = { ASSETS: { fetch: (req) => { passedThrough = req; return new Response('asset'); } } };

    const red = await mod.default.fetch(new Request('https://www.startfromnowhere.com/a/b?c=1'), env);
    if (red.status !== 301) fail('handler returned ' + red.status + ', expected 301');
    else if (red.headers.get('location') !== 'https://startfromnowhere.com/a/b?c=1') {
      fail('handler Location was ' + red.headers.get('location'));
    } else if (passedThrough !== null) {
      fail('handler redirected AND called the assets binding');
    } else ok('handler returns a 301 to the apex and does not touch assets');

    passedThrough = null;
    const served = await mod.default.fetch(new Request('https://startfromnowhere.com/app/'), env);
    if (passedThrough === null) fail('apex request never reached the assets binding');
    else if ((await served.text()) !== 'asset') fail('apex request did not return the asset response');
    else ok('apex request is passed through to the assets binding');
  }

  // The routing configuration. This is the half that actually decides whether any of the
  // above runs in production.
  const cfgText = fs.readFileSync(path.join(__dirname, '..', 'wrangler.jsonc'), 'utf8');
  const cfg = JSON.parse(cfgText.replace(/^\s*\/\/.*$/gm, ''));
  const a = cfg.assets || {};
  if (cfg.main !== 'src/worker.mjs') fail('wrangler.jsonc main is ' + JSON.stringify(cfg.main) + ', expected "src/worker.mjs"');
  else if (a.binding !== 'ASSETS') fail('wrangler.jsonc assets.binding is ' + JSON.stringify(a.binding) + ', expected "ASSETS"');
  else if (a.run_worker_first !== true) {
    fail('wrangler.jsonc assets.run_worker_first is ' + JSON.stringify(a.run_worker_first) +
         ', expected true. Without it the asset router answers first and the redirect never runs.');
  } else if (a.not_found_handling !== '404-page') {
    fail('wrangler.jsonc assets.not_found_handling is ' + JSON.stringify(a.not_found_handling) + ', expected "404-page"');
  } else ok('wrangler.jsonc routes every request through the worker first');

  // The source of the site must not be served as part of the site.
  const ignorePath = path.join(__dirname, '..', '.assetsignore');
  if (!fs.existsSync(ignorePath)) {
    fail('.assetsignore is missing, so the repository root is uploaded as public assets');
  } else {
    const lines = fs.readFileSync(ignorePath, 'utf8').split('\n').map(s => s.trim());
    const need = ['src/', 'data/', 'supabase/', 'CLAUDE.md'];
    const missing = need.filter(n => !lines.includes(n));
    if (missing.length) fail('.assetsignore does not exclude ' + JSON.stringify(missing));
    else ok('.assetsignore keeps the source out of the deploy');
    // The inverse guard. These are referenced by built pages and must stay served.
    const mustServe = ['design/', 'icons/', 'og/', 'robots.txt', 'llms.txt', 'manifest.json'];
    const wrongly = mustServe.filter(n => lines.includes(n) || lines.includes(n.replace(/\/$/, '')));
    if (wrongly.length) fail('.assetsignore excludes files the site needs: ' + JSON.stringify(wrongly));
    else ok('.assetsignore still serves design, icons, og and the root text files');
  }

  // Security headers. _headers is the readable source and the worker restates them
  // because Cloudflare does not promise _headers applies once run_worker_first is on.
  // Two copies of one decision drift, so this asserts they are identical.
  const headersFile = fs.readFileSync(path.join(__dirname, '..', '_headers'), 'utf8');
  const fromFile = {};
  let inGlob = false;
  for (const raw of headersFile.split('\n')) {
    if (!raw.trim() || raw.trim().startsWith('#')) continue;
    if (!/^\s/.test(raw)) { inGlob = raw.trim() === '/*'; continue; }
    if (!inGlob) continue;
    const i = raw.indexOf(':');
    if (i > 0) fromFile[raw.slice(0, i).trim()] = raw.slice(i + 1).trim();
  }
  const fromWorker = mod.SECURITY_HEADERS;
  const names = new Set([...Object.keys(fromFile), ...Object.keys(fromWorker)]);
  const drift = [];
  for (const n of names) {
    if (fromFile[n] !== fromWorker[n]) {
      drift.push(n + '\n        _headers:  ' + JSON.stringify(fromFile[n]) +
                     '\n        worker.mjs: ' + JSON.stringify(fromWorker[n]));
    }
  }
  if (!Object.keys(fromFile).length) fail('could not parse the /* block out of _headers');
  else if (drift.length) fail('_headers and worker.mjs SECURITY_HEADERS disagree:\n      ' + drift.join('\n      '));
  else ok(Object.keys(fromFile).length + ' security headers match between _headers and the worker');

  if (typeof Response !== 'undefined') {
    const env2 = { ASSETS: { fetch: () => new Response('asset') } };
    const r1 = await mod.default.fetch(new Request('https://www.startfromnowhere.com/'), env2);
    const r2 = await mod.default.fetch(new Request('https://startfromnowhere.com/'), env2);
    const missing1 = Object.keys(fromWorker).filter(n => r1.headers.get(n) !== fromWorker[n]);
    const missing2 = Object.keys(fromWorker).filter(n => r2.headers.get(n) !== fromWorker[n]);
    if (missing1.length) fail('the 301 response is missing security headers: ' + JSON.stringify(missing1));
    else if (missing2.length) fail('the passthrough response is missing security headers: ' + JSON.stringify(missing2));
    else ok('both the redirect and the passthrough carry every security header');
  }

  console.log(failures ? '\nFAILED: ' + failures : '\npassed');
  process.exit(failures ? 1 : 0);
})();
