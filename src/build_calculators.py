"""Builds the score calculators under /exams/<exam>/.

    /exams/act/score-calculator/   the ACT Composite and superscore, with national ranks

A calculator is only as honest as its rule. Each one here does arithmetic that the test
maker publishes and nothing else: no score conversion, estimate or percentile that the
maker does not print. Every rule and every rank on the page is read from data that
carries its source, year and URL, and the page cites them where they are used
(GROWTH.md, what brings people back).
"""
import datetime
import html
import json
import os
import pathlib
import sys

D = pathlib.Path(__file__).parent
ROOT = D.parent
sys.path.insert(0, str(D))
import partials

SITE = "https://startfromnowhere.com"
ACT_RANKS = ROOT / "data" / "act_national_ranks.json"
# The columns the page prints, in order. STEM is in the data too, but the page does not
# calculate a STEM score, so it does not print ranks for one.
RANK_COLS = ("composite", "english", "math", "reading", "science")


def esc(s):
    return html.escape(str(s), quote=True)


def fail(msg):
    print("build_calculators: " + msg, file=sys.stderr)
    sys.exit(1)


def check_ranks(d):
    """The national ranks, checked before anything is rendered from them.

    The table is parsed from ACT's PDF by a script, never typed. This keeps it honest
    afterwards: ACT as the source with a URL on act.org, the cohort and window it
    describes, a rank for every score from 1 to 36 in each printed column, never rising
    as the score falls, and a mean and standard deviation for each.
    """
    bad = []
    if d.get("src") != "ACT" or not str(d.get("url", "")).startswith("https://www.act.org/"):
        bad.append("the source must be ACT, with a URL on act.org")
    if not isinstance(d.get("year"), int):
        bad.append("no year")
    for k in ("cohort", "window", "reporting_year"):
        if not d.get(k):
            bad.append("no " + k)
    for col in RANK_COLS:
        c = (d.get("ranks") or {}).get(col) or {}
        at = c.get("at_or_below") or {}
        vals = [at.get(str(s)) for s in range(36, 0, -1)]
        if any(v is None for v in vals):
            bad.append("%s is missing a rank for some score from 1 to 36" % col)
            continue
        if any(not 1 <= v <= 100 for v in vals) or vals != sorted(vals, reverse=True):
            bad.append("%s ranks must fall from 100 toward 1 as the score falls" % col)
        if not all(isinstance(c.get(k), (int, float)) for k in ("mean", "sd")):
            bad.append("%s has no mean or standard deviation" % col)
    if bad:
        fail("data/act_national_ranks.json: " + "; ".join(bad))


def cite(label, f):
    """A citation from a record that carries src, year and url, all three required."""
    if not all(f.get(k) for k in ("src", "year", "url")):
        fail("a citation for %r lacks its source, year or URL" % label)
    return ('<a href="%s" rel="noopener" target="_blank">%s</a> (%s, %s)'
            % (esc(f["url"]), esc(label), esc(f["src"]), esc(f["year"])))


def act_fact(act, start):
    """The ACT key fact that begins with `start`. The page words its claims from these, so
    a fact reworded or removed in exams.json fails the build rather than leaving the page
    citing something that no longer says it."""
    for f in act.get("key_facts") or []:
        if f.get("text", "").startswith(start):
            return f
    fail("the ACT calculator cites the key fact beginning %r, and data/exams.json no "
         "longer has it" % start)


def long_date(iso):
    t = datetime.date.fromisoformat(iso)
    return "%s %d, %d" % (t.strftime("%B"), t.day, t.year)


def act_page(act, d, today):
    comp = d["ranks"]["composite"]
    at = comp["at_or_below"]
    cohort, window, ryear = d["cohort"], d["window"], d["reporting_year"]
    rule = act["score_scale"]
    sup = act_fact(act, "The superscore is calculated automatically")
    act_fact(act, "The Composite is the average of the English, math and reading scores")
    ranks_src = {"src": d["src"], "year": d["year"], "url": d["url"]}
    rule_cite = cite("Understanding your ACT scores", rule)
    sup_cite = cite("ACT superscore FAQs", sup)
    rank_cite = cite("ACT score national ranks, %s" % ryear, ranks_src)
    sections_cite = cite("ACT test day", act["sections_src"])

    rows = []
    for s in range(36, 0, -1):
        rows.append("<tr><td>%d</td>%s</tr>" % (s, "".join(
            "<td>%d</td>" % d["ranks"][c]["at_or_below"][str(s)] for c in RANK_COLS)))
    for label, key in (("Mean", "mean"), ("Standard deviation", "sd")):
        rows.append('<tr class="foot"><td>%s</td>%s</tr>' % (label, "".join(
            "<td>%.1f</td>" % d["ranks"][c][key] for c in RANK_COLS)))

    r24 = at["24"]
    faq = [
        ("How Is the ACT Composite Score Calculated?",
         "ACT averages your English, math and reading scale scores and rounds to the "
         "nearest whole number, fractions below one-half down and one-half or more up. "
         "Science and the optional writing test are not part of it.", rule_cite),
        ("Does Science Count Toward the ACT Composite?",
         "No. ACT removed science from the Composite for national online testing in April "
         "2025 and for all testing modes in September 2025. Students who take science also "
         "receive a STEM score, the average of math and science.", rule_cite),
        ("What Is an ACT Superscore?",
         "The average of your best English, math and reading scores across your test "
         "dates, rounded the same way as the Composite. ACT calculates it automatically "
         "once you have tested more than once since September 2016. Science and writing "
         "are not part of it, and ACT advises checking each school's own score policy.",
         sup_cite),
        ("What Percentile Is a 24 on the ACT?",
         "%d percent of %s scored a Composite of 24 or lower, on ACT's national ranks for "
         "tests taken %s." % (r24, cohort, window), rank_cite),
        ("What Is the Average ACT Score?",
         "The mean Composite among %s is %.1f, with a standard deviation of %.1f, on ACT's "
         "national ranks for %s." % (cohort, comp["mean"], comp["sd"], ryear), rank_cite),
    ]
    faq_html = "\n".join('<h3>%s</h3><p>%s</p><p class="src">Source: %s.</p>'
                         % (esc(q), esc(a), c) for q, a, c in faq)
    faq_ld = json.dumps({
        "@context": "https://schema.org", "@type": "FAQPage",
        "mainEntity": [{"@type": "Question", "name": q,
                        "acceptedAnswer": {"@type": "Answer", "text": a}}
                       for q, a, _ in faq]}, separators=(",", ":"))
    science = ("Science is optional and is not part of the Composite: ACT removed it for "
               "national online testing in April 2025 and for all testing modes in "
               "September 2025. If you take it you also receive a STEM score, the average "
               "of math and science. The optional writing test is scored 2 to 12 and does "
               "not affect the Composite either.")
    ranks_js = json.dumps({"at_or_below": at, "cohort": cohort, "year": ryear},
                          separators=(",", ":"))

    tpl = (D / "act_calculator.html").read_text()
    page = (tpl.replace("{{FAQ_LD}}", faq_ld)
               .replace("{{FAQ_HTML}}", faq_html)
               .replace("{{RANK_ROWS}}", "\n".join(rows))
               .replace("{{RANKS_JSON}}", ranks_js)
               .replace("{{RULE_CITE}}", rule_cite)
               .replace("{{SUPER_CITE}}", sup_cite)
               .replace("{{RANK_CITE}}", rank_cite)
               .replace("{{SECTIONS_CITE}}", sections_cite)
               .replace("{{SCIENCE_NOTE}}", esc(science))
               .replace("{{COHORT}}", esc(cohort))
               .replace("{{WINDOW}}", esc(window))
               .replace("{{REPORTING_YEAR}}", esc(ryear))
               .replace("{{READ}}", long_date(d["read"])))
    return partials.apply_chrome(page)


def main():
    today = os.environ.get("BLOG_BUILD_DATE") or datetime.date.today().isoformat()
    exams = json.loads((ROOT / "data" / "exams.json").read_text())
    act = next((e for e in exams if e["slug"] == "act"), None)
    if act is None:
        fail("data/exams.json has no ACT entry to build the ACT calculator from")
    d = json.loads(ACT_RANKS.read_text())
    check_ranks(d)
    page = act_page(act, d, today)
    if "{{" in page:
        fail("unresolved placeholder in the ACT calculator")
    if "—" in page or "–" in page:
        fail("em or en dash in the ACT calculator")
    out = ROOT / "exams" / "act" / "score-calculator"
    out.mkdir(parents=True, exist_ok=True)
    (out / "index.html").write_text(page)
    print("built exams/act/score-calculator/")


if __name__ == "__main__":
    main()
