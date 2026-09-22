// Pre-launch audit, run against the built site.
//
//   node src/smoke_launch.js   (the browser is resolved by src/chromium_path.js)
//
// The checks here are the ones that are cheap to automate and expensive to discover
// after launch: contrast that fails WCAG, links that 404, headings that skip a level,
// tap targets too small for a thumb, meta that Google will truncate or rewrite.
//
// Deliberately NOT here, because automating them badly is worse than not automating
// them: whether the copy is any good, whether a CTA is the right CTA, whether the
// design works. Those need eyes.
//
// Contrast is computed from the real composited colours, walking up for the effective
// background, because a rule that reads "color: #6B7280" tells you nothing until you
// know what is behind it.
const { chromium } = require('playwright');
const { chromiumPath } = require('./chromium_path.js');
const http = require('http'), fs = require('fs'), p0 = require('path'), zlib = require('zlib');
const ROOT = p0.join(__dirname, '..');
const T = {'.html':'text/html','.js':'text/javascript','.css':'text/css','.png':'image/png',
           '.svg':'image/svg+xml','.json':'application/json','.webmanifest':'application/manifest+json',
           '.txt':'text/plain','.xml':'application/xml','.ico':'image/x-icon'};
const srv = http.createServer((q, r) => {
  let rel = decodeURIComponent(q.url.split('?')[0]); if (rel.endsWith('/')) rel += 'index.html';
  const f = p0.join(ROOT, rel);
  if (!f.startsWith(ROOT) || !fs.existsSync(f) || fs.statSync(f).isDirectory()) { r.writeHead(404); r.end('nf'); return; }
  const type = T[p0.extname(f)] || 'application/octet-stream';
  const body = fs.readFileSync(f);
  if (/html|javascript|css|json|text|xml/.test(type)) {
    const gz = zlib.gzipSync(body, { level: 6 });
    r.writeHead(200, { 'Content-Type': type, 'Content-Encoding': 'gzip', 'Content-Length': gz.length });
    r.end(gz);
  } else { r.writeHead(200, { 'Content-Type': type, 'Content-Length': body.length }); r.end(body); }
});

// Content pages. The trainers are excluded from the link and heading sweeps because they
// are a single-page app whose body is built at runtime; they have their own suites.
const PAGES = ['/', '/privacy.html', '/terms.html', '/do-not-sell/', '/colleges/', '/schools/',
               '/exams/', '/pricing/', '/blog/', '/community/', '/apply/', '/funding/',
               '/international/', '/scoring/', '/colleges/methodology/'];

const noise = t => /ERR_CERT_AUTHORITY_INVALID|fonts\.(googleapis|gstatic)\.com|Failed to fetch|net::ERR/.test(t);
const fails = [], warns = [];
function check(name, cond, detail) {
  console.log((cond ? '  ok: ' : '  FAIL: ') + name + (detail ? '  -> ' + detail : ''));
  if (!cond) fails.push(name);
}
function warn(name, cond, detail) {
  if (!cond) { console.log('  warn: ' + name + (detail ? '  -> ' + detail : '')); warns.push(name); }
}

// WCAG relative luminance and contrast ratio.
const AUDIT = `(() => {
  function lum(c){
    const s = c.map(v => { v /= 255; return v <= 0.03928 ? v/12.92 : Math.pow((v+0.055)/1.055, 2.4); });
    return 0.2126*s[0] + 0.7152*s[1] + 0.0722*s[2];
  }
  function parse(c){
    const m = String(c).match(/rgba?\\(([^)]+)\\)/); if(!m) return null;
    const p = m[1].split(',').map(x => parseFloat(x));
    return { rgb: [p[0],p[1],p[2]], a: p.length > 3 ? p[3] : 1 };
  }
  // Walk up for the first opaque background, then composite anything translucent over it.
  function bgOf(el){
    let n = el, stack = [];
    while (n && n !== document.documentElement) {
      const c = parse(getComputedStyle(n).backgroundColor);
      if (c && c.a === 1) { stack.push(c); break; }
      if (c && c.a > 0) stack.push(c);
      n = n.parentElement;
    }
    let base = [255,255,255];
    for (let i = stack.length - 1; i >= 0; i--) {
      const c = stack[i];
      base = base.map((b, k) => Math.round(c.rgb[k]*c.a + b*(1-c.a)));
    }
    return base;
  }
  const out = { contrast: [], small: [], headings: [], links: [] };
  const seen = new Set();
  document.querySelectorAll('p,li,td,th,span,a,button,h1,h2,h3,h4,label,div').forEach(el => {
    if (!el.offsetParent && getComputedStyle(el).position !== 'fixed') return;
    // Only elements holding their own text.
    const own = [...el.childNodes].filter(n => n.nodeType === 3 && n.textContent.trim().length > 1);
    if (!own.length) return;
    const st = getComputedStyle(el);
    const fg = parse(st.color); if (!fg) return;
    const bg = bgOf(el);
    const fgc = fg.a === 1 ? fg.rgb : fg.rgb.map((v,k) => Math.round(v*fg.a + bg[k]*(1-fg.a)));
    const L1 = lum(fgc), L2 = lum(bg);
    const ratio = (Math.max(L1,L2) + 0.05) / (Math.min(L1,L2) + 0.05);
    const px = parseFloat(st.fontSize), wt = parseInt(st.fontWeight) || 400;
    const large = px >= 24 || (px >= 18.66 && wt >= 700);
    const need = large ? 3 : 4.5;
    if (ratio < need) {
      const key = st.color + '|' + bg.join(',') + '|' + Math.round(px);
      if (!seen.has(key)) {
        seen.add(key);
        out.contrast.push({ ratio: +ratio.toFixed(2), need, px: Math.round(px), color: st.color,
                            bg: 'rgb(' + bg.join(',') + ')',
                            text: el.textContent.trim().slice(0, 45) });
      }
    }
  });
  // Tap targets: anything clickable smaller than 24px in either axis on a phone.
  document.querySelectorAll('a,button,input,select,[onclick]').forEach(el => {
    if (!el.offsetParent) return;
    const r = el.getBoundingClientRect();
    if (r.width === 0 || r.height === 0) return;
    if (r.height < 24 || r.width < 24) {
      out.small.push({ tag: el.tagName.toLowerCase(),
                       size: Math.round(r.width) + 'x' + Math.round(r.height),
                       text: (el.textContent || el.value || '').trim().slice(0, 30) });
    }
  });
  // Heading order: exactly one h1, and no level skipped on the way down.
  const hs = [...document.querySelectorAll('h1,h2,h3,h4,h5,h6')].map(h => +h.tagName[1]);
  out.headings = { h1: hs.filter(x => x === 1).length, order: hs };
  out.links = [...document.querySelectorAll('a[href]')].map(a => a.getAttribute('href'));
  out.lang = document.documentElement.getAttribute('lang');
  out.title = (document.title || '').trim();
  const d = document.querySelector('meta[name="description"]');
  out.desc = d ? (d.getAttribute('content') || '').trim() : '';
  return out;
})()`;

(async () => {
  await new Promise(r => srv.listen(0, '127.0.0.1', r));
  const P = srv.address().port;
  const base = 'http://127.0.0.1:' + P;
  const b = await chromium.launch({ executablePath: chromiumPath() });
  const linkTargets = new Map();

  for (const path of PAGES) {
    console.log('\n' + path);
    const pg = await b.newPage({ viewport: { width: 390, height: 844 } });
    const errs = [];
    pg.on('pageerror', e => { if (!noise(e.message)) errs.push(e.message); });
    pg.on('console', m => { if (m.type() === 'error' && !noise(m.text())) errs.push(m.text()); });
    const res = await pg.goto(base + path, { waitUntil: 'domcontentloaded' });
    if (!res || res.status() >= 400) { check(path + ' loads', false, 'status ' + (res && res.status())); await pg.close(); continue; }
    await pg.waitForTimeout(250);
    const a = await pg.evaluate(AUDIT);

    check(path + ' no console errors', errs.length === 0, errs[0] || '');
    check(path + ' has lang', a.lang === 'en', String(a.lang));
    check(path + ' exactly one h1', a.headings.h1 === 1, 'found ' + a.headings.h1);

    // No skipped heading levels.
    let skipped = null, prev = 0;
    for (const lv of a.headings.order) { if (prev && lv > prev + 1) { skipped = prev + ' -> ' + lv; break; } prev = lv; }
    check(path + ' no skipped heading level', !skipped, skipped || '');

    // Google truncates around 60 and 160; these are warnings, not failures.
    warn(path + ' title length 15 to 65', a.title.length >= 15 && a.title.length <= 65, a.title.length + ' chars');
    warn(path + ' description 50 to 165', a.desc.length >= 50 && a.desc.length <= 165, a.desc.length + ' chars');

    check(path + ' contrast meets WCAG AA', a.contrast.length === 0,
      a.contrast.slice(0, 3).map(c => c.ratio + ':1 (needs ' + c.need + ') ' + c.px + 'px '
        + c.color + ' on ' + c.bg + ' "' + c.text + '"').join(' | '));

    warn(path + ' tap targets at least 24px', a.small.length === 0,
      a.small.slice(0, 3).map(s => s.tag + ' ' + s.size + ' "' + s.text + '"').join(' | '));

    // Collect internal links for the sweep below. Resolved against the page URL rather
    // than concatenated onto the origin: "app/" on "/" means "/app/", and string
    // concatenation onto an origin with no trailing slash turns it into nonsense and
    // then reports a working link as broken.
    for (const h of a.links) {
      if (!h || /^(#|mailto:|tel:)/.test(h)) continue;
      let u;
      try { u = new URL(h, base + path); } catch (e) { continue; }
      if (u.origin !== base) continue;          // external, not ours to check
      linkTargets.set(u.pathname, path);
    }
    await pg.close();
  }

  // Every internal link resolves.
  console.log('\ninternal links');
  const pg = await b.newPage();
  const broken = [];
  for (const [href, from] of linkTargets) {
    if (!href) continue;
    const r = await pg.goto(base + href, { waitUntil: 'commit' }).catch(() => null);  // href is an absolute path now
    if (!r || r.status() >= 400) broken.push(href + ' (linked from ' + from + ')');
  }
  check('all ' + linkTargets.size + ' internal link targets resolve', broken.length === 0,
    broken.slice(0, 5).join(' | '));
  await pg.close();

  await b.close(); srv.close();
  if (warns.length) console.log('\n' + warns.length + ' warning(s), not blocking');
  console.log(fails.length ? '\nFAILURES: ' + fails.join(', ') : '\nall launch checks passed');
  process.exit(fails.length ? 1 : 0);
})();
