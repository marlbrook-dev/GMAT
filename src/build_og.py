"""Generate the Open Graph card images.

These are COMMITTED, not built on deploy, and that is deliberate: rendering them needs a
browser, and the Cloudflare builder that runs build.py has none. So this script is run by
hand when the cards change, and its output lives in /og/ under version control alongside
the icons.

Run:  CHROMIUM_PATH=/opt/pw-browsers/chromium-*/chrome-linux/chrome \
      NODE_PATH=/opt/node22/lib/node_modules python3 src/build_og.py

Brand rules apply here as everywhere: the wordmark and logo are monochrome navy, headings
use the serif display stack, and no card invents a statistic. Every number on a card is
either a count of what the site contains, which the build can verify, or absent.
"""
import json
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).parent.parent
OUT = ROOT / "og"
NAVY = "#122B4E"

# (filename, headline, supporting line). The supporting line carries no claim the site
# cannot substantiate: counts come from the build, never from an estimate.
CARDS = [
    ("default", "Start From Nowhere",
     "Free adaptive practice for the GMAT, SAT, GRE, LSAT and ACT"),
    ("trainer", "Practice That Adapts",
     "Five exams. Free. No account, and the free plan never asks for a card"),
    ("mba", "MBA Program Research",
     "{MBA} business schools, every figure with its source, year and link"),
    ("colleges", "College Research",
     "{COLLEGE} colleges ranked on published data, not on reputation surveys"),
    ("exams", "Exam Guides",
     "Structure, timing, cost and registration, each fact sourced"),
    ("blog", "Start From Nowhere",
     "Notes on preparing for the exam and the application"),
    ("pricing", "Free Forever, No Card",
     "The free plan never asks for payment details"),
    ("community", "Community Forum",
     "Ask a question without creating an account"),
    ("apply", "Application Checklist",
     "Every deadline and requirement in one place"),
    ("funding", "Paying For It",
     "Scholarships, loans and funding, with the source for every figure"),
]

CARD_HTML = """<!doctype html><meta charset="utf-8">
<style>
@import url('https://fonts.googleapis.com/css2?family=Source+Serif+4:opsz,wght@8..60,700&family=Manrope:wght@600;700&display=swap');
*{margin:0;padding:0;box-sizing:border-box}
body{width:1200px;height:630px;background:#fff;display:flex;flex-direction:column;
 justify-content:space-between;padding:68px 72px;font-family:Manrope,system-ui,sans-serif}
.top{display:flex;align-items:center;gap:14px}
.mark{font-family:'Source Serif 4',Georgia,serif;font-weight:700;font-size:30px;color:NAVY}
h1{font-family:'Source Serif 4',Georgia,serif;font-weight:700;font-size:78px;line-height:1.05;
 color:NAVY;letter-spacing:-0.5px;max-width:1040px}
p{font-size:30px;line-height:1.4;color:#4A5568;margin-top:26px;max-width:960px}
.rule{height:8px;width:132px;background:NAVY;border-radius:4px}
.foot{display:flex;justify-content:space-between;align-items:flex-end}
.url{font-size:25px;font-weight:700;color:NAVY}
</style>
<div class="top">
<svg viewBox="0 0 48 48" width="44" height="44"><rect width="48" height="48" rx="12" fill="NAVY"/>
<path d="M13 33 22 22l6 5 8.5-10" fill="none" stroke="#fff" stroke-width="3.4" stroke-linecap="round" stroke-linejoin="round"/>
<path d="M29.5 16.5H37V24" fill="none" stroke="#fff" stroke-width="3.4" stroke-linecap="round" stroke-linejoin="round"/></svg>
<span class="mark">Start From Nowhere</span></div>
<div><div class="rule"></div><h1>HEADLINE</h1><p>SUB</p></div>
<div class="foot"><span class="url">startfromnowhere.com</span></div>
"""

SHOT_JS = """
const { chromium } = require('playwright');
const cards = JSON.parse(process.argv[2]);
(async () => {
  const b = await chromium.launch({ executablePath: process.env.CHROMIUM_PATH });
  const p = await b.newPage({ viewport: { width: 1200, height: 630 },
                              deviceScaleFactor: 1 });
  for (const c of cards) {
    await p.setContent(c.html, { waitUntil: 'load' });
    // Give the webfonts a moment; a card rendered in the fallback face is off brand.
    await p.evaluate(() => document.fonts.ready);
    await p.waitForTimeout(350);
    await p.screenshot({ path: c.out, type: 'png' });
    console.log('wrote ' + c.out);
  }
  await b.close();
})();
"""


def counts():
    """Real counts from the built site, so a card can never overstate what is here."""
    def n(glob):
        return len(list(ROOT.glob(glob)))
    # No item total on any card. Two attempts at counting it produced two wrong numbers:
    # globbing "*/bank.js" caught one exam and called it five, and counting "{id:'" caught
    # the flashcards as well. The counts that ARE advertised live in llms.txt, where
    # build.py already verifies them against the real banks every build, and a second
    # weaker count here could only drift away from that one. Page and school counts stay,
    # because a directory listing cannot be wrong about how many directories there are.
    return {
        "MBA": str(n("schools/*/index.html")),
        "COLLEGE": "{:,}".format(n("colleges/*/index.html")),
    }


def main():
    if not OUT.exists():
        OUT.mkdir(parents=True)
    c = counts()
    jobs = []
    for name, head, sub in CARDS:
        html = (CARD_HTML.replace("NAVY", NAVY)
                .replace("HEADLINE", head)
                .replace("SUB", sub.format(**c)))
        if "—" in html or "–" in html:
            raise SystemExit("build_og: em or en dash in card %s" % name)
        jobs.append({"html": html, "out": str(OUT / (name + ".png"))})
    script = ROOT / "src" / ".og_shot.js"
    script.write_text(SHOT_JS, encoding="utf-8")
    try:
        r = subprocess.run(["node", str(script), json.dumps(jobs)],
                           capture_output=True, text=True)
        sys.stdout.write(r.stdout)
        if r.returncode != 0:
            sys.stderr.write(r.stderr)
            raise SystemExit("build_og: rendering failed")
    finally:
        script.unlink(missing_ok=True)
    print("counts used: %s" % c)


if __name__ == "__main__":
    main()
