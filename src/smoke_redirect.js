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
const { spawnSync } = require('child_process');

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

  // Withdrawn pages that search engines still send people to: one hop, on either host,
  // with or without the trailing slash, query string kept.
  ['https://startfromnowhere.com/exams/mcat/', 'https://startfromnowhere.com/exams/'],
  ['https://startfromnowhere.com/exams/mcat', 'https://startfromnowhere.com/exams/'],
  ['https://www.startfromnowhere.com/exams/executive-assessment/?utm_source=g',
   'https://startfromnowhere.com/exams/?utm_source=g'],

  // Everything below must be served, never redirected.
  ['https://startfromnowhere.com/', null],
  ['https://startfromnowhere.com/exams/', null],
  ['https://startfromnowhere.com/exams/mcat-prep/', null],
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
    // The inverse guard, derived rather than listed.
    //
    // This used to be a list of paths kept by hand, and that list is exactly what got it
    // wrong: it named design/ as safe to exclude while terms.html and privacy.html were
    // loading /design/styles.css, so the legal pages would have shipped with no font, no
    // colour and no background. So read what the built pages actually reference and prove
    // the deploy still serves every one of them.
    //
    // Exclusion is decided by git itself, because .assetsignore uses gitignore format and
    // reimplementing that here would be a second thing to get wrong. A path the repository
    // .gitignore already covers is generated output, which ships and is not our concern, so
    // the test is "ignored once .assetsignore is added, but not ignored without it".
    const ROOT = path.join(__dirname, '..');
    function ignoredBy(file, useAssets) {
      const args = useAssets ? ['-c', 'core.excludesFile=' + path.join(ROOT, '.assetsignore')] : [];
      const r = spawnSync('git', args.concat(['check-ignore', '--no-index', '-q', file]),
                          { cwd: ROOT, encoding: 'utf8' });
      return r.status === 0;
    }

    const pages = [];
    for (const f of ['index.html', '404.html', 'terms.html', 'privacy.html']) {
      if (fs.existsSync(path.join(ROOT, f))) pages.push(f);
    }
    if (!pages.length) {
      console.log('  skipped: no built pages on disk, run python3 src/build.py first');
    } else {
      const refs = new Set();
      for (const rel of pages) {
        const text = fs.readFileSync(path.join(ROOT, rel), 'utf8');
        let m;
        const re = /(?:href|src)="(\/[A-Za-z0-9_.\/-]+)"/g;
        while ((m = re.exec(text)) !== null) refs.add(m[1]);
      }
      // One level of CSS @import, because /design/styles.css is nothing but imports and the
      // files it pulls in are the ones that actually carry the tokens.
      for (const ref of Array.from(refs)) {
        if (!ref.endsWith('.css')) continue;
        const f = path.join(ROOT, ref.replace(/^\//, ''));
        if (!fs.existsSync(f)) continue;
        const css = fs.readFileSync(f, 'utf8');
        let m;
        const re = /@import\s+['"]([^'"]+)['"]/g;
        while ((m = re.exec(css)) !== null) {
          refs.add('/' + path.posix.normalize(path.posix.join(path.posix.dirname(ref), m[1])).replace(/^\//, ''));
        }
      }

      const dropped = [];
      for (const ref of refs) {
        const rel = ref.replace(/^\//, '');
        if (!rel || !fs.existsSync(path.join(ROOT, rel))) continue;   // generated at build time
        if (ignoredBy(rel, false)) continue;                          // build output, ships anyway
        if (ignoredBy(rel, true)) dropped.push(ref);
      }
      if (dropped.length) {
        fail('.assetsignore excludes ' + dropped.length + ' path(s) that built pages load:\n      ' +
             dropped.sort().join('\n      '));
      } else {
        ok(refs.size + ' referenced paths checked, none excluded by the deploy');
      }
    }

    // The source of the site, and the repository itself, must not be served. Workers static
    // assets does not exclude .git the way Pages did, and /.git/index alone gives out the
    // full inventory of every path the rest of this list hides.
    for (const mustGo of ['src/engine.js', 'data/DATA.md', 'CLAUDE.md', '.git/config']) {
      if (!ignoredBy(mustGo, true)) fail('.assetsignore does NOT exclude ' + mustGo);
    }
    if (!failures) ok('source, data, docs and .git are all excluded from the deploy');
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
