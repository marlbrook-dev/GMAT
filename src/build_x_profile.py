"""Render the X profile avatar and header at the sizes X expects.

Separate from build_og.py because these are not page cards: they are brand assets uploaded
by hand to a profile, at X's own dimensions (400x400 avatar shown as a circle, 1500x500
header). Same rules apply, which is the point of generating them rather than improvising:
monochrome navy wordmark, the serif display face, no invented figure.

The header keeps its bottom left corner empty on purpose. X lays the circular avatar over
that corner, so anything placed there is hidden on every profile view.

Run:  CHROMIUM_PATH=/opt/pw-browsers/chromium-*/chrome-linux/chrome \
      NODE_PATH=/opt/node22/lib/node_modules python3 src/build_x_profile.py
"""
import json
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).parent.parent
OUT = ROOT / "og"
NAVY = "#122B4E"

# The logo path is not centred inside the site's 48x48 viewBox: it is drawn against a
# rounded navy tile that supplies the balance. Lift the tile away for the avatar, where the
# navy is the background instead, and the mark sits high and right. This viewBox is
# recentred on the path's own bounds, stroke included, so the mark reads centred once X
# crops it to a circle.
LOGO = ('<svg viewBox="8 8 34 34" width="W" height="W">'
        '<path d="M13 33 22 22l6 5 8.5-10" fill="none" stroke="FG" '
        'stroke-width="3.4" stroke-linecap="round" stroke-linejoin="round"/>'
        '<path d="M29.5 16.5H37V24" fill="none" stroke="FG" stroke-width="3.4" '
        'stroke-linecap="round" stroke-linejoin="round"/></svg>')

AVATAR = """<!doctype html><meta charset="utf-8">
<style>*{margin:0;padding:0}html,body{width:400px;height:400px}
body{background:NAVY;display:flex;align-items:center;justify-content:center}
svg{display:block}</style>""" + LOGO.replace("W", "232").replace("FG", "#ffffff")

HEADER = """<!doctype html><meta charset="utf-8">
<style>
@import url('https://fonts.googleapis.com/css2?family=Source+Serif+4:opsz,wght@8..60,700&family=IBM+Plex+Sans:wght@600;700&display=swap');
*{margin:0;padding:0;box-sizing:border-box}
html,body{width:1500px;height:500px}
body{background:#fff;font-family:'IBM Plex Sans',system-ui,sans-serif;position:relative}
.wrap{position:absolute;left:0;right:0;top:74px;display:flex;flex-direction:column;
 align-items:center;text-align:center}
h1{font-family:'Source Serif 4',Georgia,serif;font-weight:700;font-size:78px;color:NAVY;
 letter-spacing:-0.5px;line-height:1}
p{font-size:31px;color:#4A5568;margin-top:22px}
.chips{display:flex;gap:13px;margin-top:30px}
.chip{border:2px solid NAVY;color:NAVY;border-radius:999px;padding:10px 26px;font-size:25px;
 font-weight:700;letter-spacing:.3px}
/* X lays the circular avatar over the bottom left corner, so that corner stays empty and
   the url sits on the right where it is never covered. */
.url{position:absolute;right:54px;bottom:46px;font-size:27px;font-weight:700;color:NAVY}
.bar{position:absolute;left:0;right:0;bottom:0;height:14px;background:NAVY}
</style>
<div class="wrap">
<h1>Start From Nowhere</h1>
<p>Free adaptive practice, and admissions research with a source on every figure</p>
<div class="chips"><span class="chip">GMAT</span><span class="chip">SAT</span>
<span class="chip">GRE</span><span class="chip">LSAT</span><span class="chip">ACT</span></div>
</div>
<div class="url">startfromnowhere.com</div>
<div class="bar"></div>
"""

SHOT_JS = """
const { chromium } = require('playwright');
const jobs = JSON.parse(process.argv[2]);
(async () => {
  const b = await chromium.launch({ executablePath: process.env.CHROMIUM_PATH });
  for (const j of jobs) {
    const p = await b.newPage({ viewport: { width: j.w, height: j.h }, deviceScaleFactor: 1 });
    await p.setContent(j.html, { waitUntil: 'load' });
    await p.evaluate(() => document.fonts.ready);
    await p.waitForTimeout(400);
    await p.screenshot({ path: j.out, type: 'png' });
    console.log('wrote ' + j.out + '  ' + j.w + 'x' + j.h);
    await p.close();
  }
  await b.close();
})();
"""


def main():
    OUT.mkdir(exist_ok=True)
    jobs = [
        {"html": AVATAR.replace("NAVY", NAVY), "w": 400, "h": 400,
         "out": str(OUT / "x-avatar.png")},
        {"html": HEADER.replace("NAVY", NAVY), "w": 1500, "h": 500,
         "out": str(OUT / "x-header.png")},
    ]
    for j in jobs:
        if "—" in j["html"] or "–" in j["html"]:
            raise SystemExit("build_x_profile: em or en dash in %s" % j["out"])
    script = ROOT / "src" / ".x_shot.js"
    script.write_text(SHOT_JS, encoding="utf-8")
    try:
        r = subprocess.run(["node", str(script), json.dumps(jobs)],
                           capture_output=True, text=True)
        sys.stdout.write(r.stdout)
        if r.returncode != 0:
            sys.stderr.write(r.stderr)
            raise SystemExit("build_x_profile: rendering failed")
    finally:
        script.unlink(missing_ok=True)


if __name__ == "__main__":
    main()
