import pathlib, subprocess, sys, tempfile, os, datetime
d = pathlib.Path(__file__).parent; root = d.parent
sys.path.insert(0, str(d))
import partials
# One app per exam. Each entry names the source files that make up that exam's bank,
# the concat expression the template uses to build BANK, and the trademark line for its footer.
GMAT_BANKS = ["bank_quant.js","bank_quant2.js","bank_quant3.js","bank_quant4.js","bank_quant5.js","bank_quant6.js",
              "bank_verbal.js","bank_verbal2.js","bank_verbal3.js","bank_verbal4.js","bank_verbal5.js","bank_verbal6.js","bank_verbal7.js","bank_verbal8.js","bank_verbal9.js",
              "bank_di.js","bank_di2.js","bank_di3.js","bank_di4.js","bank_di5.js","bank_di6.js","bank_di7.js","bank_di8.js","bank_di9.js",
              "cards.js","cards2.js","cards3.js","playbook_gmat.js"]
SAT_BANKS = ["bank_sat_rw.js","bank_sat_rw2.js","bank_sat_rw3.js","bank_sat_rw4.js","bank_sat_rw5.js","bank_sat_rw6.js","bank_sat_math.js","bank_sat_math2.js","bank_sat_math3.js","bank_sat_math4.js","bank_sat_math5.js","bank_sat_easy.js","cards_sat.js","cards_sat2.js","playbook_sat.js"]

GRE_BANKS = ["bank_gre_verbal.js","bank_gre_verbal2.js","bank_gre_rc2.js","bank_gre_rc3.js","bank_gre_quant.js","bank_gre_quant2.js","bank_gre_easy.js","writing_gre.js","cards_gre.js","playbook_gre.js"]

LSAT_BANKS = ["bank_lsat_lr.js","bank_lsat_lr2.js","bank_lsat_lr3.js","bank_lsat_rc.js","bank_lsat_rc2.js","bank_lsat_rc3.js","cards_lsat.js","playbook_lsat.js"]
# ACT Mathematics comes entirely from the generated bank, which is why no hand written math
# file appears here; the schemas are mapped onto ACT taxonomy in src/gen/mapping.py.
ACT_BANKS = ["bank_act_english.js","bank_act_reading.js","bank_act_reading2.js","bank_act_reading3.js","bank_act_science.js","cards_act.js","playbook_act.js"]

APPS = [
    {"exam": "gmat-focus", "out": "app", "gen": "gmat", "files": GMAT_BANKS,
     "concat": ("BANK_QUANT, BANK_QUANT2, BANK_QUANT3, BANK_QUANT4, BANK_QUANT5, BANK_QUANT6, "
                "BANK_VERBAL, BANK_VERBAL2, BANK_VERBAL3, BANK_VERBAL4, BANK_VERBAL5, BANK_VERBAL6, BANK_VERBAL7, BANK_VERBAL8, BANK_VERBAL9, "
                "BANK_DI, BANK_DI2, BANK_DI3, BANK_DI4, BANK_DI5, BANK_DI6, BANK_DI7, BANK_DI8, BANK_DI9"),
     "footer": ("GMAT is a registered trademark of the Graduate Management Admission Council (GMAC), which does not "
                "endorse this product. Practice items are original and written for Start From Nowhere. Score bands "
                "shown here are internal estimates, not official GMAT scores."),
     "title": "Start From Nowhere | Adaptive GMAT Focus Trainer",
     "desc": "Start From Nowhere: adaptive GMAT Focus Edition practice that studies you back.",
     "is_404": True},
    {"exam": "sat", "out": "sat/app", "gen": "sat", "files": SAT_BANKS,
     "concat": "BANK_SAT_RW, BANK_SAT_RW2, BANK_SAT_RW3, BANK_SAT_RW4, BANK_SAT_RW5, BANK_SAT_RW6, BANK_SAT_MATH, BANK_SAT_MATH2, BANK_SAT_MATH3, BANK_SAT_MATH4, BANK_SAT_MATH5, BANK_SAT_EASY",
     "footer": ("SAT is a trademark registered by the College Board, which does not endorse this product. Practice "
                "items are original and written for Start From Nowhere. Content domains follow College Board's "
                "published framework; nothing here reports an official 400 to 1600 score."),
     "title": "Start From Nowhere | Adaptive Digital SAT Trainer",
     "desc": ("Start From Nowhere: adaptive digital SAT practice across the eight official content "
              "domains, with two-module mock sections that route like the real exam."),
     "is_404": False},
    {"exam": "gre", "out": "gre/app", "gen": "gre", "files": GRE_BANKS,
     "concat": "BANK_GRE_VERBAL, BANK_GRE_VERBAL2, BANK_GRE_RC2, BANK_GRE_RC3, BANK_GRE_QUANT, BANK_GRE_QUANT2, BANK_GRE_EASY",
     "footer": ("GRE is a registered trademark of ETS, which does not endorse this product. Practice items are "
                "original and written for Start From Nowhere. The trainer covers Verbal Reasoning and Quantitative "
                "Reasoning; Analytical Writing is a scored essay and is not simulated here. Score ranges shown are "
                "internal estimates, not official GRE scores."),
     "title": "Start From Nowhere | Adaptive GRE Trainer",
     "desc": ("Start From Nowhere: adaptive GRE practice across Verbal Reasoning and Quantitative Reasoning, "
              "with section-adaptive mock sections that route like the real exam."),
     "is_404": False},
    {"exam": "lsat", "out": "lsat/app", "gen": "lsat", "files": LSAT_BANKS,
     "concat": "BANK_LSAT_LR, BANK_LSAT_LR2, BANK_LSAT_LR3, BANK_LSAT_RC, BANK_LSAT_RC2, BANK_LSAT_RC3",
     "footer": ("LSAT is a registered trademark of the Law School Admission Council (LSAC), which does not "
                "endorse this product. Practice items are original and written for Start From Nowhere. LSAC "
                "publishes 35 minutes per section and, for Reading Comprehension, four sets of five to eight "
                "questions; it does not publish a Logical Reasoning question count, so our 25-question practice "
                "section is our own length, not an LSAT specification. Score ranges shown are internal "
                "estimates, not official LSAT scores, and the LSAT reports no section scores."),
     "title": "Start From Nowhere | Adaptive LSAT Trainer",
     "desc": ("Start From Nowhere: adaptive LSAT practice across Logical Reasoning and Reading Comprehension, "
              "built on the skills LSAC publishes for each section."),
     "is_404": False},
    {"exam": "act", "out": "act/app", "gen": "act", "files": ACT_BANKS,
     "concat": "BANK_ACT_ENGLISH, BANK_ACT_READING, BANK_ACT_READING2, BANK_ACT_READING3, BANK_ACT_SCIENCE",
     "footer": ("ACT is a registered trademark of ACT Education Corp., which does not endorse this product. "
                "Practice items are original and written for Start From Nowhere. Section lengths and reporting "
                "categories follow ACT published materials for the enhanced test, including four answer choices "
                "in every section and a Composite drawn from English, Mathematics and Reading only. Score ranges "
                "shown are internal estimates, not official ACT scores."),
     "title": "Start From Nowhere | Adaptive ACT Trainer",
     "desc": ("Start From Nowhere: adaptive ACT practice across English, Mathematics, Reading and the optional "
              "Science section, keyed to ACT published reporting categories."),
     "is_404": False},
]

engine = (d/"engine.js").read_text(); tpl = (d/"app_template.html").read_text()
charts = (d/"charts.js").read_text()
built = {}
# The generated banks are built first; the schemas in src/gen/ are their source of truth.
import build_banks
print("generating item banks from src/gen/ ...")
GEN_REPORT = build_banks.main()
GEN_COUNT = {}
for (_exam, _skill), (_n, _drop, _errs) in GEN_REPORT.items():
    GEN_COUNT[_exam] = GEN_COUNT.get(_exam, 0) + _n
GEN_DIR = d / "generated"

for app in APPS:
    banks = "\n".join((d/f).read_text() for f in app["files"])
    gen_file = GEN_DIR / ("bank_gen_%s.js" % app["gen"]) if app["gen"] else None
    gen_src = gen_file.read_text() if (gen_file and gen_file.exists()) else ""
    # The deferred remainder arrives in chunks because Cloudflare rejects a static asset
    # over 25 MiB and the ACT remainder is about 30. Sorted numerically, not
    # lexically, so rest10 lands after rest9 rather than after rest1.
    rest_files = (sorted(GEN_DIR.glob("bank_gen_%s_rest*.js" % app["gen"]),
                         key=lambda q: int("".join(c for c in q.stem.split("_rest")[-1] if c.isdigit()) or 0))
                  if app["gen"] else [])
    rest_parts = [q.read_text() for q in rest_files]
    concat = app["concat"] + (", BANK_GEN_" + app["gen"].upper() if gen_src else "")
    # The bank ships as its own file next to index.html. The path is absolute because the
    # GMAT app doubles as 404.html and is served from arbitrary URLs.
    #
    # It ships in two pieces. bank.js blocks, because nothing can render without items,
    # and carries every hand written item plus a strided slice of the generated ones.
    # bank_rest.js is async and pushes the remainder into the same array when it lands.
    # Before this split, time to first question was time to download the entire bank:
    # 20 seconds for GMAT and 23 for ACT on regular 3G, measured in src/smoke_load.js.
    bank_path = "/" + app["out"] + "/bank.js"
    bank_js = ("// GENERATED FILE. Built by src/build.py; edit the banks in src/ instead.\n"
               + banks + "\n" + gen_src + "\n"
               + "const BANK = [].concat(%s);\n" % concat)
    bank_out = root / app["out"]
    bank_out.mkdir(parents=True, exist_ok=True)
    (bank_out / "bank.js").write_text(bank_js)
    # const forbids reassignment, not mutation, so the remainder pushes into the same
    # array the app already holds a reference to. The hook lets the app reindex; the
    # guard means a missing hook degrades to a bigger pool rather than an exception.
    # Clear a previous build's single-file remainder. The deploy uploads whatever is in
    # the output directory, so a stale 30 MiB bank_rest.js left over from before the
    # chunking would be shipped alongside the chunks and would fail the 25 MiB asset
    # limit, which is the exact failure the chunking exists to avoid.
    _legacy_rest = bank_out / "bank_rest.js"
    if _legacy_rest.exists(): _legacy_rest.unlink()
    rest_paths = []
    for _i, _part in enumerate(rest_parts, start=1):
        rest_js = ("// GENERATED FILE. Deferred item bank, chunk %d of %d; see src/build.py.\n"
                   % (_i, len(rest_parts))
                   + _part + "\n"
                   + "BANK.push.apply(BANK, BANK_GEN_%s_REST%d);\n" % (app["gen"].upper(), _i)
                   + "if (typeof window.__bankGrew === 'function') window.__bankGrew();\n")
        (bank_out / ("bank_rest%d.js" % _i)).write_text(rest_js)
        rest_paths.append("/" + app["out"] + "/bank_rest%d.js" % _i)
    # Every chunk reindexes on arrival, so the pool grows as each lands rather than only
    # once the last one does, and a chunk that fails to load costs its own items and no
    # more.
    rest_tags = "\n".join('<script src="%s" async></script>' % q for q in rest_paths)

    # A service worker per trainer. Scoped per app rather than one at the root: the five
    # ship different banks, and a shared cache would have them evicting each other's
    # largest file. Offline is what lets a student keep practising on a train, and it is
    # also the substance behind the App Review 4.2 claim that this is not a repackaged
    # website.
    _scope = "/" + app["out"] + "/"
    _precache = ([_scope, _scope + "bank.js"] + rest_paths
                 + ["/manifest.json", "/icons/icon-192.png", "/icons/icon-512.png"])
    import json as _sw_json
    _sw = ((d / "sw_template.js").read_text()
           .replace("{{SW_VERSION}}", partials.build_id())
           .replace("{{SCOPE_PATH}}", _scope)
           .replace("{{PRECACHE_JSON}}", _sw_json.dumps(_precache)))
    (bank_out / "sw.js").write_text(_sw)
    # The social queue is admin only and about 76KB. It is written once to the site root and
    # fetched on demand by Admin > Social rather than inlined into the shell, so a student
    # loading the trainer never downloads a byte of it.
    _social = GEN_DIR / "social.js"
    if _social.exists():
        (root / "social.js").write_text(_social.read_text(), encoding="utf-8")
    out = (tpl.replace("{{EXAM_ID}}", app["exam"])
              .replace("{{BANK_SRC}}", bank_path)
              .replace("{{BANK_REST_TAGS}}", rest_tags)
              .replace("{{SW_SRC}}", _scope + "sw.js")
              .replace("{{SW_SCOPE}}", _scope)
              .replace("{{ENGINE}}", engine)
              .replace("{{CHARTS}}", charts)
              .replace("{{FOOTER_NOTE}}", app["footer"])
              .replace("{{APP_TITLE}}", app["title"])
              .replace("{{APP_DESC}}", app["desc"])
              # The app builds its own chrome rather than going through apply_chrome, so the
              # consent module has to be added here too. Missing it was how the trainer,
              # the one page people spend real time on, ended up without a banner.
              .replace("{{SENTINEL}}", partials.consent_js()
                       + partials.sentinel_js("app-" + app["exam"] + "-" + partials.build_id())))
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
# Counts drive the numbers the landing page advertises, so they include the generated
# items as well as the hand written ones. Undercounting here would understate the product;
# overcounting would be a claim we cannot back.
hand_gmat = len(_re.findall(r"\{\s*id: ?'[QVD]", gmat_banks_src))
card_count = len(_re.findall(r"\{\s*id: ?'c\d", gmat_banks_src))
hand_sat = len(_re.findall(r"\{\s*id: ?'S[RM]\d", sat_banks_src))
sat_card_count = len(_re.findall(r"\{\s*id: ?'s\d", sat_banks_src))
gre_banks_src = built["gre"][2]
hand_gre = len(_re.findall(r"\{\s*id: ?['\"]G[QVER]\d", gre_banks_src))
gre_card_count = len(_re.findall(r"\{\s*id: ?'g\d", gre_banks_src))
lsat_banks_src = built["lsat"][2]
hand_lsat = len(_re.findall(r"\{\s*id: ?['\"]L[LC]\d", lsat_banks_src))
lsat_card_count = len(_re.findall(r"\{\s*id: ?'l\d", lsat_banks_src))
act_banks_src = built["act"][2]
hand_act = len(_re.findall(r"\{\s*id: ?'A[ERS]\d", act_banks_src))
act_card_count = len(_re.findall(r"\{\s*id: ?'a\d", act_banks_src))
# Every bank file listed for an exam must contribute at least one counted item.
#
# The counts above are regexes over concatenated source, and a regex that counts things
# assumes a formatting convention. bank_lsat_rc2.js emits JSON escaped strings, so its
# ids were double quoted, none of them matched, and a file holding 35 items counted as
# zero while the build printed a total that looked plausible (INC-0059). A total cannot
# detect that; only a per-source check can.
_ID_PAT = {"gmat": r"\{\s*id: ?['\"](?:Q|V|D)\w*\d",
           "sat": r"\{\s*id: ?['\"]S[RM]\d",
           "gre": r"\{\s*id: ?['\"]G[VQER]\d",
           "lsat": r"\{\s*id: ?['\"]L[LC]\d",
           "act": r"\{\s*id: ?['\"]A[ERS]\d"}
_blind = []
# All five exams, not the two that happened to be in hand when the guard was written.
# A guard covering a subset is the same gap one level up, and it showed: the GRE id
# pattern was G[QVE] and a reading bank using GR ids counted zero, silently, exactly as
# INC-0059 did for the LSAT.
for _ex, _files in (("gmat", GMAT_BANKS), ("sat", SAT_BANKS), ("gre", GRE_BANKS),
                    ("lsat", LSAT_BANKS), ("act", ACT_BANKS)):
    for _f in _files:
        if not _f.startswith("bank_"):
            continue
        _src = (d / _f).read_text(encoding="utf-8")
        if not _re.search(_ID_PAT[_ex], _src):
            _blind.append("%s: %s holds items the counter cannot see" % (_ex, _f))
if _blind:
    print("ERROR: the item counter is blind to a bank file, so the published count is "
          "short by however many items it holds.", file=sys.stderr)
    print("\n".join("  " + b for b in _blind), file=sys.stderr)
    sys.exit(1)

# Every file that launches Playwright resolves the browser through src/chromium_path.js.
#
# Reading process.env.CHROMIUM_PATH directly passes executablePath: undefined when the
# variable is unset, which hands the decision back to Playwright, which is the case the
# resolver exists to override. That is INC-0055, and it came back in the three suites the
# fix did not touch, unnoticed for a week because CI installs the browser Playwright
# expects and only the sandbox does not (INC-0067). Extracting a helper does not migrate
# the callers, so the direct read fails the build instead.
_launchers = sorted(p for p in d.glob("*.js")
                    if "chromium.launch" in p.read_text(encoding="utf-8"))
_direct = [p.name for p in _launchers
           if "process.env.CHROMIUM_PATH" in p.read_text(encoding="utf-8")
           or "chromiumPath()" not in p.read_text(encoding="utf-8")]
if _direct:
    print("ERROR: a Playwright launch does not go through chromiumPath() from "
          "src/chromium_path.js, so it will resolve a browser that is not installed "
          "wherever Playwright's own path is wrong.", file=sys.stderr)
    print("\n".join("  " + n for n in _direct), file=sys.stderr)
    sys.exit(1)
if not _launchers:
    print("ERROR: no file launches Playwright, so the browser suites are not being "
          "found by the guard that checks how they launch.", file=sys.stderr)
    sys.exit(1)

bank_count = hand_gmat + GEN_COUNT.get("gmat", 0)
sat_bank_count = hand_sat + GEN_COUNT.get("sat", 0)
gre_bank_count = hand_gre + GEN_COUNT.get("gre", 0)
lsat_bank_count = hand_lsat + GEN_COUNT.get("lsat", 0)
act_bank_count = hand_act + GEN_COUNT.get("act", 0)
def round_down(n):
    """A round number that is still true.

    The landing page is the one place a precise count reads as false precision:
    "18,073 original practice questions" invites the reader to wonder who counted and
    when, and it is stale the day a category grows. It always rounds DOWN, so the
    claim stays true between builds rather than becoming a promise the bank has to
    catch up with.
    """
    # Two significant figures, so the step scales with the number instead of being a
    # flat 500 across a range where 500 is most of the value. A fixed step turned 1,451
    # into 1,000+, which is true but reads as a smaller library than we have.
    if n >= 10000:
        step = 1000
    elif n >= 1000:
        step = 100
    elif n >= 100:
        step = 100
    else:
        return format(n, ",d")
    return format((n // step) * step, ",d") + "+"


total_bank_count = bank_count + sat_bank_count + gre_bank_count + lsat_bank_count + act_bank_count
# Tracked skills come from the engine registry itself, so the landing page can never
# drift from the number of ratings the apps actually keep.
_skill_probe = subprocess.run(
    ["node", "-e",
     "const fs=require('fs');const s=fs.readFileSync(process.argv[1],'utf8');"
     # Every live exam, not just the first two. The landing page advertises this
     # number, and it read "20 Skills" for months after the GRE, LSAT and ACT shipped.
     "console.log(eval(s+'; GMAT_SKILLS.length + SAT_SKILLS.length + GRE_SKILLS.length"
     " + LSAT_SKILLS.length + ACT_SKILLS.length'))",
     str(d/"engine.js")],
    capture_output=True, text=True)
if _skill_probe.returncode != 0:
    print("ERROR: could not count tracked skills from engine.js\n" + _skill_probe.stderr.strip(), file=sys.stderr); sys.exit(1)
total_skills = _skill_probe.stdout.strip()

# Bank sizes are quoted in llms.txt and in the EDITORIAL fact sheet writers must work from.
# Those numbers go stale the moment a bank grows, so the build checks them against the real
# counts rather than trusting anyone to remember.
#
# The digit range matters. It was {2,4} until the banks passed ten thousand, at which
# point the two largest counts on the page stopped matching the pattern and the guard
# would have gone on passing while checking nothing. A guard that silently narrows its
# own scope is worse than one that fails.
def check_counts(name, text, allowed):
    import re as _cre
    # Two patterns, and the second one matters. The first was original|flashcards alone,
    # and the LSAT line in llms.txt was phrased "65 questions today" precisely because the
    # number was small and the page said so plainly. That honest phrasing put it outside
    # the pattern and the figure sat at less than half the true count.
    #
    # The obvious repair, adding items and questions to the noun list, immediately flagged
    # "64 questions" in the editorial fact sheet, which is the real GMAT Focus question
    # count from GMAC and not a bank size at all. A guard that cries wolf gets switched
    # off, so widening the wording was the wrong trade (INC-0063). The second pattern
    # matches a phrase only our own bank size can produce.
    hits = (_cre.findall(r"\b(\d{2,6})\s+(original|flashcards)\b", text)
            + [(n, "in the item bank") for n in
               _cre.findall(r"item bank is (\d{2,6})\b", text)])
    for n, unit in hits:
        if int(n) not in allowed:
            print(f"ERROR: {name} says '{n} {unit}' but the current counts are "
                  f"{sorted(allowed)}; update it or the bank", file=sys.stderr)
            sys.exit(1)

def no_dashes(name, text):
    if "\u2014" in text or "\u2013" in text:
        print(f"ERROR: em/en dash in {name}", file=sys.stderr); sys.exit(1)

# House rule: no em or en dashes anywhere, docs and sources included. The page checks below
# cover generated output; this covers the files people hand-edit.
_ALLOWED_COUNTS = {bank_count, sat_bank_count, gre_bank_count, lsat_bank_count,
                   act_bank_count, card_count, sat_card_count, gre_card_count,
                   lsat_card_count, act_card_count, total_bank_count}
for _counted in ["llms.txt", "src/blog/EDITORIAL.md"]:
    _cp = root / _counted
    if _cp.exists():
        check_counts(_counted, _cp.read_text(), _ALLOWED_COUNTS)

# Banned sources in prose. The source policy was enforced on the structured corpora and
# not on the words, so three posts and the editorial fact sheet went on citing The
# Princeton Review, Applerouth and Sallie Mae after the same citations were cleaned out
# of data/exams.json (INC-0082). The fact sheet is the one that mattered: it is the list
# of approved figures a post is written from, so a wrong entry there reappears in the
# next post. Matching only inside a "(Name, year)" citation is what lets this run over
# the very files that legitimately name these sites as the list of what never to cite.
sys.path.insert(0, str(d))
from sources import banned_citations as _banned_citations
_cite_bad = []
for _doc in sorted((root / "src" / "blog").glob("*.html")) + \
        [root / "src" / "blog" / "EDITORIAL.md", root / "data" / "DATA.md"]:
    if not _doc.exists():
        continue
    for _name, _inner in _banned_citations(_doc.read_text()):
        _cite_bad.append("%s cites %s in \"(%s)\"" % (_doc.name, _name, _inner))
if _cite_bad:
    for _b in _cite_bad:
        print("ERROR: banned source in a citation: %s" % _b, file=sys.stderr)
    print("CLAUDE.md bans coaching-site blogs outright. Replace the figure with the "
          "test maker's own published one, or drop it.", file=sys.stderr)
    sys.exit(1)

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

for _doc in ["README.md", "ROADMAP.md", "CLAUDE.md", "HANDOFF.md", "llms.txt", "GROWTH.md", "INTEGRATIONS.md", "I18N.md", "data/DATA.md"]:
    _p = root / _doc
    if _p.exists():
        no_dashes(_doc, _p.read_text())
for _src in sorted(d.glob("bank_*.js")) + sorted(d.glob("cards*.js")) + sorted(d.glob("playbook_*.js")) + [d/"engine.js"]:
    no_dashes(_src.name, _src.read_text())

# INC-0076. Python's str.capitalize() uppercases the first character and LOWER CASES
# every other one, so a stored fragment carrying a name comes out as "The fenwick track".
# 180 items shipped that way, 70 of them in the key. framework.upfirst raises the first
# character and nothing else, and it is the only correct one for a generator, so the
# wrong one is banned rather than reviewed for.
for _g in sorted((d/"gen").glob("*.py")):
    if ".capitalize()" in _g.read_text():
        print(f"ERROR: {_g.name} calls str.capitalize(), which lower cases the rest of "
              f"the string and flattens any name in it; use framework.upfirst "
              f"(INC-0076)", file=sys.stderr)
        sys.exit(1)

import json as _json_mod
_college_n = len(list((root/"data"/"colleges").glob("*.json")))
_mba_n = sum(1 for _p in (root/"data"/"schools").glob("*.json")
             if not _json_mod.loads(_p.read_text()).get("discontinued"))
landing = ((d/"landing.html").read_text().replace("{{BANK_COUNT}}", str(bank_count)).replace("{{CARD_COUNT}}", str(card_count))
           .replace("{{SAT_BANK_COUNT}}", str(sat_bank_count)).replace("{{SAT_CARD_COUNT}}", str(sat_card_count))
           .replace("{{TOTAL_BANK_ROUND}}", round_down(total_bank_count))
           .replace("{{TOTAL_BANK_COUNT}}", format(total_bank_count, ",d")).replace("{{TOTAL_SKILLS}}", total_skills)
           # Library sizes are advertised on the landing page, so they are counted at
           # build time rather than typed. "2 Exams" sat on that page for months after
           # the third, fourth and fifth shipped.
           .replace("{{COLLEGE_ROUND}}", round_down(_college_n))
           .replace("{{COLLEGE_COUNT}}", format(_college_n, ",d"))
           .replace("{{MBA_COUNT}}", format(_mba_n, ",d"))
           .replace("{{RANKED_ROUND}}", round_down(_college_n + _mba_n))
           .replace("{{RANKED_TOTAL}}", format(_college_n + _mba_n, ",d")))
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
for _src, _dir in [("international.html", "international"), ("scoring.html", "scoring"),
                   ("funding.html", "funding"), ("do_not_sell.html", "do-not-sell")]:
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
                       root/"funding"/"index.html", root/"terms.html", root/"privacy.html",
                       root/"do-not-sell"/"index.html"]:
    check_scripts(p)

# The bank is not an inline script, so check_scripts never saw it, and the largest
# artefact the site ships was the one file nothing parsed. A syntax error in it takes the
# trainer down exactly as INC-0001 did, and would have built cleanly (INC-0060). Every
# built bank and every chunk is parsed here, next to the pages.
_banks = []
for _a in APPS:
    _banks += sorted((root / _a["out"]).glob("bank*.js"))
if not _banks:
    print("ERROR: no built bank files found to parse; the check below would pass vacuously.",
          file=sys.stderr)
    sys.exit(1)
for _b in _banks:
    _r = subprocess.run(["node", "--check", str(_b)], capture_output=True, text=True)
    if _r.returncode != 0:
        print("ERROR: %s does not parse, and it is the file every visitor downloads."
              % _b.relative_to(root), file=sys.stderr)
        print(_r.stderr.strip()[:800], file=sys.stderr)
        sys.exit(1)
print("  parsed %d built bank file(s)" % len(_banks))
# The shell and the bank are now separate downloads, so report both, and report the
# whole bank rather than only the hand written part of it.
_TOTAL = {"gmat-focus": bank_count, "sat": sat_bank_count, "gre": gre_bank_count,
          "lsat": lsat_bank_count, "act": act_bank_count}
_summary = ", ".join(
    "%s (shell %dk, bank %dk, %d items)" % (
        a["out"], round(len(built[a["exam"]][1]) / 1024),
        round((root / a["out"] / "bank.js").stat().st_size / 1024),
        _TOTAL[a["exam"]])
    for a in APPS)
# Cloudflare refuses any single static asset over 25 MiB, and the deploy fails outright
# rather than degrading, so this is a build gate and not a warning. It caught the ACT
# deferred bank at 29.9 MiB when TARGET went to 3300, which is why that bank now ships in
# chunks. Checked across everything the deploy uploads, not just the banks, because the
# next file to cross the line will not necessarily be one.
_ASSET_LIMIT = 25 * 1024 * 1024
_too_big = []
for _p in root.rglob("*"):
    if not _p.is_file():
        continue
    _rel = _p.relative_to(root).as_posix()
    if _rel.startswith((".git/", "src/", "data/", "supabase/", "node_modules/", "design/")):
        continue
    _sz = _p.stat().st_size
    if _sz > _ASSET_LIMIT:
        _too_big.append((_rel, _sz))
if _too_big:
    for _rel, _sz in sorted(_too_big, key=lambda t: -t[1]):
        print("ERROR: %s is %.1f MiB, over the 25 MiB Cloudflare static asset limit"
              % (_rel, _sz / 1048576.0), file=sys.stderr)
    print("ERROR: the deploy would be rejected; split the file or lower TARGET in "
          "src/build_banks.py", file=sys.stderr)
    sys.exit(1)

print("built " + _summary + "; landing, community/, terms, privacy built; inline scripts parse")

import subprocess as _sp
_sp.run([sys.executable, str(d/"build_rankings.py")], check=True)

# /apply/ carries a large inline script and is built by build_rankings.py, so it is
# parsed here, after that step, under the same guard as every other inline script.
check_scripts(root/"apply"/"index.html")
_sp.run([sys.executable, str(d/"build_colleges.py")], check=True)
# The source policy validators are only as good as the last time anyone saw one
# fail. This runs validate_exams against deliberately bad records, both the kind
# it must refuse and the kind it must not, before it is trusted on the real file
# a line later (INC-0082).
_sp.run([sys.executable, str(d/"validate_exams.py")], check=True)
_sp.run([sys.executable, str(d/"build_exams.py")], check=True)
_sp.run([sys.executable, str(d/"build_guide.py")], check=True)

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


# ---------------------------------------------------------------------------
# The Build Playbook, rebuilt with the site.
#
# It is generated from the chapters, the defect ledger and a harvest of this repository,
# so it goes stale the moment either moves. Running it here rather than on request is the
# whole point: a document that has to be remembered is a document that falls behind the
# thing it describes.
#
# It is deliberately NOT fatal. The playbook is a deliverable about the build, not part of
# the site, and a chapter citing a file that was just renamed should not stop a deploy. It
# prints loudly instead, and src/smoke_playbook.js fails the test suite, which is the
# right place for it to be blocking.
try:
    _pb = subprocess.run([sys.executable, str(d / "build_playbook.py")],
                         capture_output=True, text=True, timeout=300)
    if _pb.returncode == 0:
        print(_pb.stdout.strip())
    else:
        # ERROR, not WARNING, and still exit zero. playbook/ is excluded from the
        # deploy so a broken chapter must not stop the site shipping, but the word a
        # non fatal step fails with is the whole of its signal, and three commits went
        # out with a stale playbook because this said WARNING (INC-0080).
        print("ERROR: the playbook did not build; the site did. Run "
              "python3 src/build_playbook.py to see why.", file=sys.stderr)
        print((_pb.stderr or _pb.stdout).strip(), file=sys.stderr)
except Exception as _e:
    print("ERROR: could not run the playbook build: %s" % _e, file=sys.stderr)
