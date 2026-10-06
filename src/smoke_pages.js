// Browser validation for the standalone content pages (/international/, /apply/ and the
// deadlines hub): no console errors, checklist state
// survives a reload, the shortlist written by /schools/ shows up on /apply/, and CSV
// export produces a real download.
//
// Served over http, as the pages are live. It used to open them as file:// URLs, where a
// root-relative path such as /vendor/fonts-2026-09-27/fonts.css names the root of the disk
// rather than the site, so it could not load the site's own stylesheet once the fonts moved
// onto it (INC-0166).
const { chromium } = require('playwright');
const { chromiumPath } = require('./chromium_path.js');
const http = require('http');
const fs = require('fs');
const path = require('path');
const ROOT = path.resolve(__dirname, '..');
const TYPES = { '.html': 'text/html', '.js': 'text/javascript', '.css': 'text/css',
                '.json': 'application/json', '.svg': 'image/svg+xml', '.png': 'image/png',
                '.woff2': 'font/woff2', '.webmanifest': 'application/manifest+json' };
const server = http.createServer((req, res) => {
  let rel = decodeURIComponent(req.url.split('?')[0]);
  if (rel.endsWith('/')) rel += 'index.html';
  const file = path.join(ROOT, rel);
  if (!file.startsWith(ROOT) || !fs.existsSync(file) || fs.statSync(file).isDirectory()) {
    res.writeHead(404); res.end('not found'); return;
  }
  res.writeHead(200, { 'Content-Type': TYPES[path.extname(file)] || 'application/octet-stream' });
  fs.createReadStream(file).pipe(res);
});
let PORT = 0;
const url = p => 'http://127.0.0.1:' + PORT + '/' + p;

(async () => {
  await new Promise(r => server.listen(0, r));
  PORT = server.address().port;
  const b = await chromium.launch({ executablePath: chromiumPath() });
  const p = await b.newPage({ viewport: { width: 1280, height: 900 } });
  // A consent choice already made, the way a returning visitor arrives. Without it the
  // consent dialog, which is modal, sits over the checklist and intercepts every click, so
  // this suite had been timing out on its first checkbox since the dialog shipped.
  await p.addInitScript(() => {
    try { localStorage.setItem('sfn_consent_v1', JSON.stringify({ analytics: false, ts: '', v: 1 })); } catch (e) {}
  });
  const errs = [];
  p.on('pageerror', e => errs.push('pageerror: ' + e.message));
  // Every console error counts. Supabase is answered locally, since a test run must not
  // call it, and a resource that fails to load is a page defect now that the site's own
  // paths resolve: this used to excuse Google Fonts' failures here, and that excuse is how
  // the file:// loads went unnoticed (INC-0166).
  await p.route('**/rest/v1/**', r => r.fulfill({ status: 200, contentType: 'application/json', body: '[]' }));
  p.on('requestfailed', r => errs.push('failed: ' + r.url()));
  p.on('response', r => { if (r.status() >= 400) errs.push(r.status() + ': ' + r.url()); });
  p.on('console', m => { if (m.type() === 'error') errs.push('console: ' + m.text()); });

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

  // 7b. The calendar export is a calendar file a phone will open: one event for each open
  // task and for each school deadline entered, CRLF line ends, and no line over 75 octets.
  await p.fill('table.sc input[data-sch=berkeley-haas][data-f=deadline]', '2027-01-07');
  await p.waitForTimeout(150);
  const [icsDl] = await Promise.all([p.waitForEvent('download'), p.click('#btnIcs')]);
  const cal = fs.readFileSync(await icsDl.path(), 'utf8');
  const open = await p.$$eval('.task input[data-task]', xs => xs.filter(x => !x.checked).length);
  const events = (cal.match(/^BEGIN:VEVENT$/gm) || []).length;
  const longest = Math.max(...cal.split('\r\n').map(l => Buffer.byteLength(l, 'utf8')));
  console.log('ics:', icsDl.suggestedFilename(), events, 'events for', open,
    'open tasks and 1 school deadline; longest line', longest, 'octets');
  if (!cal.startsWith('BEGIN:VCALENDAR\r\n') || !cal.endsWith('END:VCALENDAR\r\n')) errs.push('ics: not a calendar file');
  if (cal.replace(/\r\n/g, '').includes('\n')) errs.push('ics: a line ends without CRLF');
  if (events !== open + 1) errs.push('ics: ' + events + ' events, expected ' + (open + 1));
  if (longest > 75) errs.push('ics: a line of ' + longest + ' octets');
  if (!/SUMMARY:Application Deadline: [^\r\n]*\r\nDESCRIPTION:/.test(cal.replace(/\r\n /g, '')))
    errs.push('ics: no event for the school deadline entered');
  if (!cal.includes('DTSTART;VALUE=DATE:20270107')) errs.push('ics: the school deadline is not on its date');

  // 7c. The deadlines hub, read on a date after the build's: every round in the records is a
  // row, the rounds already passed are hidden until asked for, and the next deadline note is
  // chosen again for the reader's date from the rows, naming every round due that day.
  const recs = fs.readdirSync(path.join(ROOT, 'data', 'schools')).filter(f => f.endsWith('.json'))
    .map(f => JSON.parse(fs.readFileSync(path.join(ROOT, 'data', 'schools', f), 'utf8')))
    .filter(s => s.deadlines && !s.discontinued);
  const rounds = recs.flatMap(s => s.deadlines.rounds.map(r => ({ when: r.deadline, name: s.name })));
  const READER = '2027-01-06';
  const h = await b.newPage({ viewport: { width: 1280, height: 900 } });
  await h.addInitScript(() => {
    try { localStorage.setItem('sfn_consent_v1', JSON.stringify({ analytics: false, ts: '', v: 1 })); } catch (e) {}
  });
  await h.addInitScript(t => {
    const T = new Date(t + 'T12:00:00').getTime(), D = Date;
    class F extends D { constructor(...a) { super(...(a.length ? a : [T])); } static now() { return T; } }
    globalThis.Date = F;
  }, READER);
  h.on('pageerror', e => errs.push('hub pageerror: ' + e.message));
  await h.route('**/rest/v1/**', r => r.fulfill({ status: 200, contentType: 'application/json', body: '[]' }));
  await h.goto(url('schools/deadlines/index.html'));
  await h.waitForTimeout(300);
  const hub = await h.evaluate(() => ({
    rows: document.querySelectorAll('table.rounds tbody tr').length,
    shown: [...document.querySelectorAll('table.rounds tbody tr')].filter(t => t.offsetParent).length,
    next: document.getElementById('next').hidden ? '' : document.getElementById('next').textContent,
    btn: document.getElementById('btnPast').textContent }));
  const passedN = rounds.filter(r => r.when < READER).length;
  const dueNow = rounds.filter(r => r.when === READER);
  console.log('deadlines hub:', hub.rows, 'rows for', rounds.length, 'rounds;', hub.shown, 'shown on', READER,
    '|', hub.next.slice(0, 60), '|', hub.btn);
  if (hub.rows !== rounds.length) errs.push('hub: ' + hub.rows + ' rows for ' + rounds.length + ' rounds');
  if (hub.shown !== rounds.length - passedN) errs.push('hub: ' + hub.shown + ' rows shown, expected ' + (rounds.length - passedN));
  if (!dueNow.length || !hub.next.startsWith('Next deadline: January 6, 2027.')) errs.push('hub: next note reads ' + JSON.stringify(hub.next));
  for (const r of dueNow) if (!hub.next.includes(r.name)) errs.push('hub: next note leaves out ' + r.name);
  if (hub.btn !== 'Show Passed Rounds (' + passedN + ')') errs.push('hub: button reads ' + JSON.stringify(hub.btn));
  await h.click('#btnPast');
  const all = await h.$$eval('table.rounds tbody tr', ts => ts.filter(t => t.offsetParent).length);
  if (all !== rounds.length) errs.push('hub: ' + all + ' rows shown after Show Passed Rounds');
  await h.close();

  // 8. Mobile width does not overflow horizontally.
  for (const pg of ['international/index.html', 'apply/index.html', 'schools/deadlines/index.html']) {
    const m = await b.newPage({ viewport: { width: 390, height: 844 } });
    await m.goto(url(pg)); await m.waitForTimeout(300);
    const over = await m.evaluate(() => document.documentElement.scrollWidth - document.documentElement.clientWidth);
    console.log(pg, 'horizontal overflow at 390px:', over + 'px');
    await m.close();
  }

  console.log('errors:', errs.length ? errs : 'none');
  await b.close();
  server.close();
  if (errs.length) process.exit(1);
})();
