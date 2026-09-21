// Print the playbook to PDF with headless Chromium. Kept as a separate script from
// build_playbook.py because Chromium is a heavy dependency the Python build does not
// otherwise need, and because a missing browser should degrade the deliverable rather
// than fail the build that produces the other three formats.
//
// Run: node src/playbook_pdf.js   (after python3 src/build_playbook.py)
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');
const ROOT = path.resolve(__dirname, '..');
const SRC = path.join(ROOT, 'playbook', 'index.html');
const OUT = path.join(ROOT, 'playbook', 'BUILD_PLAYBOOK.pdf');

(async () => {
  if (!fs.existsSync(SRC)) {
    console.error('no playbook/index.html; run python3 src/build_playbook.py first');
    process.exit(1);
  }
  const exe = process.env.CHROMIUM_PATH ||
    (fs.existsSync('/opt/pw-browsers') &&
      fs.readdirSync('/opt/pw-browsers').filter(d => d.startsWith('chromium-'))
        .map(d => '/opt/pw-browsers/' + d + '/chrome-linux/chrome').find(p => fs.existsSync(p)));
  const browser = await chromium.launch({ executablePath: exe || undefined });
  const page = await browser.newPage();
  await page.goto('file://' + SRC, { waitUntil: 'load' });
  // Fonts come from the system here; the stylesheet names real fallbacks so the PDF is
  // typeset either way rather than silently falling back to a default sans.
  await page.emulateMedia({ media: 'print' });
  await page.pdf({
    path: OUT, format: 'A4', printBackground: true,
    margin: { top: '20mm', bottom: '22mm', left: '20mm', right: '20mm' },
    displayHeaderFooter: true,
    headerTemplate: '<div></div>',
    footerTemplate:
      '<div style="width:100%;font-size:8px;color:#9ca3af;padding:0 20mm;' +
      'font-family:-apple-system,Segoe UI,Roboto,sans-serif;display:flex;justify-content:space-between">' +
      '<span>The Build Playbook</span><span class="pageNumber"></span></div>',
  });
  await browser.close();
  const kb = fs.statSync(OUT).size / 1024;
  console.log('  playbook/BUILD_PLAYBOOK.pdf   %s KB', kb.toFixed(1));
})().catch(e => { console.error(String(e)); process.exit(1); });
