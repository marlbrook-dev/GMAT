// Drive the rankings page the way a reader would and check what comes back.
const { chromium } = require('playwright');
const { chromiumPath } = require('./chromium_path.js');
const http = require('http'), fs = require('fs'), p0 = require('path');
const ROOT = '/home/user/GMAT';
const T = {'.html':'text/html','.js':'text/javascript','.css':'text/css','.png':'image/png','.svg':'image/svg+xml','.json':'application/json'};
const srv = http.createServer((q, r) => {
  let rel = decodeURIComponent(q.url.split('?')[0]); if (rel.endsWith('/')) rel += 'index.html';
  const f = p0.join(ROOT, rel);
  if (!fs.existsSync(f) || fs.statSync(f).isDirectory()) { r.writeHead(404); r.end('nf'); return; }
  r.writeHead(200, {'Content-Type': T[p0.extname(f)] || 'application/octet-stream'});
  fs.createReadStream(f).pipe(r);
});
const fail = [];
function check(name, cond, detail) {
  console.log((cond ? '  ok   ' : '  FAIL ') + name + (detail ? '  ' + detail : ''));
  if (!cond) fail.push(name);
}
(async () => {
  await new Promise(r => srv.listen(0, '127.0.0.1', r)); const P = srv.address().port;
  const b = await chromium.launch({ executablePath: chromiumPath() });
  const pg = await b.newPage({ viewport: { width: 1440, height: 1000 } });
  const errs = [];
  pg.on('console', m => { if (m.type() === 'error' && !/CERT|fonts\.g/.test(m.text())) errs.push(m.text()); });
  pg.on('pageerror', e => errs.push('pageerror: ' + e.message));
  await pg.goto('http://127.0.0.1:' + P + '/colleges/', { waitUntil: 'load' });
  await pg.evaluate(() => { const c = document.getElementById('sfn-consent'); if (c) c.hidden = true; });
  await pg.waitForTimeout(400);

  const first = () => pg.evaluate(() => {
    const r = document.querySelector('#tb tr');
    return r ? r.innerText.replace(/\n/g, ' | ').slice(0, 70) : '(none)';
  });
  const count = () => pg.evaluate(() => document.getElementById('cnt').textContent);
  const rows = () => pg.evaluate(() => document.querySelectorAll('#tb tr').length);

  console.log('default tab');
  check('opens on National Universities', (await first()).includes('Massachusetts Institute'), await first());
  check('no JS errors on load', errs.length === 0, errs[0] || '');

  console.log('\ncategory tabs');
  for (const [cat, expect] of [['liberal-arts', 'Claremont'], ['masters', 'Baruch'], ['baccalaureate', 'Cooper Union']]) {
    await pg.click(`.cattabs button[data-cat="${cat}"]`);
    await pg.waitForTimeout(250);
    const f = await first();
    check(`${cat} tab leads with the right school`, f.includes(expect), f);
  }
  const blurb = await pg.evaluate(() => document.getElementById('catblurb').textContent);
  check('blurb updates with the tab', blurb.length > 20, blurb.slice(0, 50));
  check('url carries the category', (await pg.evaluate(() => location.hash)) === '#baccalaureate');

  console.log('\nfilters');
  await pg.click('.cattabs button[data-cat="national"]');
  await pg.waitForTimeout(200);
  const base = await rows();
  await pg.click('#adv'); await pg.waitForTimeout(200);
  check('More Filters opens the panel', await pg.evaluate(() => !document.getElementById('advbox').hidden));

  await pg.selectOption('#fgrad', '90'); await pg.waitForTimeout(250);
  const gradRows = await rows();
  check('graduation filter narrows the list', gradRows < base, `${base} -> ${gradRows}`);
  const allHighGrad = await pg.evaluate(() => {
    return [...document.querySelectorAll('#tb tr')].every(tr => {
      const c = tr.children[4]; if (!c) return true;
      const n = parseInt(c.textContent, 10); return isNaN(n) ? false : n >= 90;
    });
  });
  check('every surviving row really is 90% or better', allHighGrad);

  await pg.selectOption('#fadmit', '-50'); await pg.waitForTimeout(250);
  const openRows = await rows();
  check('admit-rate "over 50%" combines with it', openRows < gradRows, `${gradRows} -> ${openRows}`);

  await pg.click('#clear'); await pg.waitForTimeout(250);
  check('Clear restores the full category', (await rows()) === base, `${await rows()} vs ${base}`);
  check('count names both totals', /ranked/.test(await count()), await count());

  await pg.selectOption('#fsize', '0-2000'); await pg.waitForTimeout(250);
  check('size band filters', (await rows()) < base, await count());
  await pg.click('#clear'); await pg.waitForTimeout(200);

  await pg.fill('#q', 'berkeley'); await pg.waitForTimeout(250);
  check('search works inside a category', (await first()).toLowerCase().includes('berkeley'), await first());

  console.log('\nerrors: ' + (errs.length ? errs.join(' | ') : 'none'));
  await b.close(); srv.close();
  console.log(fail.length ? '\nFAILURES: ' + fail.join(', ') : '\nall interaction checks passed');
  process.exit(fail.length ? 1 : 0);
})();
