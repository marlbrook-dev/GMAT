// The text of a web page as a person reading it sees it, for the source check (INC-0146).
//
//   node src/render_page.js URL [USER_AGENT]     prints the text to stdout
//
// check_sources.py --render calls this for sources that build their text with
// JavaScript. A plain page load misses three things, and each of them hid Stanford GSB's
// class profile, whose figures are an Infogram chart embedded from another site:
//
//   - A page that keeps sending analytics requests never goes quiet, so waiting for
//     networkidle hangs until the timeout. The wait for quiet here is capped instead.
//   - An embedded chart is a separate document in an iframe, and its text is not part of
//     the page's own innerText. Every frame a reader can see is read, the page's own
//     first; a hidden one is skipped, because its text is its raw source.
//   - An embedded chart can draw its numbers only once it is scrolled into view. The page
//     is scrolled to the bottom in steps before anything is read.
//
// src/smoke_render.js holds a local page with all three traits and fails unless the
// figure it hides comes back.
const { chromium } = require('playwright');
const { chromiumPath } = require('./chromium_path');

async function renderText(url, opts = {}) {
  const browser = await chromium.launch({ executablePath: chromiumPath() });
  let timer;
  try {
    // One deadline for the whole read, so a page that stalls ends here, with the browser
    // closed below, rather than by the caller killing this process and leaving it running.
    const deadline = new Promise((_, reject) => {
      timer = setTimeout(() => reject(new Error('no read within ' + (opts.deadlineMs || 150000) / 1000 + 's')),
                         opts.deadlineMs || 150000);
    });
    return await Promise.race([read(browser, url, opts), deadline]);
  } finally {
    clearTimeout(timer);
    await browser.close();
  }
}

async function read(browser, url, opts) {
  const page = await browser.newPage({
    userAgent: opts.userAgent || undefined,
    viewport: { width: 1280, height: 900 },
  });
  // A PDF or other file is not built by script, and a browser shows it in a viewer whose
  // text is not the document's, so it is not read here. Reading a frame that holds one
  // stalls: Wharton's career report link is an HTML page with the PDF in a frame.
  const notHtml = new Set();
  page.on('response', r => {
    try {
      const type = r.request().isNavigationRequest() ? (r.headers()['content-type'] || '') : '';
      if (type && !/html/i.test(type)) notHtml.add(r.frame());
    } catch (e) {
      // A response whose frame has gone says nothing about the frames still here.
    }
  });
  let resp;
  try {
    resp = await page.goto(url, { waitUntil: 'domcontentloaded', timeout: opts.timeout || 60000 });
  } catch (e) {
    // Chromium without a PDF viewer, as in CI, or a file sent as an attachment, turns the
    // navigation into a download and goto throws; that is the same refusal.
    if (/Download is starting/.test(String(e))) throw new Error('not an HTML page (a download)');
    throw e;
  }
  const type = (resp && resp.headers()['content-type']) || '';
  if (type && !/html/i.test(type)) throw new Error('not an HTML page (' + type.split(';')[0] + ')');
  await page.waitForLoadState('networkidle', { timeout: opts.quietMs || 10000 }).catch(() => {});
  // Most of a viewport at a time, so nothing is jumped over, until the bottom is reached
  // or the step cap is, which is what ends a page that loads more as it scrolls.
  for (let i = 0; i < (opts.maxSteps || 80); i++) {
    const atBottom = await page.evaluate(() => {
      window.scrollBy(0, Math.round(window.innerHeight * 0.8));
      const root = document.scrollingElement || document.documentElement;
      return window.scrollY + window.innerHeight >= root.scrollHeight - 2;
    });
    await page.waitForTimeout(opts.stepMs || 250);
    if (atBottom) break;
  }
  await page.waitForTimeout(opts.settleMs || 3000);
  const main = page.mainFrame();
  // Chromium shows a PDF in a viewer frame of its own, nested inside the frame that
  // received the PDF, so every frame below a non-HTML one is skipped with it.
  const insideNotHtml = f => {
    for (let x = f; x; x = x.parentFrame()) if (notHtml.has(x) || /^chrome-extension:/.test(x.url())) return true;
    return false;
  };
  const parts = [];
  for (const frame of [main, ...page.frames().filter(f => f !== main)]) {
    try {
      // A frame nobody can see is skipped, and not only because a reader never sees it:
      // innerText of a document that is not rendered falls back to its raw text, script
      // source included, which filled Wharton's read with more than 21,000 characters of
      // an Infogram chart's configuration and every number in it.
      if (insideNotHtml(frame)) continue;
      if (frame !== main) {
        const el = await frame.frameElement();
        const box = el && await el.boundingBox();
        if (!box || box.width < 2 || box.height < 2 || !(await el.isVisible())) continue;
      }
      // An image's alt text is the words the page gives for it, read out in its place to
      // anyone who cannot see it, and innerText leaves it out. Berkeley Haas and Pitt Katz
      // draw their figures as images and write the figures into the alt text (INC-0154), so
      // the alt text of every image that is shown is read after the frame's own text.
      //
      // What one click opens is part of the page too. innerText leaves out a collapsed
      // accordion panel, and Berkeley Haas's non-resident tuition and Buffalo's MBA charges
      // sit in panels like that, so a site that refused the plain read had them reported
      // missing (INC-0183). A panel the page's own controls open, named by an aria-controls
      // attribute, and a closed details element are read after the page's text, when they
      // hold a figure. Navigation, headers and footers stay out: their collapsed menus are
      // closed for another reason, and name other programs beside nothing of this one.
      const text = await within(10000, frame.evaluate(() => {
        if (!document.body) return '';
        const alts = Array.from(document.images)
          .filter(i => (i.alt || '').trim() && i.getClientRects().length && getComputedStyle(i).visibility !== 'hidden')
          .map(i => i.alt.trim());
        const chrome = 'nav, header, footer, [role="navigation"], [role="banner"], [role="contentinfo"]';
        const panels = [];
        for (const control of document.querySelectorAll('[aria-controls]')) {
          if (control.closest(chrome)) continue;
          for (const id of (control.getAttribute('aria-controls') || '').split(/\s+/)) {
            const el = id && document.getElementById(id);
            if (el && !el.getClientRects().length && !el.closest(chrome) && !panels.includes(el)) panels.push(el);
          }
        }
        for (const d of document.querySelectorAll('details:not([open])')) {
          if (!d.closest(chrome) && !panels.includes(d)) panels.push(d);
        }
        const opened = panels
          .filter(el => !panels.some(other => other !== el && other.contains(el)))
          .map(el => {
            const copy = el.cloneNode(true);
            copy.querySelectorAll('script, style, noscript, template').forEach(n => n.remove());
            return (copy.textContent || '').replace(/\s+/g, ' ').trim();
          })
          .filter(s => /\d/.test(s));
        return document.body.innerText + (alts.length ? '\n' + alts.join('\n') : '') +
          (opened.length ? '\n' + opened.join('\n') : '');
      }));
      if (text && text.trim()) parts.push(text);
    } catch (e) {
      // A frame that navigated or detached while it was being read has nothing to give.
    }
  }
  return parts.join('\n\n');
}

// A frame that never answers is given up on rather than waited for.
function within(ms, promise) {
  let timer;
  const late = new Promise((_, reject) => { timer = setTimeout(() => reject(new Error('frame did not answer')), ms); });
  return Promise.race([promise, late]).finally(() => clearTimeout(timer));
}

module.exports = { renderText };

if (require.main === module) {
  const [, , url, userAgent] = process.argv;
  if (!url) {
    console.error('usage: node src/render_page.js URL [USER_AGENT]');
    process.exit(2);
  }
  renderText(url, { userAgent })
    .then(text => process.stdout.write(text))
    .catch(e => {
      console.error(String(e).split('\n')[0]);
      process.exit(1);
    });
}
