"""Builds the score calculators under /exams/<exam>/.

    /exams/act/score-calculator/   the ACT Composite and superscore, with national ranks
    /exams/gre/score-calculator/   GRE percentile ranks for Verbal, Quant and Writing
    /exams/sat/score-calculator/   the SAT total and College Board's two percentile groups
    /exams/sat/psat-calculator/    the PSAT/NMSQT total, NMSC Selection Index and percentiles
    /exams/lsat/percentile-calculator/   LSAC's LSAT percentiles, looked up either way

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
import re
import sys

D = pathlib.Path(__file__).parent
ROOT = D.parent
sys.path.insert(0, str(D))
import partials

SITE = "https://startfromnowhere.com"
ACT_RANKS = ROOT / "data" / "act_national_ranks.json"
GRE_RANKS = ROOT / "data" / "gre_percentiles.json"
SAT_RANKS = ROOT / "data" / "sat_percentiles.json"
PSAT_RANKS = ROOT / "data" / "psat_percentiles.json"
LSAT_RANKS = ROOT / "data" / "lsat_percentiles.json"
LSAT_SCORES = [str(x) for x in range(180, 119, -1)]
PSAT_TOTALS = [str(x) for x in range(1520, 319, -10)]
PSAT_SECTIONS = [str(x) for x in range(760, 159, -10)]
SAT_TOTALS = [str(x) for x in range(1600, 399, -10)]
SAT_SECTIONS = [str(x) for x in range(800, 199, -10)]
# College Board prints a whole-number percentile, or 99+ and 1- at the ends of the scale.
SAT_CELL = re.compile(r"^(99\+|1-|[1-9]\d?)$")
GRE_SCORES = [str(x) for x in range(170, 129, -1)]
GRE_WRITING = ["6.0", "5.5", "5.0", "4.5", "4.0", "3.5", "3.0", "2.5", "2.0", "1.5", "1.0",
               "0.5", "0.0"]
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


def check_gre(d):
    """ETS's percentile ranks, checked before anything is rendered from them.

    Parsed from ETS's PDF by a script. ETS leaves a cell blank where no test taker scored
    beyond it, and the text layer drops those cells, so a blank must sit only below the
    last reported score; a blank in the middle would mean the columns were misaligned.
    """
    bad = []
    if d.get("src") != "ETS" or not str(d.get("url", "")).startswith("https://www.ets.org/"):
        bad.append("the source must be ETS, with a URL on ets.org")
    for k in ("window", "read", "note_blank"):
        if not d.get(k):
            bad.append("no " + k)
    for col, keys in (("verbal", GRE_SCORES), ("quant", GRE_SCORES), ("writing", GRE_WRITING)):
        c = d.get(col) or {}
        if sorted(c) != sorted(keys):
            bad.append("%s does not have one entry per score" % col)
            continue
        vals = [c[k] for k in keys]
        first_blank = next((i for i, v in enumerate(vals) if v is None), len(vals))
        shown = vals[:first_blank]
        if any(v is not None for v in vals[first_blank:]):
            bad.append("%s has a blank above a reported score" % col)
        if not shown or any(not 0 <= v <= 100 for v in shown) or shown != sorted(shown, reverse=True):
            bad.append("%s ranks must fall as the score falls" % col)
    for m in ("verbal", "quant", "writing"):
        st = (d.get("stats") or {}).get(m) or {}
        if not all(st.get(k) is not None for k in ("takers", "mean", "sd")):
            bad.append("no mean, standard deviation or count for %s" % m)
    if bad:
        fail("data/gre_percentiles.json: " + "; ".join(bad))


def gre_page(gre, d):
    rank_src = {"src": d["src"], "year": d["year"], "url": d["url"]}
    rank_cite = cite("GRE General Test Interpretive Data, Tables 1A to 1C", rank_src)
    scale = gre["score_scale"]
    scale_cite = cite("How the GRE General Test is scored", scale)
    window, st = d["window"], d["stats"]

    def cell(v):
        return "<td>%d</td>" % v if v is not None else '<td class="nr">not reported</td>'
    vq = "\n".join("<tr><td>%s</td>%s%s</tr>" % (k, cell(d["verbal"][k]), cell(d["quant"][k]))
                   for k in GRE_SCORES)
    aw = "\n".join("<tr><td>%s</td>%s</tr>" % (k, cell(d["writing"][k])) for k in GRE_WRITING)
    opts = "".join('<option value="%s">%s</option>' % (k, k) for k in GRE_WRITING)
    stats = ("In the same period the mean Verbal Reasoning score was %.2f (standard deviation "
             "%.2f) across %s test takers, the mean Quantitative Reasoning score %.2f (%.2f) "
             "across %s, and the mean Analytical Writing score %.2f (%.2f) across %s."
             % (st["verbal"]["mean"], st["verbal"]["sd"], st["verbal"]["takers"],
                st["quant"]["mean"], st["quant"]["sd"], st["quant"]["takers"],
                st["writing"]["mean"], st["writing"]["sd"], st["writing"]["takers"]))
    v160, q160 = d["verbal"]["160"], d["quant"]["160"]
    faq = [
        ("Does ETS Report a Total GRE Score?",
         "No. ETS reports three scores: Verbal Reasoning and Quantitative Reasoning, each 130 "
         "to 170 in 1-point increments, and Analytical Writing, 0 to 6 in half-point "
         "increments. Adding Verbal and Quantitative gives a figure between 260 and 340, but "
         "ETS does not report that sum and publishes no percentile for it.", scale_cite),
        ("What Percentile Is a 160 on the GRE?",
         "%d percent of test takers scored lower than 160 in Verbal Reasoning, and %d percent "
         "in Quantitative Reasoning, among everyone who tested between %s."
         % (v160, q160, window), rank_cite),
        ("What Is the Average GRE Score?",
         "Among everyone who tested between %s, the mean was %.2f in Verbal Reasoning, %.2f in "
         "Quantitative Reasoning and %.2f in Analytical Writing."
         % (window, st["verbal"]["mean"], st["quant"]["mean"], st["writing"]["mean"]),
         rank_cite),
        ("Why Is the Same Score a Different Percentile in Verbal and Quant?",
         "Each measure has its own distribution. The Quantitative Reasoning mean is %.2f "
         "against %.2f for Verbal Reasoning, so a 160 is ahead of %d percent of test takers in "
         "Verbal but %d percent in Quant."
         % (st["quant"]["mean"], st["verbal"]["mean"], v160, q160), rank_cite),
    ]
    faq_html = "\n".join('<h3>%s</h3><p>%s</p><p class="src">Source: %s.</p>'
                         % (esc(q), esc(a), c) for q, a, c in faq)
    faq_ld = json.dumps({"@context": "https://schema.org", "@type": "FAQPage",
                         "mainEntity": [{"@type": "Question", "name": q,
                                         "acceptedAnswer": {"@type": "Answer", "text": a}}
                                        for q, a, _ in faq]}, separators=(",", ":"))
    text = scale["text"]
    blank = ("Where a cell says not reported, ETS gives no percentile, because no test taker "
             "scored beyond that score.")
    ranks = json.dumps({k: d[k] for k in ("verbal", "quant", "writing")}, separators=(",", ":"))
    page = ((D / "gre_calculator.html").read_text()
            .replace("{{FAQ_LD}}", faq_ld).replace("{{FAQ_HTML}}", faq_html)
            .replace("{{VQ_ROWS}}", vq).replace("{{AW_ROWS}}", aw)
            .replace("{{AW_OPTIONS}}", opts)
            .replace("{{STATS_TEXT}}", esc(stats))
            .replace("{{SCALE_TEXT}}", esc(text[0].upper() + text[1:] + "."))
            .replace("{{SCALE_CITE}}", scale_cite).replace("{{RANK_CITE}}", rank_cite)
            .replace("{{BLANK_NOTE}}", esc(blank))
            .replace("{{RANKS_JSON}}", ranks)
            .replace("{{WINDOW}}", esc(window)).replace("{{READ}}", long_date(d["read"])))
    return partials.apply_chrome(page)


def sat_order(v):
    """A printed percentile as a number that sorts: 99+ above 99, 1- below 1."""
    return 99.5 if v == "99+" else 0.5 if v == "1-" else int(v)


def check_sat(d):
    """College Board's SAT percentiles, checked before anything is rendered from them.

    Parsed from the research page by a script, never typed. Every score College Board
    lists must be there in each group, in the form it prints, never rising as the score
    falls; the definitions quoted on the page and the two citations must be present.
    """
    bad = []
    if d.get("src") != "College Board" or not str(d.get("url", "")).startswith(
            "https://research.collegeboard.org/"):
        bad.append("the source must be College Board, with a URL on research.collegeboard.org")
    for k in ("year", "read", "modified", "title"):
        if not d.get(k):
            bad.append("no " + k)
    if sorted((d.get("definitions") or {})) != ["national", "rank", "user"]:
        bad.append("the three definitions the page prints must be quoted")
    for part, keys in (("total", SAT_TOTALS), ("rw", SAT_SECTIONS), ("math", SAT_SECTIONS)):
        for grp in ("national", "user"):
            c = (d.get(part) or {}).get(grp) or {}
            if list(c) != keys:
                bad.append("%s %s does not list every score in order" % (part, grp))
                continue
            vals = [c[k] for k in keys]
            if not all(isinstance(v, str) and SAT_CELL.match(v) for v in vals):
                bad.append("%s %s has a cell College Board would not print" % (part, grp))
            elif [sat_order(v) for v in vals] != sorted((sat_order(v) for v in vals), reverse=True):
                bad.append("%s %s percentiles must fall as the score falls" % (part, grp))
    for k in ("sum_rule", "all_tester"):
        f = d.get(k) or {}
        if not all(f.get(x) for x in ("text", "src", "year", "url", "title")) or \
                not f["url"].startswith("https://satsuite.collegeboard.org/"):
            bad.append("%s needs its text, title, source, year and a satsuite.collegeboard.org URL" % k)
    if bad:
        fail("data/sat_percentiles.json: " + "; ".join(bad))


def ordinal(n):
    n = int(n)
    suf = "th" if 10 <= n % 100 <= 20 else {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th")
    return "%d%s" % (n, suf)


def sat_page(d):
    rank_src = {"src": d["src"], "year": d["year"], "url": d["url"]}
    rank_cite = cite(d["title"], rank_src)
    sum_cite = cite(d["sum_rule"]["title"], d["sum_rule"])
    tester_cite = cite(d["all_tester"]["title"], d["all_tester"])
    tot, rw, math = d["total"], d["rw"], d["math"]
    defs = d["definitions"]

    total_rows = "\n".join("<tr><td>%s</td><td>%s</td><td>%s</td></tr>"
                            % (k, esc(tot["national"][k]), esc(tot["user"][k])) for k in SAT_TOTALS)
    def section_rows(t):
        return "\n".join("<tr><td>%s</td><td>%s</td><td>%s</td></tr>"
                         % (k, esc(t["national"][k]), esc(t["user"][k])) for k in SAT_SECTIONS)
    hi = sum(1 for k in SAT_TOTALS if sat_order(tot["national"][k]) > sat_order(tot["user"][k]))
    lo = sum(1 for k in SAT_TOTALS if sat_order(tot["national"][k]) < sat_order(tot["user"][k]))
    eq = len(SAT_TOTALS) - hi - lo
    compare = ("Neither group always gives the higher figure. Of the %d totals College Board "
               "lists, the nationally representative percentile is the higher at %d, the user "
               "group percentile at %d, and the two match at %d. At a total of 1200 they are %s "
               "and %s; at 800 they are %s and %s."
               % (len(SAT_TOTALS), hi, lo, eq, tot["national"]["1200"], tot["user"]["1200"],
                  tot["national"]["800"], tot["user"]["800"]))

    def at(score):
        n, u = tot["national"][score], tot["user"][score]
        if not (n.isdigit() and u.isdigit()):
            fail("the SAT FAQ quotes the percentiles for %s, which are no longer whole numbers" % score)
        return ("On College Board's tables a total of %s is at the %s nationally representative "
                "percentile and the %s user group percentile: %s percent of the nationally "
                "representative group, and %s percent of the user group, scored at or below it."
                % (score, ordinal(n), ordinal(u), n, u))
    faq = [
        ("How Is the SAT Total Score Calculated?", d["sum_rule"]["text"] + ".", sum_cite),
        ("What Percentile Is a 1200 on the SAT?", at("1200"), rank_cite),
        ("What Percentile Is a 1400 on the SAT?", at("1400"), rank_cite),
        ("What Percentile Is a 1000 on the SAT?", at("1000"), rank_cite),
        ("What Is the Difference Between the Two SAT Percentiles?",
         'College Board describes them this way: "%s" And: "%s"' % (defs["national"], defs["user"]),
         rank_cite),
        ("Is the Percentile on My Score Report One of These?",
         'Your score report shows an All Tester Percentile, which College Board\'s guide to '
         'fall 2026 scores describes this way: "%s"' % d["all_tester"]["text"] +
         " College Board does not say that it is the same table as the user group "
         "percentiles on its research site, so the figure on your own report is the one that "
         "describes you.", tester_cite),
    ]
    faq_html = "\n".join('<h3>%s</h3><p>%s</p><p class="src">Source: %s.</p>'
                         % (esc(q), esc(a), c) for q, a, c in faq)
    faq_ld = json.dumps({"@context": "https://schema.org", "@type": "FAQPage",
                         "mainEntity": [{"@type": "Question", "name": q,
                                         "acceptedAnswer": {"@type": "Answer", "text": a}}
                                        for q, a, _ in faq]}, separators=(",", ":"))
    ranks = json.dumps({k: d[k] for k in ("total", "rw", "math")}, separators=(",", ":"))
    page = ((D / "sat_calculator.html").read_text()
            .replace("{{FAQ_LD}}", faq_ld).replace("{{FAQ_HTML}}", faq_html)
            .replace("{{TOTAL_ROWS}}", total_rows)
            .replace("{{RW_ROWS}}", section_rows(rw)).replace("{{MATH_ROWS}}", section_rows(math))
            .replace("{{RANKS_JSON}}", ranks)
            .replace("{{RANK_CITE}}", rank_cite).replace("{{SUM_CITE}}", sum_cite)
            .replace("{{TESTER_CITE}}", tester_cite)
            .replace("{{SUM_TEXT}}", esc(d["sum_rule"]["text"]))
            .replace("{{DEF_RANK}}", esc(defs["rank"]))
            .replace("{{DEF_NATIONAL}}", esc(defs["national"]))
            .replace("{{DEF_USER}}", esc(defs["user"]))
            .replace("{{ALL_TESTER}}", esc(d["all_tester"]["text"]))
            .replace("{{GROUP_COMPARE}}", esc(compare))
            .replace("{{READ}}", long_date(d["read"]))
            .replace("{{MODIFIED}}", long_date(d["modified"])))
    return partials.apply_chrome(page)


def check_psat(d):
    """College Board's PSAT/NMSQT percentiles, rules and benchmarks, checked like the SAT's,
    for each of the two grades the page prints."""
    bad = []
    if d.get("src") != "College Board" or not str(d.get("url", "")).startswith(
            "https://research.collegeboard.org/"):
        bad.append("the source must be College Board, with a URL on research.collegeboard.org")
    for k in ("year", "read", "modified", "title"):
        if not d.get(k):
            bad.append("no " + k)
    if sorted((d.get("definitions") or {})) != ["national", "rank", "user"]:
        bad.append("the three definitions the page prints must be quoted")
    for part, keys in (("total", PSAT_TOTALS), ("rw", PSAT_SECTIONS), ("math", PSAT_SECTIONS)):
        for grade in ("10", "11"):
            for grp in ("national", "user"):
                c = ((d.get(part) or {}).get(grade) or {}).get(grp) or {}
                if list(c) != keys:
                    bad.append("%s grade %s %s does not list every score in order" % (part, grade, grp))
                    continue
                vals = [c[k] for k in keys]
                if not all(isinstance(v, str) and SAT_CELL.match(v) for v in vals):
                    bad.append("%s grade %s %s has a cell College Board would not print" % (part, grade, grp))
                elif [sat_order(v) for v in vals] != sorted((sat_order(v) for v in vals), reverse=True):
                    bad.append("%s grade %s %s percentiles must fall as the score falls" % (part, grade, grp))
    b = d.get("benchmarks") or {}
    for sec in ("rw", "math"):
        for grade in ("10", "11"):
            v = (b.get(sec) or {}).get(grade)
            if not isinstance(v, int) or str(v) not in PSAT_SECTIONS:
                bad.append("no %s benchmark on the section scale for grade %s" % (sec, grade))
    for k in ("ranges", "selection_index", "all_tester", "benchmarks", "common_scale"):
        f = d.get(k) or {}
        if not all(f.get(x) for x in ("text", "src", "year", "url", "title")) or \
                not f["url"].startswith("https://satsuite.collegeboard.org/"):
            bad.append("%s needs its text, title, source, year and a satsuite.collegeboard.org URL" % k)
    if sorted(d.get("rw_heading") or {}) != ["10", "11"]:
        bad.append("the reading section's column heading must be recorded for each grade")
    if bad:
        fail("data/psat_percentiles.json: " + "; ".join(bad))


def psat_page(d):
    rank_cite = cite(d["title"], {"src": d["src"], "year": d["year"], "url": d["url"]})
    guide_cite = cite(d["ranges"]["title"], d["ranges"])
    scores_cite = cite(d["selection_index"]["title"], d["selection_index"])
    sat_guide_cite = cite(d["common_scale"]["title"], d["common_scale"])
    tot, rw, math, defs, bench = d["total"], d["rw"], d["math"], d["definitions"], d["benchmarks"]

    def rows(t, grade):
        keys = PSAT_TOTALS if t is tot else PSAT_SECTIONS
        return "\n".join("<tr><td>%s</td><td>%s</td><td>%s</td></tr>"
                         % (k, esc(t[grade]["national"][k]), esc(t[grade]["user"][k])) for k in keys)

    def tally(grade):
        n, u = tot[grade]["national"], tot[grade]["user"]
        hi = sum(1 for k in PSAT_TOTALS if sat_order(n[k]) > sat_order(u[k]))
        lo = sum(1 for k in PSAT_TOTALS if sat_order(n[k]) < sat_order(u[k]))
        return hi, lo, len(PSAT_TOTALS) - hi - lo
    h10, l10, e10 = tally("10")
    h11, l11, e11 = tally("11")
    compare = ("Neither group always gives the higher figure. Of the %d totals College Board lists, "
               "the nationally representative percentile is the higher at %d for 10th graders and "
               "%d for 11th graders, the user group percentile at %d and %d, and the two match at "
               "%d and %d. For an 11th grader, a total of 1200 is at %s and %s."
               % (len(PSAT_TOTALS), h10, h11, l10, l11, e10, e11,
                  tot["11"]["national"]["1200"], tot["11"]["user"]["1200"]))
    heads = d["rw_heading"]
    heading_note = ('College Board\'s percentile page heads the reading section\'s columns "%s" in '
                    'its 10th grade table and "%s" in its 11th grade table. This page calls the '
                    'section Reading and Writing, as College Board\'s fall 2026 score guide does.'
                    % (heads["10"], heads["11"]))
    bench_text = ("Reading and Writing %d in 10th grade and %d in 11th, and Math %d in 10th grade "
                  "and %d in 11th" % (bench["rw"]["10"], bench["rw"]["11"],
                                      bench["math"]["10"], bench["math"]["11"]))

    def at(score):
        vals = [tot[g][grp][score] for g in ("10", "11") for grp in ("national", "user")]
        if not all(v.isdigit() for v in vals):
            fail("the PSAT/NMSQT FAQ quotes the percentiles for %s, which are no longer whole numbers" % score)
        return ("On College Board's tables a total of %s is at the %s nationally representative "
                "percentile and the %s user group percentile for 10th graders, and at the %s and "
                "the %s for 11th graders." % (score, ordinal(vals[0]), ordinal(vals[1]),
                                              ordinal(vals[2]), ordinal(vals[3])))
    faq = [
        ("How Is the PSAT/NMSQT Selection Index Calculated?",
         'College Board describes it this way: "%s" It runs from 48 to 228, and College Board '
         "lists it for the PSAT/NMSQT only." % d["selection_index"]["text"], scores_cite),
        ("How Is the PSAT/NMSQT Total Score Calculated?", d["ranges"]["text"] + ".", guide_cite),
        ("What Percentile Is a 1200 on the PSAT/NMSQT?", at("1200"), rank_cite),
        ("What Percentile Is a 1000 on the PSAT/NMSQT?", at("1000"), rank_cite),
        ("What Are the PSAT/NMSQT Benchmarks?",
         "College Board's grade-level benchmarks are %s. %s" % (bench_text, bench["text"]), guide_cite),
        ("Does This Page Estimate National Merit Cutoffs?",
         "No. It works out the Selection Index as College Board describes it and shows College "
         "Board's percentiles and benchmarks. It does not estimate any National Merit cutoff.",
         None),
    ]
    # The last answer is about this page, so it cites nothing.
    faq_html = "\n".join('<h3>%s</h3><p>%s</p>%s' % (esc(q), esc(a), '<p class="src">Source: %s.</p>' % c if c else "")
                         for q, a, c in faq)
    faq_ld = json.dumps({"@context": "https://schema.org", "@type": "FAQPage",
                         "mainEntity": [{"@type": "Question", "name": q,
                                         "acceptedAnswer": {"@type": "Answer", "text": a}}
                                        for q, a, _ in faq]}, separators=(",", ":"))
    ranks = json.dumps({"total": tot, "rw": rw, "math": math,
                        "bench": {"rw": bench["rw"], "math": bench["math"]}}, separators=(",", ":"))
    page = ((D / "psat_calculator.html").read_text()
            .replace("{{FAQ_LD}}", faq_ld).replace("{{FAQ_HTML}}", faq_html)
            .replace("{{TOT10}}", rows(tot, "10")).replace("{{TOT11}}", rows(tot, "11"))
            .replace("{{RW10}}", rows(rw, "10")).replace("{{RW11}}", rows(rw, "11"))
            .replace("{{M10}}", rows(math, "10")).replace("{{M11}}", rows(math, "11"))
            .replace("{{RANKS_JSON}}", ranks)
            .replace("{{RANK_CITE}}", rank_cite).replace("{{GUIDE_CITE}}", guide_cite)
            .replace("{{SCORES_CITE}}", scores_cite).replace("{{SAT_GUIDE_CITE}}", sat_guide_cite)
            .replace("{{RANGES_TEXT}}", esc(d["ranges"]["text"]))
            .replace("{{SI_RULE}}", esc(d["selection_index"]["text"]))
            .replace("{{COMMON_SCALE}}", esc(d["common_scale"]["text"]))
            .replace("{{BENCH_TEXT}}", esc(bench_text)).replace("{{BENCH_RULE}}", esc(bench["text"]))
            .replace("{{DEF_RANK}}", esc(defs["rank"]))
            .replace("{{DEF_NATIONAL}}", esc(defs["national"]))
            .replace("{{DEF_USER}}", esc(defs["user"]))
            .replace("{{ALL_TESTER}}", esc(d["all_tester"]["text"]))
            .replace("{{GROUP_COMPARE}}", esc(compare))
            .replace("{{HEADING_NOTE}}", esc(heading_note))
            .replace("{{READ}}", long_date(d["read"]))
            .replace("{{MODIFIED}}", long_date(d["modified"])))
    return partials.apply_chrome(page)


def check_lsat(d):
    """LSAC's LSAT percentiles, checked before anything is rendered from them.

    Parsed from LSAC's Data Library by a script, never typed: every score from 180 to 120,
    each in the three precisions LSAC prints, the three agreeing with each other, never
    rising as the score falls, and the testing years and quoted sentences present."""
    bad = []
    if d.get("src") != "LSAC" or not str(d.get("url", "")).startswith("https://www.lsac.org/"):
        bad.append("the source must be LSAC, with a URL on lsac.org")
    for k in ("year", "read", "title", "definition"):
        if not d.get(k):
            bad.append("no " + k)
    if len(d.get("window") or []) != 3:
        bad.append("the three testing years the table covers must be recorded")
    r = d.get("ranks") or {}
    if list(r) != LSAT_SCORES:
        bad.append("the table does not list every score from 180 down to 120")
    else:
        h = [float(r[k]["hundredths"]) for k in LSAT_SCORES]
        if h != sorted(h, reverse=True) or not (0 <= min(h) and max(h) < 100):
            bad.append("percentiles must fall as the score falls, and stay under 100")
        # Each column rounds the same underlying figure, so tenths sit within 0.055 of the
        # hundredths and whole numbers within 0.505; LSAC's whole-number column stops at 99,
        # so 99.5 and above print as 99. A wider gap means the columns were misread.
        for k in LSAT_SCORES:
            x, w = float(r[k]["hundredths"]), float(r[k]["whole"])
            if abs(float(r[k]["tenths"]) - x) > 0.0551 or not (abs(w - x) <= 0.505 or (w == 99 and x >= 99.5)):
                bad.append("the three precisions disagree at %s" % k)
                break
    for k in ("scale", "report", "years", "band"):
        f = d.get(k) or {}
        if not all(f.get(x) for x in ("text", "src", "year", "url", "title")) or \
                not f["url"].startswith("https://www.lsac.org/"):
            bad.append("%s needs its text, title, source, year and an lsac.org URL" % k)
    if bad:
        fail("data/lsat_percentiles.json: " + "; ".join(bad))


def lsat_page(d):
    rank_cite = cite(d["title"], {"src": d["src"], "year": d["year"], "url": d["url"]})
    scoring_cite = cite(d["scale"]["title"], d["scale"])
    band_cite = cite(d["band"]["title"], d["band"])
    r = d["ranks"]
    window = "%s, %s and %s" % tuple(d["window"])

    def lowest(p):
        return next(int(k) for k in reversed(LSAT_SCORES) if float(r[k]["hundredths"]) >= p)
    rows = "\n".join("<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>"
                     % (k, esc(r[k]["hundredths"]), esc(r[k]["tenths"]), esc(r[k]["whole"]))
                     for k in LSAT_SCORES)

    def at(score):
        return ("On LSAC's percentile table, %s percent of LSAT test scores in the %s testing "
                "years were lower than %s." % (r[score]["hundredths"], window, score))

    def need(p):
        s = lowest(p)
        return ("The lowest score with at least %d percent of test scores below it is %d, with "
                "%s percent, on LSAC's table for the %s testing years."
                % (p, s, r[str(s)]["hundredths"], window))
    faq = [
        ("What Percentile Is a 160 on the LSAT?", at("160"), rank_cite),
        ("What Percentile Is a 170 on the LSAT?", at("170"), rank_cite),
        ("What LSAT Score Is the 90th Percentile?", need(90), rank_cite),
        ("What LSAT Score Is the 50th Percentile?", need(50), rank_cite),
        ("What Is an LSAT Score Band?",
         'LSAC reports a score band with each score. In its words: "%s"' % d["band"]["text"], band_cite),
        ("How Often Does LSAC Update Its Percentiles?",
         'LSAC\'s scoring page says: "%s" And: "%s" The table on this page covers the %s testing '
         'years.' % (d["report"]["text"].split(". ", 1)[1], d["years"]["text"], window), scoring_cite),
    ]
    faq_html = "\n".join('<h3>%s</h3><p>%s</p><p class="src">Source: %s.</p>'
                         % (esc(q), esc(a), c) for q, a, c in faq)
    faq_ld = json.dumps({"@context": "https://schema.org", "@type": "FAQPage",
                         "mainEntity": [{"@type": "Question", "name": q,
                                         "acceptedAnswer": {"@type": "Answer", "text": a}}
                                        for q, a, _ in faq]}, separators=(",", ":"))
    ranks = json.dumps({"ranks": r, "window": window}, separators=(",", ":"))
    report = d["report"]["text"]
    page = ((D / "lsat_calculator.html").read_text()
            .replace("{{FAQ_LD}}", faq_ld).replace("{{FAQ_HTML}}", faq_html)
            .replace("{{ROWS}}", rows).replace("{{RANKS_JSON}}", ranks)
            .replace("{{RANK_CITE}}", rank_cite).replace("{{SCORING_CITE}}", scoring_cite)
            .replace("{{BAND_CITE}}", band_cite)
            .replace("{{DEFINITION}}", esc(d["definition"]))
            .replace("{{REPORT}}", esc(report))
            .replace("{{YEARS}}", esc(d["years"]["text"]))
            .replace("{{SCALE}}", esc(d["scale"]["text"]))
            .replace("{{BAND}}", esc(d["band"]["text"]))
            .replace("{{WINDOW}}", esc(window))
            .replace("{{READ}}", long_date(d["read"])))
    return partials.apply_chrome(page)


def write_page(rel, page):
    if "{{" in page:
        fail("unresolved placeholder in /%s/" % rel)
    if "—" in page or "–" in page:
        fail("em or en dash in /%s/" % rel)
    out = ROOT / rel
    out.mkdir(parents=True, exist_ok=True)
    (out / "index.html").write_text(page)
    print("built %s/" % rel)


def main():
    today = os.environ.get("BLOG_BUILD_DATE") or datetime.date.today().isoformat()
    exams = json.loads((ROOT / "data" / "exams.json").read_text())
    act = next((e for e in exams if e["slug"] == "act"), None)
    if act is None:
        fail("data/exams.json has no ACT entry to build the ACT calculator from")
    d = json.loads(ACT_RANKS.read_text())
    check_ranks(d)
    write_page("exams/act/score-calculator", act_page(act, d, today))
    gre = next((e for e in exams if e["slug"] == "gre"), None)
    if gre is None:
        fail("data/exams.json has no GRE entry to build the GRE calculator from")
    g = json.loads(GRE_RANKS.read_text())
    check_gre(g)
    write_page("exams/gre/score-calculator", gre_page(gre, g))
    sat = json.loads(SAT_RANKS.read_text())
    check_sat(sat)
    write_page("exams/sat/score-calculator", sat_page(sat))
    psat = json.loads(PSAT_RANKS.read_text())
    check_psat(psat)
    write_page("exams/sat/psat-calculator", psat_page(psat))
    lsat = json.loads(LSAT_RANKS.read_text())
    check_lsat(lsat)
    write_page("exams/lsat/percentile-calculator", lsat_page(lsat))


if __name__ == "__main__":
    main()
