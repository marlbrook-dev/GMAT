/* Renders the test date pages and checks what a student relies on them for.
 *
 *   - The note at the top names a date a student can still register for, on any day. The
 *     first draft pointed at the next test date, and on September 27 told a reader to
 *     register for October 3 by September 18. Each page is opened with the clock set to
 *     several days and the visible note is checked against the data file.
 *   - Every calendar file parses: CRLF lines no longer than 75 octets, one VEVENT per
 *     deadline, and each event's date equal to the date the table prints for it.
 *   - Nothing pushes the page sideways on a phone.
 *
 * Served over http so the pages load the way they do live.
 */
const { chromium } = require('playwright');
const { chromiumPath } = require('./chromium_path.js');
const http = require('http');
const fs = require('fs');
const path = require('path');
const ROOT = path.resolve(__dirname, '..');
const DATA = JSON.parse(fs.readFileSync(path.join(ROOT, 'data', 'test_dates.json'), 'utf8'));

const TYPES = { '.html': 'text/html', '.js': 'text/javascript', '.css': 'text/css', '.json': 'application/json',
                '.svg': 'image/svg+xml', '.png': 'image/png', '.ics': 'text/calendar' };
const server = http.createServer((req, res) => {
  let rel = decodeURIComponent(req.url.split('?')[0]);
  if (rel.endsWith('/')) rel += 'index.html';
  const f = path.join(ROOT, rel);
  if (!f.startsWith(ROOT) || !fs.existsSync(f) || fs.statSync(f).isDirectory()) { res.writeHead(404); return res.end('nope'); }
  res.writeHead(200, { 'Content-Type': TYPES[path.extname(f)] || 'application/octet-stream' });
  res.end(fs.readFileSync(f));
});

let failures = 0;
function ok(cond, msg) { console.log((cond ? '  ok   ' : '  FAIL ') + msg); if (!cond) failures++; }

// The rows the pages are built from, in the shape the page script uses: the last test day,
// the regular deadline and the last deadline a student can still register by.
function rows(exam) {
  if (exam === 'sat') return DATA.sat.weekend.map(r => ({ key: r.test, end: r.test, reg: r.register_by, late: r.late_by }));
  if (exam === 'act') return DATA.act.national.map(r => ({ key: r.test, end: r.test, reg: r.register_by, late: r.late_by }));
  return DATA.lsat.administrations.filter(r => r.region === 'us_canada' && !r.place).map(r => ({
    key: r.administration.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, ''),
    end: r.days[r.days.length - 1], reg: r.register_by, late: r.register_by }));
}

// What a reader on `day` should see, worked out from the data rather than the page.
function expected(exam, day) {
  const R = rows(exam);
  const ids = R.filter(r => r.late < day && day <= r.end).map(r => 'closed-' + r.key);
  const open = R.find(r => r.late >= day);
  ids.push(open ? (day <= open.reg ? 'reg-' : 'late-') + open.key : 'none');
  return ids.sort();
}

function unfold(text) { return text.replace(/\r\n[ \t]/g, ''); }

function checkIcs(name, body) {
  const lines = body.split('\r\n');
  ok(body.endsWith('\r\n') && !/[^\r]\n/.test(body), name + ': every line ends in CRLF');
  ok(lines.every(l => Buffer.byteLength(l, 'utf8') <= 75), name + ': no line is longer than 75 octets');
  const events = unfold(body).split('BEGIN:VEVENT').slice(1);
  ok(events.length >= 3, name + ': holds ' + events.length + ' events');
  for (const ev of events) {
    const start = (ev.match(/DTSTART;VALUE=DATE:(\d{8})/) || [])[1];
    const end = (ev.match(/DTEND;VALUE=DATE:(\d{8})/) || [])[1];
    if (!start || !end || end <= start || !/UID:[^\r]+@startfromnowhere\.com/.test(ev) || !/SUMMARY:/.test(ev)) {
      ok(false, name + ': an event is missing its dates, UID or summary');
      return [];
    }
  }
  return events.map(ev => (ev.match(/DTSTART;VALUE=DATE:(\d{8})/) || [])[1]);
}

(async () => {
  await new Promise(r => server.listen(0, r));
  const base = 'http://127.0.0.1:' + server.address().port;
  const browser = await chromium.launch({ executablePath: chromiumPath() });
  const days = ['2026-09-27', '2026-10-25', '2027-01-02', '2027-07-01'];
  for (const exam of ['sat', 'act', 'lsat']) {
    const url = '/exams/' + exam + '/test-dates/';
    console.log(exam.toUpperCase() + ' ' + url);
    for (const day of days) {
      const ctx = await browser.newContext({ viewport: { width: 390, height: 844 } });
      // The reader's clock, set before the page's script runs.
      await ctx.addInitScript(d => {
        const fixed = new Date(d + 'T12:00:00').getTime(), Real = Date;
        // eslint-disable-next-line no-global-assign
        Date = class extends Real { constructor(...a) { super(...(a.length ? a : [fixed])); } static now() { return fixed; } };
      }, day);
      const page = await ctx.newPage();
      await page.goto(base + url, { waitUntil: 'load' });
      const shown = await page.$$eval('p.next', ps => ps.filter(p => !p.hidden).map(p => p.id).sort());
      ok(JSON.stringify(shown) === JSON.stringify(expected(exam, day)),
        exam + ' on ' + day + ': shows ' + JSON.stringify(shown) + ', expected ' + JSON.stringify(expected(exam, day)));
      if (day === days[0]) {
        const over = await page.evaluate(() => document.documentElement.scrollWidth - window.innerWidth);
        ok(over <= 0, exam + ': no sideways scroll at 390px (' + over + 'px)');
        const links = await page.$$eval('a.cal', as => as.map(a => a.getAttribute('href')));
        ok(links.length > 0, exam + ': ' + links.length + ' calendar links');
        for (const href of links) {
          const res = await page.request.get(base + url + href);
          ok(res.status() === 200, exam + ': ' + href + ' is served');
          const starts = checkIcs(href, await res.text());
          // The test day is in the file, on the date the row prints.
          const iso = s => s.slice(0, 4) + '-' + s.slice(4, 6) + '-' + s.slice(6);
          const row = exam === 'lsat'
            ? DATA.lsat.administrations.find(r => href.endsWith(r.administration.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '') + '.ics'))
            : (exam === 'sat' ? DATA.sat.weekend : DATA.act.national).find(r => href === exam + '-' + r.test + '.ics');
          const want = row ? [exam === 'lsat' ? row.days[0] : row.test, row.register_by] : [];
          ok(row && want.every(w => starts.map(iso).includes(w)), href + ': carries the test day and registration deadline its row prints');
        }
      }
      await ctx.close();
    }
  }
  await browser.close();
  server.close();
  if (failures) { console.log('\n' + failures + ' test date check(s) failed'); process.exit(1); }
  console.log('\nall test date checks passed');
})().catch(e => { console.error(e); process.exit(1); });
