// iOS standalone quality, checked against the built trainers.
//
//   CHROMIUM_PATH=/opt/pw-browsers/chromium-*/chrome-linux/chrome node src/smoke_ios.js
//
// These are the properties that decide whether an installed web app reads as an app or
// as a Safari bookmark. They are all one character away from regressing and none of them
// produce an error when they do, which is why they are tested rather than remembered.
//
// The font size check is the one that matters most. iOS force zooms the entire page when
// a focused input is under 16px and does not zoom back out. A user tapping the email box
// and watching the layout lurch sideways has learned it is a website, and no amount of
// polish elsewhere undoes that.
//
// Chromium is not iOS and cannot tell us how Safari will render. What it can tell us is
// whether the declarations Safari needs are present and correct, which is the part that
// actually breaks.
const { chromium } = require('playwright');
const http = require('http'), fs = require('fs'), p0 = require('path');
const ROOT = p0.join(__dirname, '..');
const T = {'.html':'text/html','.js':'text/javascript','.css':'text/css','.png':'image/png',
           '.svg':'image/svg+xml','.json':'application/json','.webmanifest':'application/manifest+json'};
const srv = http.createServer((q, r) => {
  let rel = decodeURIComponent(q.url.split('?')[0]); if (rel.endsWith('/')) rel += 'index.html';
  const f = p0.join(ROOT, rel);
  if (!f.startsWith(ROOT) || !fs.existsSync(f) || fs.statSync(f).isDirectory()) { r.writeHead(404); r.end('nf'); return; }
  r.writeHead(200, { 'Content-Type': T[p0.extname(f)] || 'application/octet-stream' });
  fs.createReadStream(f).pipe(r);
});
const fails = [];
const check = (n, c, d) => {
  console.log((c ? '  ok: ' : '  FAIL: ') + n + (d ? '  -> ' + d : ''));
  if (!c) fails.push(n);
};

const APPS = ['app', 'sat/app', 'act/app', 'gre/app', 'lsat/app'];

(async () => {
  await new Promise(r => srv.listen(0, '127.0.0.1', r));
  const P = srv.address().port;
  const base = 'http://127.0.0.1:' + P;
  const b = await chromium.launch({ executablePath: process.env.CHROMIUM_PATH });

  // --- the manifest, once ----------------------------------------------------------
  {
    const pg = await b.newPage();
    const res = await pg.goto(base + '/manifest.json');
    check('manifest.json serves', res && res.status() === 200);
    const m = JSON.parse(await res.text());
    for (const k of ['id', 'name', 'short_name', 'start_url', 'scope', 'display',
                     'background_color', 'theme_color', 'icons']) {
      check('manifest has ' + k, m[k] !== undefined);
    }
    check('manifest display is standalone', m.display === 'standalone', m.display);
    // Android crops a non-maskable icon into a circle and clips whatever is near the edge.
    check('manifest ships a maskable icon',
      (m.icons || []).some(i => String(i.purpose || '').includes('maskable')));
    check('manifest has a 512px icon',
      (m.icons || []).some(i => i.sizes === '512x512'));
    // Every icon the manifest promises has to actually exist.
    for (const i of m.icons || []) {
      const r = await pg.goto(base + i.src).catch(() => null);
      check('icon exists: ' + i.src, r && r.status() === 200);
    }
    await pg.close();
  }

  // --- per trainer -------------------------------------------------------------------
  for (const app of APPS) {
    const pg = await b.newPage({ viewport: { width: 390, height: 844 } });
    await pg.goto(base + '/' + app + '/', { waitUntil: 'domcontentloaded' });
    await pg.waitForTimeout(200);

    const head = await pg.evaluate(() => {
      const meta = n => { const e = document.querySelector('meta[name="' + n + '"]'); return e ? e.content : null; };
      return {
        viewport: meta('viewport'),
        capable: meta('apple-mobile-web-app-capable'),
        statusBar: meta('apple-mobile-web-app-status-bar-style'),
        appTitle: meta('apple-mobile-web-app-title'),
        themeColor: meta('theme-color'),
        manifest: !!document.querySelector('link[rel="manifest"]'),
        appleIcon: !!document.querySelector('link[rel="apple-touch-icon"]'),
      };
    });

    check('[' + app + '] viewport-fit=cover', /viewport-fit\s*=\s*cover/.test(head.viewport || ''), head.viewport);
    // user-scalable=no is an accessibility failure and Safari ignores it anyway.
    check('[' + app + '] zoom is not disabled',
      !/user-scalable\s*=\s*no|maximum-scale\s*=\s*1/.test(head.viewport || ''), head.viewport);
    check('[' + app + '] apple-mobile-web-app-capable', head.capable === 'yes', String(head.capable));
    check('[' + app + '] status bar style set', !!head.statusBar, String(head.statusBar));
    check('[' + app + '] app title set', !!head.appTitle, String(head.appTitle));
    check('[' + app + '] links a manifest', head.manifest);
    check('[' + app + '] has an apple-touch-icon', head.appleIcon);
    check('[' + app + '] theme-color set', !!head.themeColor, String(head.themeColor));

    // The zoom trigger. Every focusable text control, as rendered.
    const small = await pg.evaluate(() => {
      const out = [];
      document.querySelectorAll('input,select,textarea').forEach(el => {
        const t = (el.getAttribute('type') || 'text').toLowerCase();
        if (['checkbox', 'radio', 'range', 'submit', 'button', 'hidden', 'file', 'color'].includes(t)) return;
        const px = parseFloat(getComputedStyle(el).fontSize);
        if (px < 16) out.push((el.id || el.name || el.tagName.toLowerCase()) + ' ' + px + 'px');
      });
      return out;
    });
    check('[' + app + '] no text input under 16px', small.length === 0, small.slice(0, 4).join(', '));

    const css = await pg.evaluate(() => {
      const h = getComputedStyle(document.documentElement);
      const btn = document.querySelector('button, .btn, a');
      const bs = btn ? getComputedStyle(btn) : null;
      return {
        overscroll: h.overscrollBehaviorY,
        padTop: h.paddingTop,
        adjust: h.webkitTextSizeAdjust || h.textSizeAdjust,
        tap: bs ? (bs.webkitTapHighlightColor || '') : '',
        select: bs ? (bs.webkitUserSelect || bs.userSelect) : '',
      };
    });
    check('[' + app + '] overscroll chaining off', css.overscroll === 'none', css.overscroll);
    // env() resolves to 0px off-device, so this proves the declaration is present and
    // parsed rather than that it has a value here.
    check('[' + app + '] safe area padding declared', css.padTop !== '' && css.padTop !== undefined, css.padTop);
    check('[' + app + '] tap highlight cleared on controls',
      /rgba\(0,\s*0,\s*0,\s*0\)|transparent/.test(css.tap), css.tap);
    check('[' + app + '] controls are not text selectable', css.select === 'none', css.select);

    await pg.close();
  }

  await b.close(); srv.close();
  console.log(fails.length ? '\nFAILURES: ' + fails.join(', ') : '\nall iOS standalone checks passed');
  process.exit(fails.length ? 1 : 0);
})();
