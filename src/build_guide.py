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
from guide import gmat_quant, gmat_verbal, gmat_di  # noqa: E402
from guide import sat_math, sat_rw                   # noqa: E402
from guide import gre_verbal, gre_quant             # noqa: E402
from guide import lsat_lr, lsat_rc                  # noqa: E402
from guide import act_english, act_math             # noqa: E402
from guide import act_reading, act_science          # noqa: E402
from guide.model import check_all                   # noqa: E402
from guide import coverage                          # noqa: E402

SITE = "https://startfromnowhere.com"
OUT = ROOT / "guide"
EXAMS_JSON = ROOT / "data" / "exams.json"

# Which exam each guide is for, and where its trainer lives.
EXAMS = {
    "gmat": dict(harness="gmat-focus", app="/app/", name="GMAT Focus Edition",
                 short="GMAT",
                 blurb="Three sections, 2 hours 15 minutes, every one of them adaptive. "
                       "The guides below cover what each section actually asks."),
    "sat": dict(harness="sat", app="/sat/app/", name="Digital SAT", short="SAT",
                blurb="Two sections delivered in adaptive modules. The diagnostic below "
                      "covers every skill the exam scores."),
    "gre": dict(harness="gre", app="/gre/app/", name="GRE General Test", short="GRE",
                blurb="Verbal and quantitative reasoning, section adaptive. The "
                      "diagnostic below covers every skill the exam scores."),
    "lsat": dict(harness="lsat", app="/lsat/app/", name="LSAT", short="LSAT",
                 blurb="Logical reasoning and reading comprehension. The diagnostic "
                       "below covers every skill the exam scores."),
    "act": dict(harness="act", app="/act/app/", name="ACT", short="ACT",
                blurb="English, mathematics, reading and science. The diagnostic below "
                      "covers every skill the exam scores."),
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
        "data-insights": dict(
            title="Data Insights", short="Data Insights", topics=gmat_di.TOPICS,
            facts_title="What Each Type Actually Asks",
            facts_word="rules and forms",
            facts_lede="Five question types, and each one has a fixed structure "
                       "underneath it. Almost every trap in this section is an "
                       "invitation to calculate something the question never needed.",
            blurb="Data sufficiency, tables, graphics, multi-source reasoning and "
                  "two-part analysis. The section that did not exist before the Focus "
                  "Edition, and the only one with a calculator."),
    },
    "sat": {
        "reading-writing": dict(
            title="Reading and Writing", short="Reading and Writing",
            topics=sat_rw.TOPICS,
            exam_section="Reading and Writing (two 32-minute modules of 27 questions "
                         "each)",
            facts_title="The Rules and the Method",
            facts_word="rules",
            facts_lede="Every question here has its own short passage, so there is "
                       "nothing to skim and come back to. What replaces a formula is the "
                       "rule or the test that decides the question.",
            blurb="Information and ideas, craft and structure, expression of ideas, and "
                  "standard English conventions: College Board's own four domains. Every "
                  "question carries its own one-paragraph passage, which changes the "
                  "strategy completely."),
        "math": dict(title="Math", short="Math", topics=sat_math.TOPICS,
                     exam_section="Math (two 35-minute modules of 22 questions each)",
                     blurb="Algebra, advanced math, problem solving and data analysis, "
                           "and geometry and trigonometry: College Board's own four "
                           "domains. Desmos is built in and allowed throughout, which "
                           "changes what solving means."),
    },
    "gre": {
        "verbal": dict(
            title="Verbal Reasoning", short="Verbal", topics=gre_verbal.TOPICS,
            exam_section="Verbal Reasoning (two sections)",
            facts_title="The Rules and the Method",
            facts_word="rules",
            facts_lede="Three question types, and each one has a method that works "
                       "whether or not you know every word in it. What replaces a "
                       "formula here is the rule that decides the question.",
            blurb="Text completion, sentence equivalence and reading comprehension. "
                  "Vocabulary is load bearing on this exam in a way it is not on the "
                  "others, and the method is what lets you work when a word is "
                  "unfamiliar."),
        "quant": dict(
            title="Quantitative Reasoning", short="Quant", topics=gre_quant.TOPICS,
            exam_section="Quantitative Reasoning (two sections, 12 + 15 questions)",
            blurb="Arithmetic, algebra, geometry and data analysis, plus quantitative "
                  "comparison, which is a format rather than a content area and is "
                  "where most of the wasted time on this section goes."),
    },
    "lsat": {
        "logical-reasoning": dict(
            title="Logical Reasoning", short="Logical Reasoning", topics=lsat_lr.TOPICS,
            exam_section="Logical Reasoning (scored)",
            facts_title="The Rules and the Method",
            facts_word="rules",
            facts_lede="Conditional logic is explicit and load bearing on this exam in a "
                       "way it is not on the others. What replaces a formula here is the "
                       "rule, the translation, or the test that decides the question.",
            blurb="Argument structure, conditional logic, assumptions, flaws, additional "
                  "evidence, conclusions, principles and parallel reasoning. The "
                  "arguments are tighter than any other exam's and the gap is usually "
                  "one precise logical step."),
        "reading-comprehension": dict(
            title="Reading Comprehension", short="Reading Comprehension",
            topics=lsat_rc.TOPICS,
            exam_section="Reading Comprehension (scored): four sets of five to eight "
                         "questions",
            facts_title="The Rules and the Method",
            facts_word="rules",
            facts_lede="Longer passages than any other exam we cover, so there is "
                       "genuinely something to map and come back to. What replaces a "
                       "formula here is the test that decides each question type.",
            blurb="Main idea, stated information, inference, structure and tone, and "
                  "application. One set per section is Comparative Reading: two "
                  "passages by different authors, asked about together."),
    },
    "act": {
        "english": dict(
            title="English", short="English", topics=act_english.TOPICS,
            exam_section="English (40 of 50 scored)",
            facts_title="The Rules and the Method",
            facts_word="rules",
            facts_lede="Fifty questions in thirty-five minutes is about forty-two "
                       "seconds each, so this section rewards rules you can apply on "
                       "sight rather than reasoning you have to construct.",
            blurb="Conventions of standard English, production of writing, and knowledge "
                  "of language: ACT's own three reporting categories. The tightest "
                  "per-question budget of any section we cover, which is what shapes "
                  "the strategy."),
        "mathematics": dict(
            title="Mathematics", short="Math", topics=act_math.TOPICS,
            exam_section="Mathematics (41 of 45 scored)",
            blurb="Number and quantity, algebra, functions, geometry, statistics and "
                  "probability, and integrating essential skills: ACT's own six "
                  "reporting categories. The broadest maths of any exam here and the "
                  "shallowest per topic, with no formula sheet provided."),
        "reading": dict(
            title="Reading", short="Reading", topics=act_reading.TOPICS,
            exam_section="Reading (27 of 36 scored)",
            facts_title="The Rules and the Method",
            facts_word="rules",
            facts_lede="Four passage sets in forty minutes is about nine minutes each "
                       "including the reading, which is the tightest reading budget of "
                       "any exam here. What replaces a formula is the test that decides "
                       "each question type.",
            blurb="Key ideas and details, craft and structure, and integration of "
                  "knowledge and ideas. One set per section is Paired Passages, two "
                  "texts by different authors asked about together."),
        "science": dict(
            title="Science", short="Science", topics=act_science.TOPICS,
            exam_section="Science, optional, not in the Composite (34 of 40 scored)",
            facts_title="The Rules and the Method",
            facts_word="rules",
            facts_lede="This section is not a test of science knowledge. It is data "
                       "interpretation using scientific material, and what replaces a "
                       "formula is the routine that gets an answer off a figure.",
            blurb="Interpretation of data, scientific investigation, and evaluation of "
                  "arguments and models. Students who try to understand the underlying "
                  "science lose this section on time; students who treat the figures as "
                  "a lookup finish it."),
    },
}

# Sections we have not written yet. The hub lists these as unwritten rather than leaving
# them off, because a guide index that silently omits a third of the exam is the exact
# failure the coverage check exists to prevent, one level up.
PLANNED = {
    "gmat": [],
    "sat": [],
    "gre": [],
    "lsat": [],
    "act": [],
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
    // Plain multiple choice first. Two-part analysis has no plain form at all, so it
    // falls back to its own shape rather than showing nothing: a skill whose ladder has
    // no real item on it looks like a deliberate omission, not a gap.
    const plain = api.BANK.filter(q => q.skill === sk && q.diff === d
                                       && Array.isArray(q.choices) && !q.answerType);
    const alt = api.BANK.filter(q => q.skill === sk && q.diff === d
                                     && (q.answerType === 'tpa' || q.answerType === 'se')
                                     && Array.isArray(q.answer));
    const c = plain.length ? plain : alt;
    if (c.length) {
      const q = c[Math.floor(c.length / 2)];
      out[sk][d] = {stem: q.stem, choices: q.choices, answer: q.answer,
                    columns: q.columns || null, kind: q.answerType || 'mc',
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


def exam_facts(exam, sec_title):
    """The section's own published figures, with the source that states them.

    This file's header has always said data/exams.json is one of its three sources and
    until now it was not read at all, which is the same defect as a check that promises
    more than it performs. The guide states exam facts on its pages, so it states them
    from the record that carries source, year and URL, and shows that citation.
    """
    rows = json.loads(EXAMS_JSON.read_text())
    rec = next((e for e in rows if e.get("slug") == exam), None)
    if rec is None:
        raise SystemExit("build_guide: data/exams.json has no record for %r" % exam)
    # Matched on the record's own section name. The GMAT's are bare ("Math" would be
    # "Quantitative Reasoning"); the SAT's carry parenthetical detail, so its registry
    # entry names the record explicitly rather than this guessing at a prefix.
    sec = next((s for s in rec.get("sections") or []
                if s.get("name") == sec_title), None)
    if sec is None:
        raise SystemExit(
            "build_guide: data/exams.json has no %r section for %s. Sections there: %s"
            % (sec_title, exam, ", ".join(s.get("name", "?")
                                          for s in rec.get("sections") or [])))
    src = rec.get("sections_src") or {}
    for k in ("src", "year", "url"):
        if not src.get(k):
            raise SystemExit("build_guide: %s sections_src is missing %s; a published "
                             "exam figure carries source, year and URL" % (exam, k))
    bits = []
    if sec.get("questions") is not None:
        bits.append(("Questions", str(sec["questions"])))
    if sec.get("minutes") is not None:
        bits.append(("Minutes", str(sec["minutes"])))
    if sec.get("scale"):
        bits.append(("Scored", sec["scale"]))
    return bits, src


def facts_strip_html(bits, src):
    tiles = "".join('<div class="ef"><span class="ef-n">%s</span>'
                    '<span class="ef-l">%s</span></div>' % (esc(v), esc(l))
                    for l, v in bits)
    return ('<div class="efs">%s</div>'
            '<p class="efs-src">Source: %s, %s. '
            '<a href="%s" rel="nofollow noopener" target="_blank">%s</a></p>'
            % (tiles, esc(src["src"]), esc(src["year"]), esc(src["url"]),
               esc(src["url"])))


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
        if item and item.get("kind") == "tpa":
            # Two columns picking from one shared list, which is the whole point of the
            # format, so it is shown as two columns rather than flattened to a list.
            picks = item["answer"]
            head = "".join("<th>%s</th>" % esc(c) for c in item["columns"])
            rows_html = "".join(
                "<tr>%s<td>%s</td></tr>"
                % ("".join('<td>%s</td>'
                           % ("&#10003;" if j < len(picks) and picks[j] == i else "")
                           for j in range(len(item["columns"]))), esc(c))
                for i, c in enumerate(item["choices"]))
            shown = ('<details class="lx"><summary>See a real level %d item '
                     '(%d in the bank)</summary>'
                     '<p class="lx-stem">%s</p>'
                     '<div class="lx-tw"><table class="lx-tpa"><thead><tr>%s<th></th>'
                     '</tr></thead><tbody>%s</tbody></table></div>'
                     '<p class="lx-key">One selection per column, from the shared list.'
                     '</p></details>'
                     % (d, item["n"], esc(item["stem"]), head, rows_html))
        elif item and item.get("kind") == "se":
            # Select two from six, and the pair is the answer: both are marked, and the
            # instruction says so, because one marked choice would read as the key.
            picks = set(item["answer"])
            opts = "".join(
                '<li%s>%s</li>' % (' class="key"' if i in picks else "", esc(c))
                for i, c in enumerate(item["choices"]))
            shown = ('<details class="lx"><summary>See a real level %d item '
                     '(%d in the bank)</summary>'
                     '<p class="lx-stem">%s</p><ol type="A" class="lx-opts">%s</ol>'
                     '<p class="lx-key">Select <b>%d</b>. Both marked choices are '
                     'required; either alone scores nothing.</p></details>'
                     % (d, item["n"], esc(item["stem"]), opts, len(picks)))
        elif item:
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


def diagnostic_items(harness_id):
    """One real item per scored skill, at the middle difficulty.

    Middle difficulty because the job is to separate, and an item everyone gets right
    or everyone gets wrong separates nobody. Deterministic, so the diagnostic is the
    same on every build rather than reshuffling under a student who came back to it.

    Every skill the engine scores appears exactly once. A diagnostic that quietly
    skipped a skill would tell a student they had covered the exam when they had not,
    which is the failure this whole guide is built to avoid.
    """
    js = r"""
const h = require('./exam_harness.js');
const api = h.load(h.byId[process.argv[1]]);
const meta = api.SECTION_META || {};
const skills = api.SKILLS || [];
const out = [];
for (const sk of skills) {
  // Plain multiple choice, plus the two formats that are the ONLY form some skills
  // have: GMAT two-part analysis and GRE sentence equivalence. Excluding them would
  // drop those skills from the diagnostic silently, which is the thing the coverage
  // check below exists to prevent.
  const pool = api.BANK.filter(q => q.skill === sk.id && Array.isArray(q.choices)
                                    && (!q.answerType || q.answerType === 'tpa'
                                        || q.answerType === 'se'));
  if (!pool.length) continue;
  const mid = pool.filter(q => q.diff === 3);
  const c = mid.length ? mid : pool;
  const q = c[Math.floor(c.length / 2)];
  // Both passage fields. RC and CR prose lives in passage; the DI reading types put
  // their tables and their multi-tab material in passageHtml. Naming only one of them
  // is how the trainer once shipped 280 questions with nothing to read (INC-0099).
  out.push({id: q.id, section: q.section, type: q.type,
            sectionName: (meta[q.section] || {}).name || q.section,
            skill: sk.id, skillName: sk.label,
            kind: (q.answerType === 'tpa' || q.answerType === 'se')
                  ? q.answerType : 'mc',
            pick: q.answerType === 'se' && Array.isArray(q.answer)
                  ? q.answer.length : 1,
            passage: q.passage || null, passageHtml: q.passageHtml || null,
            stem: q.stem,
            columns: q.columns || null, choices: q.choices, answer: q.answer});
}
process.stdout.write(JSON.stringify({items: out,
  sections: Object.fromEntries(Object.entries(meta).map(([k, v]) => [k, v.name])),
  skills: skills.map(s => s.id), floor: (api.EXAM.scale || {}).minAttempts || null}));
"""
    r = subprocess.run(["node", "-e", js, harness_id], cwd=str(D),
                       capture_output=True, text=True)
    if r.returncode != 0:
        raise SystemExit("build_guide: could not build the diagnostic.\n"
                         + (r.stderr or "")[-600:])
    return json.loads(r.stdout)


def diagnostic_page(tpl, exam):
    """The diagnostic, with its items and its reading map baked in at build time."""
    e = EXAMS[exam]
    d = diagnostic_items(e["harness"])
    items = d["items"]
    missing = [s for s in d["skills"] if not any(i["skill"] == s for i in items)]
    if missing:
        raise SystemExit("build_guide: the %s diagnostic covers no item for %d of its "
                         "skills, so it would report on a smaller exam than the real "
                         "one: %s" % (exam, len(missing), ", ".join(missing)))
    # An item whose TYPE asks about source material has to be carrying some. Derived
    # from the type, never from whether a field happens to be populated, because a check
    # that reads the same field it is checking cannot fail on that field being absent.
    READS = {"RC", "R", "MSR", "GT", "GI", "TA"}
    mute = [i for i in items if i.get("type") in READS
            and not (i.get("passage") or i.get("passageHtml"))]
    if mute:
        raise SystemExit(
            "build_guide: the %s diagnostic would ask about material it does not show. "
            "These items are types that read from a source and carry none: %s"
            % (exam, ", ".join("%s (%s, type %s)" % (i["id"], i["skillName"], i["type"])
                               for i in mute)))
    if not d.get("floor"):
        raise SystemExit("build_guide: %s exposes no scale.minAttempts, so the "
                         "diagnostic cannot state the evidence floor it is below"
                         % e["harness"])

    # skill -> the guide pages that teach it, which is what a wrong answer points at.
    by_skill = {}
    for sec_key, sec in SECTIONS.get(exam, {}).items():
        for t in sec["topics"]:
            by_skill.setdefault(t.skill, []).append(
                {"title": t.title, "url": "/guide/%s/%s/%s/" % (exam, sec_key, t.slug)})

    data = json.dumps({"items": items, "sections": d["sections"], "topics": by_skill},
                      ensure_ascii=False)
    if "</script" in data:
        raise SystemExit("build_guide: diagnostic data would close its own script tag")
    mins = max(5, round(len(items) * 1.5))
    return (tpl
            .replace("{{EXAM_SHORT}}", esc(e["short"]))
            .replace("{{EXAM}}", esc(exam))
            .replace("{{N}}", str(len(items)))
            .replace("{{MINS}}", str(mins))
            .replace("{{FLOOR}}", str(d["floor"]))
            .replace("{{APP}}", esc(e["app"]))
            .replace("{{DATA}}", data)), len(items)


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
            .replace("{{EXAM_FACTS}}", facts_strip_html(
                *exam_facts(exam, sec.get("exam_section", sec["title"]))))
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
    diag_tpl = (D / "guide_diagnostic_template.html").read_text()
    written = 0
    diag_counts = {}
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
        diag = OUT / exam / "diagnostic"
        diag.mkdir(parents=True, exist_ok=True)
        page, n_diag = diagnostic_page(diag_tpl, exam)
        diag_counts[exam] = n_diag
        page = partials.apply_chrome(page)
        guard(page, "%s diagnostic" % exam)
        (diag / "index.html").write_text(page)
        written += 1
    OUT.mkdir(parents=True, exist_ok=True)
    page = partials.apply_chrome(hub_page(hub_tpl, diag_counts))
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


def hub_page(tpl, diag_counts):
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
        cards.insert(0,
            '<a class="scard" href="/guide/%s/diagnostic/">'
            '<span class="scard-t">Diagnostic</span>'
            '<span class="scard-i">One question from every skill the %s scores, then a '
            'list of what to work on first. Not a score and not a prediction.</span>'
            '<span class="scard-m">%d questions</span></a>'
            % (esc(exam), esc(e["short"]), diag_counts[exam]))
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
