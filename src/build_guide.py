"""Builds /guide/: the study guides, one page per topic.

Three sources, and nothing else:

  the mathematics    which belongs to nobody and is written out in src/guide/
  data/exams.json    every exam FIGURE, each carrying its source, year and URL
  our own bank       a real item at each difficulty, pulled through exam_harness

The third is the part that makes this more than a reference sheet. The exam is
adaptive, so a topic is not one thing: the engine serves a different question at
level 1 than at level 5, and the guide shows the student the actual item rather than
describing it. That also means a guide page cannot drift from the practice behind it,
because the practice is what the page is quoting.
"""
import html
import json
import pathlib
import subprocess
import sys

D = pathlib.Path(__file__).parent
ROOT = D.parent
sys.path.insert(0, str(D))
import partials                                     # noqa: E402
from guide import gmat_quant, gmat_verbal           # noqa: E402
from guide.model import check_all                   # noqa: E402
from guide import coverage                          # noqa: E402

SITE = "https://startfromnowhere.com"
OUT = ROOT / "guide"

# Which exam each guide is for, and where its trainer lives.
EXAMS = {
    "gmat": dict(harness="gmat-focus", app="/app/", name="GMAT Focus Edition",
                 short="GMAT",
                 blurb="Three sections, 2 hours 15 minutes, every one of them adaptive. "
                       "The guides below cover what each section actually asks."),
}

# exam -> section key -> the section. Adding a section is an entry here and a topic
# module; nothing else in this file needs to know about it.
SECTIONS = {
    "gmat": {
        "quant": dict(title="Quantitative Reasoning", short="Quant",
                      topics=gmat_quant.TOPICS,
                      blurb="Arithmetic, algebra, word problems and the statistics that "
                            "sit on top of them. No calculator, so the work is chosen to "
                            "be short when you see the shape of it."),
        "verbal": dict(title="Verbal Reasoning", short="Verbal",
                       topics=gmat_verbal.TOPICS,
                       facts_title="The Question Forms",
                       facts_word="question forms",
                       facts_lede="What replaces a formula here is the skeleton of each "
                                  "question and what it is really asking underneath the "
                                  "wording. The exam rewrites the wording constantly and "
                                  "changes the skeleton almost never.",
                       blurb="Reading comprehension and critical reasoning. There is no "
                             "formula sheet, which is why people assume it cannot be "
                             "studied, and every question here still has a mechanical "
                             "structure underneath it."),
    },
}

# Sections we have not written yet. The hub lists these as unwritten rather than leaving
# them off, because a guide index that silently omits a third of the exam is the exact
# failure the coverage check exists to prevent, one level up.
PLANNED = {
    "gmat": [
        ("Data Insights", "Table analysis, graphics, multi-source reasoning, two-part "
                          "analysis and data sufficiency."),
    ],
}


def esc(s):
    return html.escape(str(s), quote=True)


def bank_samples(harness_id, skills):
    """One real item per skill per difficulty, straight out of the shipped bank.

    Through exam_harness because that is the single place that knows which files make
    up an exam, and a second list here would be a second thing to keep in step.
    """
    js = r"""
const h = require('./exam_harness.js');
const api = h.load(h.byId[process.argv[1]]);
const want = process.argv.slice(2);
const out = {};
out.__known = [...new Set(api.BANK.map(q => q.skill))].sort();
for (const sk of want) {
  out[sk] = {};
  for (let d = 1; d <= 5; d++) {
    const c = api.BANK.filter(q => q.skill === sk && q.diff === d
                                   && Array.isArray(q.choices) && !q.answerType);
    if (c.length) {
      const q = c[Math.floor(c.length / 2)];
      out[sk][d] = {stem: q.stem, choices: q.choices, answer: q.answer,
                    expl: q.expl || '', n: c.length};
    }
  }
}
process.stdout.write(JSON.stringify(out));
"""
    p = subprocess.run(["node", "-e", js, harness_id] + list(skills),
                       cwd=str(D), capture_output=True, text=True)
    if p.returncode != 0:
        raise SystemExit("build_guide: could not read the bank through exam_harness.\n"
                         + (p.stderr or "")[-600:])
    return json.loads(p.stdout)


def facts_html(t):
    rows = []
    for name, expr, says in t.facts:
        rows.append(
            '<div class="fx"><div class="fx-name">%s</div>'
            '<div class="fx-expr">%s</div>'
            '<div class="fx-says">%s</div></div>' % (esc(name), esc(expr), esc(says)))
    return '<div class="fx-grid">%s</div>' % "".join(rows)


def worked_html(t):
    out = []
    for w in t.worked:
        steps = "".join("<li>%s</li>" % esc(s) for s in w["steps"])
        note = ('<p class="w-why"><b>Why it works.</b> %s</p>' % esc(w["why"])
                if w.get("why") else "")
        out.append(
            '<div class="w"><p class="w-ask">%s</p><ol class="w-steps">%s</ol>'
            '<p class="w-ans">Answer: <b>%s</b></p>%s</div>'
            % (esc(w["ask"]), steps, esc(w["answer"]), note))
    return "".join(out)


def ladder_html(t, samples, app):
    """The difficulty roadmap, with a real item beside each rung where we have one."""
    rows = []
    for d in (1, 2, 3, 4, 5):
        item = (samples.get(t.skill) or {}).get(str(d)) or (samples.get(t.skill) or {}).get(d)
        shown = ""
        if item:
            letters = "ABCDE"
            opts = "".join(
                '<li%s>%s</li>' % (' class="key"' if i == item["answer"] else "", esc(c))
                for i, c in enumerate(item["choices"]))
            shown = ('<details class="lx"><summary>See a real level %d item '
                     '(%d in the bank)</summary>'
                     '<p class="lx-stem">%s</p><ol type="A" class="lx-opts">%s</ol>'
                     '<p class="lx-key">Answer: <b>%s</b></p></details>'
                     % (d, item["n"], esc(item["stem"]), opts,
                        esc(letters[item["answer"]] if item["answer"] < 5 else "")))
        rows.append('<div class="rung"><div class="rung-n">Level %d</div>'
                    '<div class="rung-b"><p>%s</p>%s</div></div>'
                    % (d, esc(t.ladder[d]), shown))
    return "".join(rows)


def topic_page(tpl, exam, sec_key, t, samples, prev_t, next_t):
    sec = SECTIONS[exam][sec_key]
    e = EXAMS[exam]
    traps = "".join("<li>%s</li>" % esc(x) for x in t.traps)
    nav = []
    if prev_t:
        nav.append('<a class="btn sec" href="../%s/">Previous: %s</a>'
                   % (esc(prev_t.slug), esc(prev_t.title)))
    if next_t:
        nav.append('<a class="btn" href="../%s/">Next: %s</a>'
                   % (esc(next_t.slug), esc(next_t.title)))
    ld = json.dumps({
        "@context": "https://schema.org", "@type": "LearningResource",
        "name": "%s: %s" % (e["short"], t.title),
        "educationalLevel": "Graduate admissions test preparation",
        "teaches": t.title,
        "publisher": {"@type": "Organization", "name": "Start From Nowhere"}})
    return (tpl
            .replace("{{FACTS_TITLE}}", esc(sec.get("facts_title", "The Formulas")))
            .replace("{{FACTS_LEDE}}", esc(sec.get(
                "facts_lede",
                "Each one with what it actually says, because a formula you can only "
                "recite is a formula you will misapply under time.")))
            .replace("{{TITLE}}", esc(t.title))
            .replace("{{EXAM_SHORT}}", esc(e["short"]))
            .replace("{{EXAM}}", esc(exam))
            .replace("{{SEC}}", esc(sec_key))
            .replace("{{SEC_TITLE}}", esc(sec["title"]))
            .replace("{{SLUG}}", esc(t.slug))
            .replace("{{AREA}}", esc(t.area))
            .replace("{{IDEA}}", esc(t.idea))
            .replace("{{WHY}}", esc(t.why))
            .replace("{{FACTS}}", facts_html(t))
            .replace("{{WORKED}}", worked_html(t))
            .replace("{{TRAPS}}", traps)
            .replace("{{LADDER}}", ladder_html(t, samples, e["app"]))
            .replace("{{APP}}", esc(e["app"]))
            .replace("{{PAGENAV}}", "".join(nav))
            .replace("{{LD}}", ld))


def section_index(tpl, exam, sec_key):
    sec = SECTIONS[exam][sec_key]
    e = EXAMS[exam]
    by_area = {}
    for t in sec["topics"]:
        by_area.setdefault(t.area, []).append(t)
    blocks = []
    for area, ts in by_area.items():
        cards = "".join(
            '<a class="tcard" href="%s/"><span class="tcard-t">%s</span>'
            '<span class="tcard-i">%s</span>'
            '<span class="tcard-m">%d %s &middot; %d worked examples</span></a>'
            % (esc(t.slug), esc(t.title), esc(t.idea), len(t.facts),
               esc(sec.get("facts_word", "formulas")), len(t.worked))
            for t in ts)
        blocks.append('<section class="area"><h2>%s</h2><div class="tgrid">%s</div></section>'
                      % (esc(area), cards))
    ld = json.dumps({"@context": "https://schema.org", "@type": "Course",
                     "name": "%s %s" % (e["short"], sec["title"]),
                     "description": sec["blurb"],
                     "provider": {"@type": "Organization",
                                  "name": "Start From Nowhere"}})
    return (tpl
            .replace("{{EXAM_SHORT}}", esc(e["short"]))
            .replace("{{EXAM}}", esc(exam))
            .replace("{{SEC}}", esc(sec_key))
            .replace("{{SEC_TITLE}}", esc(sec["title"]))
            .replace("{{BLURB}}", esc(sec["blurb"]))
            .replace("{{COUNT}}", str(len(sec["topics"])))
            .replace("{{FACTS_WORD}}", esc(sec.get("facts_word", "formulas").title()))
            .replace("{{FORMULAS}}", str(sum(len(t.facts) for t in sec["topics"])))
            .replace("{{BLOCKS}}", "".join(blocks))
            .replace("{{APP}}", esc(e["app"]))
            .replace("{{LD}}", ld))


def main():
    problems = check_all(gmat_quant.TOPICS)
    if problems:
        print("build_guide: unfinished topics", file=sys.stderr)
        for p in problems:
            print("  " + p, file=sys.stderr)
        sys.exit(1)

    topic_tpl = (D / "guide_topic_template.html").read_text()
    index_tpl = (D / "guide_section_template.html").read_text()
    hub_tpl = (D / "guide_hub_template.html").read_text()
    written = 0
    for exam, e in EXAMS.items():
        secs = SECTIONS.get(exam, {})
        skills = sorted({t.skill for s in secs.values() for t in s["topics"]})
        samples = bank_samples(e["harness"], skills) if skills else {}
        # A topic whose skill the engine does not know still renders: the ladder just
        # comes out with prose and no real items, which looks deliberate. Checked
        # against the bank itself rather than a list kept here, because a second list
        # is a second thing to drift.
        known = set(samples.pop("__known", []))
        unknown = sorted(sk for sk in skills if sk not in known)
        if unknown:
            raise SystemExit(
                "build_guide: %s has topics whose skill the %s bank does not know: %s.\n"
                "Known skills: %s" % (exam, e["harness"], ", ".join(unknown),
                                      ", ".join(sorted(known))))
        mute = sorted(sk for sk in skills if not samples.get(sk))
        if mute:
            raise SystemExit(
                "build_guide: %s has topics whose skill yields no bank item at any "
                "level, so their ladders would show nothing real: %s"
                % (exam, ", ".join(mute)))
        for sec_key, sec in secs.items():
            base = OUT / exam / sec_key
            base.mkdir(parents=True, exist_ok=True)
            page = partials.apply_chrome(section_index(index_tpl, exam, sec_key))
            guard(page, "%s/%s index" % (exam, sec_key))
            (base / "index.html").write_text(page)
            written += 1
            ts = sec["topics"]
            for i, t in enumerate(ts):
                out = base / t.slug
                out.mkdir(parents=True, exist_ok=True)
                page = partials.apply_chrome(topic_page(
                    topic_tpl, exam, sec_key, t, samples,
                    ts[i - 1] if i else None, ts[i + 1] if i + 1 < len(ts) else None))
                guard(page, "%s/%s/%s" % (exam, sec_key, t.slug))
                (out / "index.html").write_text(page)
                written += 1
    OUT.mkdir(parents=True, exist_ok=True)
    page = partials.apply_chrome(hub_page(hub_tpl))
    guard(page, "guide hub")
    (OUT / "index.html").write_text(page)
    written += 1
    print("built guide/: %d pages, %d sections, %d topics, %d formulas, %d worked"
          % (written, sum(len(v) for v in SECTIONS.values()),
             all_topics_count(), all_formula_count(), all_worked_count()))


def all_topics(): return [t for v in SECTIONS.values() for s in v.values() for t in s["topics"]]
def all_topics_count(): return len(all_topics())
def all_formula_count(): return sum(len(t.facts) for t in all_topics())
def all_worked_count(): return sum(len(t.worked) for t in all_topics())


def hub_page(tpl):
    """The /guide/ index: every exam, its live sections, and the ones still unwritten.

    Built from the registry rather than hand-written, so it cannot advertise a section
    that does not exist and cannot quietly drop one that does.
    """
    blocks = []
    for exam, e in EXAMS.items():
        cards = []
        for sec_key, sec in SECTIONS.get(exam, {}).items():
            cards.append(
                '<a class="scard" href="/guide/%s/%s/"><span class="scard-t">%s</span>'
                '<span class="scard-i">%s</span>'
                '<span class="scard-m">%d topics &middot; %d %s</span></a>'
                % (esc(exam), esc(sec_key), esc(sec["title"]), esc(sec["blurb"]),
                   len(sec["topics"]), sum(len(t.facts) for t in sec["topics"]),
                   esc(sec.get("facts_word", "formulas"))))
        for title, note in PLANNED.get(exam, []):
            cards.append('<div class="scard soon"><span class="scard-t">%s</span>'
                         '<span class="scard-i">%s</span>'
                         '<span class="scard-m">Being written</span></div>'
                         % (esc(title), esc(note)))
        blocks.append('<section class="ex"><h2>%s</h2><p class="lede">%s</p>'
                      '<div class="sgrid">%s</div></section>'
                      % (esc(e["name"]), esc(e["blurb"]), "".join(cards)))
    cov = coverage.report(SECTIONS["gmat"]["quant"]["topics"])
    note = ("The GMAT quant guide currently covers %d of the %d headings in the "
            "reference syllabus we hold." % (len(cov["covered"]), cov["total"]))
    ld = json.dumps({"@context": "https://schema.org", "@type": "CollectionPage",
                     "name": "Start From Nowhere Study Guides",
                     "description": "Free topic-by-topic study guides for every exam "
                                    "we train.",
                     "publisher": {"@type": "Organization",
                                   "name": "Start From Nowhere"}})
    return (tpl
            .replace("{{SECTIONS}}", str(sum(len(v) for v in SECTIONS.values())))
            .replace("{{TOPICS}}", str(all_topics_count()))
            .replace("{{FORMULAS}}", str(all_formula_count()))
            .replace("{{WORKED}}", str(all_worked_count()))
            .replace("{{BLOCKS}}", "".join(blocks))
            .replace("{{COVERAGE}}", esc(note))
            .replace("{{LD}}", ld))


def guard(page, where):
    """No unresolved placeholder and no dash, the same two checks every page gets."""
    if "{{" in page:
        print("build_guide: unresolved placeholder in %s" % where, file=sys.stderr)
        sys.exit(1)
    if "—" in page or "–" in page:
        print("build_guide: em or en dash in %s" % where, file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
