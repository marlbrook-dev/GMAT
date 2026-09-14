import pathlib, subprocess, sys, tempfile, os
d = pathlib.Path(__file__).parent; root = d.parent
sys.path.insert(0, str(d))
import partials
# One app per exam. Each entry names the source files that make up that exam's bank,
# the concat expression the template uses to build BANK, and the trademark line for its footer.
GMAT_BANKS = ["bank_quant.js","bank_quant2.js","bank_quant3.js","bank_quant4.js","bank_quant5.js","bank_quant6.js",
              "bank_verbal.js","bank_verbal2.js","bank_verbal3.js","bank_verbal4.js","bank_verbal5.js","bank_verbal6.js","bank_verbal7.js","bank_verbal8.js",
              "bank_di.js","bank_di2.js","bank_di3.js","bank_di4.js","bank_di5.js","bank_di6.js","bank_di7.js","bank_di8.js",
              "cards.js","cards2.js","cards3.js","playbook_gmat.js"]
SAT_BANKS = ["bank_sat_rw.js","bank_sat_rw2.js","bank_sat_math.js","bank_sat_math2.js","cards_sat.js","playbook_sat.js"]

APPS = [
    {"exam": "gmat-focus", "out": "app", "files": GMAT_BANKS,
     "concat": ("BANK_QUANT, BANK_QUANT2, BANK_QUANT3, BANK_QUANT4, BANK_QUANT5, BANK_QUANT6, "
                "BANK_VERBAL, BANK_VERBAL2, BANK_VERBAL3, BANK_VERBAL4, BANK_VERBAL5, BANK_VERBAL6, BANK_VERBAL7, BANK_VERBAL8, "
                "BANK_DI, BANK_DI2, BANK_DI3, BANK_DI4, BANK_DI5, BANK_DI6, BANK_DI7, BANK_DI8"),
     "footer": ("GMAT is a registered trademark of the Graduate Management Admission Council (GMAC), which does not "
                "endorse this product. Practice items are original and written for Start From Nowhere. Score bands "
                "shown here are internal estimates, not official GMAT scores."),
     "is_404": True},
    {"exam": "sat", "out": "sat/app", "files": SAT_BANKS,
     "concat": "BANK_SAT_RW, BANK_SAT_RW2, BANK_SAT_MATH, BANK_SAT_MATH2",
     "footer": ("SAT is a trademark registered by the College Board, which does not endorse this product. Practice "
                "items are original and written for Start From Nowhere. Content domains follow College Board's "
                "published framework; nothing here reports an official 400 to 1600 score."),
     "is_404": False},
]

engine = (d/"engine.js").read_text(); tpl = (d/"app_template.html").read_text()
built = {}
for app in APPS:
    banks = "\n".join((d/f).read_text() for f in app["files"])
    out = (tpl.replace("{{EXAM_ID}}", app["exam"])
              .replace("{{BANKS}}", banks)
              .replace("{{ENGINE}}", engine)
              .replace("{{BANK_CONCAT}}", app["concat"])
              .replace("{{FOOTER_NOTE}}", app["footer"]))
    if "{{" in out:
        import re as _r
        print("ERROR: unresolved placeholder in " + app["out"] + ": " + str(_r.findall(r"\{\{[A-Z_]+\}\}", out)[:4]), file=sys.stderr)
        sys.exit(1)
    target = root
    for part in app["out"].split("/"):
        target = target/part
        target.mkdir(exist_ok=True)
    (target/"index.html").write_text(out)
    if app["is_404"]:
        (root/"404.html").write_text(out)
    built[app["exam"]] = (app["out"], out, banks)

import re as _re
gmat_banks_src = built["gmat-focus"][2]
sat_banks_src = built["sat"][2]
bank_count = len(_re.findall(r"\{\s*id: ?'[QVD]", gmat_banks_src))
card_count = len(_re.findall(r"\{\s*id: ?'c\d", gmat_banks_src))
sat_bank_count = len(_re.findall(r"\{\s*id: ?'S[RM]\d", sat_banks_src))
sat_card_count = len(_re.findall(r"\{\s*id: ?'s\d", sat_banks_src))
total_bank_count = bank_count + sat_bank_count
# Tracked skills come from the engine registry itself, so the landing page can never
# drift from the number of ratings the apps actually keep.
_skill_probe = subprocess.run(
    ["node", "-e",
     "const fs=require('fs');const s=fs.readFileSync(process.argv[1],'utf8');"
     "console.log(eval(s+'; GMAT_SKILLS.length + SAT_SKILLS.length'))",
     str(d/"engine.js")],
    capture_output=True, text=True)
if _skill_probe.returncode != 0:
    print("ERROR: could not count tracked skills from engine.js\n" + _skill_probe.stderr.strip(), file=sys.stderr); sys.exit(1)
total_skills = _skill_probe.stdout.strip()

def no_dashes(name, text):
    if "\u2014" in text or "\u2013" in text:
        print(f"ERROR: em/en dash in {name}", file=sys.stderr); sys.exit(1)

# House rule: no em or en dashes anywhere, docs and sources included. The page checks below
# cover generated output; this covers the files people hand-edit.
for _doc in ["README.md", "ROADMAP.md", "CLAUDE.md", "llms.txt", "GROWTH.md", "INTEGRATIONS.md", "data/DATA.md"]:
    _p = root / _doc
    if _p.exists():
        no_dashes(_doc, _p.read_text())
for _src in sorted(d.glob("bank_*.js")) + sorted(d.glob("cards*.js")) + sorted(d.glob("playbook_*.js")) + [d/"engine.js"]:
    no_dashes(_src.name, _src.read_text())

landing = ((d/"landing.html").read_text().replace("{{BANK_COUNT}}", str(bank_count)).replace("{{CARD_COUNT}}", str(card_count))
           .replace("{{SAT_BANK_COUNT}}", str(sat_bank_count)).replace("{{SAT_CARD_COUNT}}", str(sat_card_count))
           .replace("{{TOTAL_BANK_COUNT}}", str(total_bank_count)).replace("{{TOTAL_SKILLS}}", total_skills))
landing = partials.apply_chrome(landing)
if "{{" in landing:
    print("ERROR: unresolved placeholder in landing.html", file=sys.stderr); sys.exit(1)
no_dashes("landing.html", landing)
(root/"index.html").write_text(landing)

def check_scripts(path):
    # a single unescaped quote in generated JS once took down the whole app;
    # parse every inline script with node before letting a build succeed
    import re
    html = pathlib.Path(path).read_text()
    for i, m in enumerate(re.finditer(r"<script>([\s\S]*?)</script>", html)):
        with tempfile.NamedTemporaryFile("w", suffix=".js", delete=False) as f:
            f.write(m.group(1))
            tmp = f.name
        r = subprocess.run(["node", "--check", tmp], capture_output=True, text=True)
        os.unlink(tmp)
        if r.returncode != 0:
            print(f"SYNTAX ERROR in inline script {i} of {path}:\n{r.stderr.strip()}", file=sys.stderr)
            sys.exit(1)

community = partials.apply_chrome((d/"community.html").read_text())
no_dashes("community.html", community)
(root/"community").mkdir(exist_ok=True); (root/"community"/"index.html").write_text(community)

for name in ["terms.html", "privacy.html"]:
    page = partials.apply_chrome((d/name).read_text())
    no_dashes(name, page)
    if "{{" in page:
        print(f"ERROR: unresolved placeholder in {name}", file=sys.stderr); sys.exit(1)
    (root/name).write_text(page)

for p in [root/"app"/"index.html", root/"sat"/"app"/"index.html", root/"index.html", root/"community"/"index.html", root/"terms.html", root/"privacy.html"]:
    check_scripts(p)
print("built app/index.html (%d bytes, %d items) and sat/app/index.html (%d bytes, %d items); landing, community/, terms, privacy built; inline scripts parse"
      % (len(built["gmat-focus"][1]), bank_count, len(built["sat"][1]), sat_bank_count))

import subprocess as _sp
_sp.run([sys.executable, str(d/"build_rankings.py")], check=True)
_sp.run([sys.executable, str(d/"build_exams.py")], check=True)
