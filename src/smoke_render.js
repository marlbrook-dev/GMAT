/* The source check's browser read, against a page built to hide its figure (INC-0146).
 *
 * Stanford GSB's class profile hid its average GPA from the old read in three ways at
 * once, and the fixture here has all three: the page never goes quiet on the network, the
 * figure is in an iframe, and the iframe writes it only when an IntersectionObserver sees
 * it, far below the fold. render_page.js must return the figure, and must return the
 * page's own text first. A hidden frame on the same page holds a decoy in its script,
 * which a read of every frame would pick up as text; it must not come back. A second fixture holds its figure in the page itself, so a read
 * that learned to see frames cannot have stopped seeing the page.
 *
 * Nothing leaves the machine: the server is local and the fixtures are inline.
 */
const http = require('http');
const { renderText } = require('./render_page.js');

const FIGURE = '4.17 average widget GPA';
const DECOY = '9.93 figure from a hidden frame';

// Asks the server for something every 200 ms, forever, so networkidle never arrives.
const BEACON = `<script>setInterval(function(){ fetch('/beacon?' + Date.now()).catch(function(){}); }, 200);</script>`;

const CHART = `<!doctype html><html><body><div id="c">loading</div><script>
new IntersectionObserver(function (entries, obs) {
  if (entries.some(function (e) { return e.isIntersecting; })) {
    document.getElementById('c').textContent = ${JSON.stringify(FIGURE)};
    obs.disconnect();
  }
}).observe(document.getElementById('c'));
</script></body></html>`;

const PAGES = {
  '/embedded/': `<!doctype html><html><head><title>Fixture</title></head><body>
<h1>Entering Class Profile</h1><p>The page's own introduction.</p>
<div style="height:4000px"></div>
<iframe src="/chart/" style="width:600px;height:300px;border:0"></iframe>
<div style="height:1200px"></div>
<iframe src="/hidden/" style="display:none"></iframe>${BEACON}</body></html>`,
  '/chart/': CHART,
  // A chart kept for another screen size and hidden on this one. Its document is never
  // rendered, so its innerText is its raw source, script included.
  '/hidden/': `<!doctype html><html><body><script>var config = { figure: ${JSON.stringify(DECOY)} };</script></body></html>`,
  '/plain/': `<!doctype html><html><body><h1>Plain Page</h1><p>The figure printed in the page itself is 7,531.</p>${BEACON}</body></html>`,
  // Figures drawn as images, with the figures in the alt text, as Berkeley Haas and Pitt
  // Katz publish them (INC-0154); a hidden image's alt text is not shown to anyone.
  '/images/': `<!doctype html><html><body><h1>Class Profile</h1><h3>GMAT Focus</h3>
<img src="/none.svg" width="400" height="113" alt="637 to 725 middle 80% range; 675 median">
<img src="/none.svg" style="display:none" alt="9.94 from a hidden image"></body></html>`,
  // A link that is an HTML page with the PDF in a frame, as Wharton's career report is.
  '/wrapped/': `<!doctype html><html><body><p>Report wrapper text.</p>
<iframe src="/file.pdf" style="width:800px;height:600px;border:0"></iframe></body></html>`,
};

let beacons = 0;
const server = http.createServer((req, res) => {
  const p = req.url.split('?')[0];
  if (p === '/beacon') {
    beacons++;
    // Held open for a moment, like a slow analytics endpoint.
    return setTimeout(() => { res.writeHead(204); res.end(); }, 150);
  }
  if (p === '/file.pdf' || p === '/attached.pdf') {
    // The second is sent as an attachment, which every Chromium turns into a download, as
    // CI's does with any PDF; the first opens in a viewer where Chromium has one.
    const head = { 'Content-Type': 'application/pdf' };
    if (p === '/attached.pdf') head['Content-Disposition'] = 'attachment; filename="attached.pdf"';
    res.writeHead(200, head);
    return res.end('%PDF-1.4\n%fixture\n');
  }
  if (!PAGES[p]) { res.writeHead(404); return res.end('nope'); }
  res.writeHead(200, { 'Content-Type': 'text/html' });
  res.end(PAGES[p]);
});

(async () => {
  await new Promise(r => server.listen(0, '127.0.0.1', r));
  const base = 'http://127.0.0.1:' + server.address().port;
  let fail = 0;
  const check = (name, pass, extra) => {
    if (pass) console.log('  ok   ' + name);
    else { fail++; console.log('  FAIL: ' + name + (extra ? ' -> ' + extra : '')); }
  };

  const t0 = Date.now();
  const text = await renderText(base + '/embedded/', { quietMs: 3000, settleMs: 1500 });
  const secs = (Date.now() - t0) / 1000;
  check('the figure drawn in a lazy iframe below the fold comes back', text.includes(FIGURE),
        JSON.stringify(text.slice(0, 200)));
  check('the page\'s own text comes back, ahead of the frame\'s',
        text.includes('Entering Class Profile') && text.indexOf('Entering Class Profile') < text.indexOf(FIGURE));
  check('a hidden frame\'s raw source stays out of the text', !text.includes(DECOY));
  check('a page that never goes quiet does not hang the read (' + secs.toFixed(1) + 's)', secs < 30);
  check('the fixture really did keep the network busy (' + beacons + ' beacons)', beacons >= 10);

  const plain = await renderText(base + '/plain/', { quietMs: 2000, settleMs: 500 });
  check('a figure in the page itself still comes back', plain.includes('printed in the page itself is 7,531'),
        JSON.stringify(plain.slice(0, 200)));

  const images = await renderText(base + '/images/', { quietMs: 2000, settleMs: 500 });
  check('a figure an image carries in its alt text comes back', images.includes('675 median'),
        JSON.stringify(images.slice(0, 200)));
  check('a hidden image\'s alt text stays out of the text', !images.includes('9.94'));

  // A PDF is not built by script. Shown in Chromium's viewer it stalled the read on a
  // school's PDF, so it is refused at once instead.
  const t1 = Date.now();
  const pdf = await renderText(base + '/file.pdf').then(() => 'read', e => String(e));
  check('a PDF is refused rather than read in the viewer (' + ((Date.now() - t1) / 1000).toFixed(1) + 's)',
        /not an HTML page/.test(pdf) && Date.now() - t1 < 20000, pdf);
  const attached = await renderText(base + '/attached.pdf').then(() => 'read', e => String(e));
  check('a PDF sent as a download is refused the same way', /not an HTML page/.test(attached), attached);

  // A PDF in a frame of an HTML page: the viewer never answers a read, so it is skipped.
  const t2 = Date.now();
  const wrapped = await renderText(base + '/wrapped/', { quietMs: 2000, settleMs: 500 }).catch(e => String(e));
  check('a PDF in a frame is skipped, not waited on (' + ((Date.now() - t2) / 1000).toFixed(1) + 's)',
        wrapped.includes('Report wrapper text') && Date.now() - t2 < 8000, wrapped.slice(0, 200));

  // A read that runs past its deadline ends, and says so, rather than hanging the caller.
  const late = await renderText(base + '/embedded/', { deadlineMs: 1500, settleMs: 20000 })
    .then(() => 'read', e => String(e));
  check('a read past its deadline ends with an error', /no read within/.test(late), late);

  server.close();
  if (fail) { console.log(fail + ' render check(s) failed'); process.exit(1); }
  console.log('all render checks passed');
})().catch(e => { console.log('  FAIL: ' + String(e).split('\n')[0]); server.close(); process.exit(1); });
