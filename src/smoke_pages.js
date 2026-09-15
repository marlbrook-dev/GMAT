// Browser validation for the standalone content pages (/international/ and /apply/): no console errors, checklist state
// survives a reload, the shortlist written by /schools/ shows up on /apply/, and CSV
// export produces a real download.
const { chromium } = require('playwright');
const path = require('path');
const ROOT = path.resolve(__dirname, '..');
const url = p => 'file://' + path.join(ROOT, p);

(async () => {
  const b = await chromium.launch({ executablePath: process.env.CHROMIUM_PATH });
  const p = await b.newPage({ viewport: { width: 1280, height: 900 } });
  const errs = [];
  p.on('pageerror', e => errs.push('pageerror: ' + e.message));
  // Google Fonts cannot be fetched through this sandbox's proxy CA, so the cert failure
  // it produces is environment noise rather than a page defect. Everything else counts.
  // Google Fonts cannot be fetched through this sandbox's proxy CA, and the analytics
  // beacon has nothing to POST to over file://. Both are environment noise.
  const noise = t => /ERR_CERT_AUTHORITY_INVALID|fonts\.(googleapis|gstatic)\.com|Failed to fetch/.test(t);
  p.on('console', m => { if (m.type() === 'error' && !noise(m.text())) errs.push('console: ' + m.text()); });

  // 1. International hub renders.
  await p.goto(url('international/index.html'));
  await p.waitForTimeout(400);
  const h1 = await p.textContent('h1');
  const rows = await p.$$eval('table.dt tbody tr', r => r.length);
  console.log('international h1:', h1.trim(), '| sourced table rows:', rows);

  // 2. Seed a shortlist the way /schools/ writes it, then load /apply/.
  await p.goto(url('apply/index.html'));
  await p.evaluate(() => localStorage.setItem('sfn_school_list_v1',
    JSON.stringify({ order: ['chicago-booth', 'berkeley-haas', 'bu-questrom'], meta: {} })));
  await p.reload();
  await p.waitForTimeout(400);
  console.log('apply h1:', (await p.textContent('h1')).trim());
  console.log('school rows from shortlist:', await p.$$eval('table.sc tbody tr', r => r.length));
  console.log('task rows visible:', await p.$$eval('.task', r => r.length));

  // 3. Deadline drives the dates.
  await p.fill('#dl', '2027-01-05');
  await p.waitForTimeout(250);
  const firstDate = await p.textContent('.phase .task .dt');
  console.log('first task target date:', firstDate.trim());

  // 4. International toggle adds the international-only tasks.
  const before = await p.$$eval('.task', r => r.length);
  await p.check('#intl');
  await p.waitForTimeout(250);
  const after = await p.$$eval('.task', r => r.length);
  console.log('tasks before/after international toggle:', before, '->', after);
  console.log('CIP column present:', (await p.$$eval('table.sc th', t => t.map(x => x.textContent))).join(' | '));

  // 5. Tick a task, reload, confirm it stuck.
  await p.click('.task input[data-task=target]');
  await p.waitForTimeout(200);
  const pct = await p.textContent('#pn');
  await p.reload();
  await p.waitForTimeout(400);
  const pct2 = await p.textContent('#pn');
  console.log('progress before/after reload:', pct.trim(), '->', pct2.trim(),
    pct.trim() === pct2.trim() ? '(persisted)' : '(LOST)');
  console.log('checkbox still checked:', await p.isChecked('.task input[data-task=target]'));

  // 6. Per-school field persists.
  await p.fill('table.sc input[data-sch=chicago-booth][data-f=cip]', '52.0201');
  await p.waitForTimeout(150);
  await p.reload(); await p.waitForTimeout(400);
  console.log('school CIP after reload:',
    await p.inputValue('table.sc input[data-sch=chicago-booth][data-f=cip]'));

  // 7. CSV export really downloads.
  const [dl] = await Promise.all([p.waitForEvent('download'), p.click('#btnCsv')]);
  const f = await dl.path();
  const csv = require('fs').readFileSync(f, 'utf8');
  console.log('csv:', dl.suggestedFilename(), csv.split('\r\n').length, 'lines; has Booth:', csv.includes('Booth'));

  // 8. Mobile width does not overflow horizontally.
  for (const pg of ['international/index.html', 'apply/index.html']) {
    const m = await b.newPage({ viewport: { width: 390, height: 844 } });
    await m.goto(url(pg)); await m.waitForTimeout(300);
    const over = await m.evaluate(() => document.documentElement.scrollWidth - document.documentElement.clientWidth);
    console.log(pg, 'horizontal overflow at 390px:', over + 'px');
    await m.close();
  }

  console.log('errors:', errs.length ? errs : 'none');
  await b.close();
  if (errs.length) process.exit(1);
})();
