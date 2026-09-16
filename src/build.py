import pathlib, subprocess, sys, tempfile, os, datetime
d = pathlib.Path(__file__).parent; root = d.parent
sys.path.insert(0, str(d))
import partials
# One app per exam. Each entry names the source files that make up that exam's bank,
# the concat expression the template uses to build BANK, and the trademark line for its footer.
GMAT_BANKS = ["bank_quant.js","bank_quant2.js","bank_quant3.js","bank_quant4.js","bank_quant5.js","bank_quant6.js",
              "bank_verbal.js","bank_verbal2.js","bank_verbal3.js","bank_verbal4.js","bank_verbal5.js","bank_verbal6.js","bank_verbal7.js","bank_verbal8.js",
              "bank_di.js","bank_di2.js","bank_di3.js","bank_di4.js","bank_di5.js","bank_di6.js","bank_di7.js","bank_di8.js","bank_di9.js",
              "cards.js","cards2.js","cards3.js","playbook_gmat.js"]
SAT_BANKS = ["bank_sat_rw.js","bank_sat_rw2.js","bank_sat_rw3.js","bank_sat_rw4.js","bank_sat_rw5.js","bank_sat_math.js","bank_sat_math2.js","bank_sat_math3.js","bank_sat_math4.js","bank_sat_math5.js","bank_sat_easy.js","cards_sat.js","cards_sat2.js","playbook_sat.js"]

GRE_BANKS = ["bank_gre_verbal.js","bank_gre_quant.js","bank_gre_easy.js","cards_gre.js","playbook_gre.js"]

APPS = [
    {"exam": "gmat-focus", "out": "app", "files": GMAT_BANKS,
     "concat": ("BANK_QUANT, BANK_QUANT2, BANK_QUANT3, BANK_QUANT4, BANK_QUANT5, BANK_QUANT6, "
                "BANK_VERBAL, BANK_VERBAL2, BANK_VERBAL3, BANK_VERBAL4, BANK_VERBAL5, BANK_VERBAL6, BANK_VERBAL7, BANK_VERBAL8, "
                "BANK_DI, BANK_DI2, BANK_DI3, BANK_DI4, BANK_DI5, BANK_DI6, BANK_DI7, BANK_DI8, BANK_DI9"),
     "footer": ("GMAT is a registered trademark of the Graduate Management Admission Council (GMAC), which does not "
                "endorse this product. Practice items are original and written for Start From Nowhere. Score bands "
                "shown here are internal estimates, not official GMAT scores."),
     "title": "Start From Nowhere | Adaptive GMAT Focus Trainer",
     "desc": "Start From Nowhere: adaptive GMAT Focus Edition practice that studies you back.",
     "is_404": True},
    {"exam": "sat", "out": "sat/app", "files": SAT_BANKS,
     "concat": "BANK_SAT_RW, BANK_SAT_RW2, BANK_SAT_RW3, BANK_SAT_RW4, BANK_SAT_RW5, BANK_SAT_MATH, BANK_SAT_MATH2, BANK_SAT_MATH3, BANK_SAT_MATH4, BANK_SAT_MATH5, BANK_SAT_EASY",
     "footer": ("SAT is a trademark registered by the College Board, which does not endorse this product. Practice "
                "items are original and written for Start From Nowhere. Content domains follow College Board's "
                "published framework; nothing here reports an official 400 to 1600 score."),
     "title": "Start From Nowhere | Adaptive Digital SAT Trainer",
     "desc": ("Start From Nowhere: adaptive digital SAT practice across the eight official content "
              "domains, with two-module mock sections that route like the real exam."),
     "is_404": False},
    {"exam": "gre", "out": "gre/app", "files": GRE_BANKS,
     "concat": "BANK_GRE_VERBAL, BANK_GRE_QUANT, BANK_GRE_EASY",
     "footer": ("GRE is a registered trademark of ETS, which does not endorse this product. Practice items are "
                "original and written for Start From Nowhere. The trainer covers Verbal Reasoning and Quantitative "
                "Reasoning; Analytical Writing is a scored essay and is not simulated here. Score ranges shown are "
                "internal estimates, not official GRE scores."),
     "title": "Start From Nowhere | Adaptive GRE Trainer",
     "desc": ("Start From Nowhere: adaptive GRE practice across Verbal Reasoning and Quantitative Reasoning, "
              "with section-adaptive mock sections that route like the real exam."),
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
              .replace("{{FOOTER_NOTE}}", app["footer"])
              .replace("{{APP_TITLE}}", app["title"])
              .replace("{{APP_DESC}}", app["desc"])
              .replace("{{SENTINEL}}", partials.sentinel_js("app-" + app["exam"] + "-" + partials.build_id())))
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

# Bank sizes are quoted in llms.txt and in the EDITORIAL fact sheet writers must work from.
# Those numbers go stale the moment a bank grows, so the build checks them against the real
# counts rather than trusting anyone to remember.
def check_counts(name, text, allowed):
    import re as _cre
    for n, unit in _cre.findall(r"\b(\d{2,4})\s+(original|flashcards)\b", text):
        if int(n) not in allowed:
            print(f"ERROR: {name} says '{n} {unit}' but the current counts are "
                  f"{sorted(allowed)}; update it or the bank", file=sys.stderr)
            sys.exit(1)

def no_dashes(name, text):
    if "\u2014" in text or "\u2013" in text:
        print(f"ERROR: em/en dash in {name}", file=sys.stderr); sys.exit(1)

# House rule: no em or en dashes anywhere, docs and sources included. The page checks below
# cover generated output; this covers the files people hand-edit.
_ALLOWED_COUNTS = {bank_count, sat_bank_count, card_count, sat_card_count}
for _counted in ["llms.txt", "src/blog/EDITORIAL.md"]:
    _cp = root / _counted
    if _cp.exists():
        check_counts(_counted, _cp.read_text(), _ALLOWED_COUNTS)

# Prices drift the same way counts do, and llms.txt is worse than a stale page: it is the
# file LLMs read to answer "what does this cost", so a stale number there gets repeated by
# an AI answer engine rather than just sitting on a page nobody visits. It shipped once
# quoting $9.99 and $19.99 months after the real prices became $4.99 and $9.99. Take the
# truth from the trainer template and fail the build on anything that disagrees.
def check_prices(name, text):
    import re as _pre
    tpl = (d / "app_template.html").read_text()
    live = set(_pre.findall(r"mo:'(\$[0-9]+\.[0-9]{2})'", tpl))
    live |= set(_pre.findall(r"or (\$[0-9]+\.[0-9]{2})/yr", tpl))
    if not live:
        print("ERROR: could not read plan prices out of app_template.html", file=sys.stderr)
        sys.exit(1)
    quoted = set(_pre.findall(r"\$[0-9]+\.[0-9]{2}", text))
    # Dollar figures that are not our own prices (loan caps, GI Bill rates, awards) are
    # everywhere in the sourced pages, so only judge figures that look like a plan price.
    plan_like = {q for q in quoted if float(q[1:]) < 200}
    stale = plan_like - live - {"$0.00"}
    if stale:
        print(f"ERROR: {name} quotes {sorted(stale)} but the live plan prices are "
              f"{sorted(live)}; update it", file=sys.stderr)
        sys.exit(1)

check_prices("llms.txt", (root / "llms.txt").read_text())

for _doc in ["README.md", "ROADMAP.md", "CLAUDE.md", "llms.txt", "GROWTH.md", "INTEGRATIONS.md", "I18N.md", "data/DATA.md"]:
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

# Standalone content pages that only need chrome and a build date.
_today = os.environ.get("BLOG_BUILD_DATE") or datetime.date.today().isoformat()
for _src, _dir in [("international.html", "international"), ("scoring.html", "scoring"), ("funding.html", "funding")]:
    page = partials.apply_chrome((d/_src).read_text().replace("{{TODAY}}", _today))
    no_dashes(_src, page)
    if "{{" in page:
        print(f"ERROR: unresolved placeholder in {_src}", file=sys.stderr); sys.exit(1)
    (root/_dir).mkdir(exist_ok=True); (root/_dir/"index.html").write_text(page)

for name in ["terms.html", "privacy.html"]:
    page = partials.apply_chrome((d/name).read_text())
    no_dashes(name, page)
    if "{{" in page:
        print(f"ERROR: unresolved placeholder in {name}", file=sys.stderr); sys.exit(1)
    (root/name).write_text(page)

# Parse every inline script in every built app plus the standalone pages. The app list is
# derived from APPS rather than hardcoded, so a new exam is covered the day it is added
# instead of quietly shipping unparsed.
_app_pages = [root / a["out"] / "index.html" for a in APPS]
for p in _app_pages + [root/"index.html", root/"community"/"index.html",
                       root/"international"/"index.html", root/"scoring"/"index.html",
                       root/"funding"/"index.html", root/"terms.html", root/"privacy.html"]:
    check_scripts(p)
_summary = ", ".join(
    "%s/index.html (%d bytes, %d items)" % (
        a["out"], len(built[a["exam"]][1]),
        len(_re.findall(r"\{\s*id: ?'[A-Z]{2}\d", built[a["exam"]][2])) or
        len(_re.findall(r"\{\s*id: ?'[QVD]", built[a["exam"]][2])))
    for a in APPS)
print("built " + _summary + "; landing, community/, terms, privacy built; inline scripts parse")

import subprocess as _sp
_sp.run([sys.executable, str(d/"build_rankings.py")], check=True)

# I18N.md Stage 0: the content site stays translatable, which means its copy stays
# in markup where browser and search translation can reach it. Text that moves into
# a script literal becomes invisible to every one of those tools, so the count is
# capped per page. Raising a ceiling is a deliberate act, not a side effect.
_I18N_CEILING = {"index.html": 20, "schools/index.html": 60, "international/index.html": 15,
                 "apply/index.html": 40, "exams/index.html": 5, "pricing/index.html": 5}
sys.path.insert(0, str(d))
import i18n_audit as _ia
_over = []
for _rel, _cap in _I18N_CEILING.items():
    _f = root / _rel
    if not _f.exists():
        continue
    _n = len(set(_ia.audit_file(_f)["script"]))
    if _n > _cap:
        _over.append(f"  {_rel}: {_n} script UI strings, ceiling {_cap}")
if _over:
    print("ERROR: page copy is moving into JavaScript, where translation tools cannot reach it.",
          file=sys.stderr)
    print("\n".join(_over), file=sys.stderr)
    print("Move the copy into markup, or raise the ceiling in build.py deliberately. See I18N.md.",
          file=sys.stderr)
    sys.exit(1)
# /apply/ carries a large inline script and is built by build_rankings.py, so it is
# parsed here, after that step, under the same guard as every other inline script.
check_scripts(root/"apply"/"index.html")
_sp.run([sys.executable, str(d/"build_exams.py")], check=True)
