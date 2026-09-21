"""Builds /schools/ (MBA rankings) and one page per school from data/schools.json.

Two-layer ranking, both documented verbatim on the page:

1. Publisher consensus: each publisher rank converts to points (101 - rank,
   floor 0), combined as a weighted average over the publishers that rank
   the school (weights renormalized when a source is missing).

2. SFN Score (0 to 100): ranks every school, including those the big lists
   skip, from whatever verified data exists:
      publishers 50% + outcomes 20% + GMAT selectivity 20% + acceptance 10%
   with weights renormalized over available components. Outcomes = the mean
   of salary points (70k to 190k maps 0 to 100) and 3-month employment
   points (60% to 95% maps 0 to 100); both bands recalibrated August 2026
   to the observed range of official school reports. GMAT maps Focus 555 to 695 or
   Classic 605 to 745 onto 0 to 100 (whichever edition the school
   publishes; never converted). Acceptance maps 60% down to 6% onto 0 to
   100. A school needs the publisher component or at least two other
   components to be scored; otherwise it is listed unscored. This mirrors
   how the major publishers weight outcomes and selectivity, applied
   transparently to published data instead of surveys.
"""
import json, pathlib, datetime, os, html, re, sys

D = pathlib.Path(__file__).parent
ROOT = D.parent
sys.path.insert(0, str(D))
import partials
SITE = "https://startfromnowhere.com"
RANKINGS_LEGAL = ("Rankings cited from US News, Financial Times, Bloomberg, QS, and Poets and Quants, "
                  "each the property of its publisher. Class profile data from the sources shown on each row.")

WEIGHTS = {"usnews": 0.30, "ft": 0.25, "bloomberg": 0.15, "qs": 0.15, "pq": 0.15}
SOURCE_LABEL = {"usnews": "US News", "ft": "Financial Times", "bloomberg": "Bloomberg", "qs": "QS", "pq": "Poets and Quants"}
COMP_WEIGHTS = {"publishers": 0.50, "outcomes": 0.20, "gmat": 0.20, "accept": 0.10}

def lead_paragraph(s, p, g, gc, acc, tui, sal, cs):
    """The sentences an answer engine can actually quote.

    A language model answering "what does the Notre Dame MBA cost" lifts a sentence.
    It cannot lift a table cell, because a cell carries no subject and no year, so a
    page whose facts live only in tables gets read and not cited. These are the same
    figures the tables carry, written as complete sentences with the thing named, the
    number stated and the year attached, which is also the form a reader skims.
    """
    name = s["name"]
    out = []
    where = ", ".join(x for x in (s.get("city"), s.get("state")) if x)
    uni = s.get("university")
    first = "%s is the full-time MBA program at %s" % (name, uni) if uni and uni != name \
        else "%s is a full-time MBA program" % name
    if where:
        first += ", in %s" % where
    out.append(first + ".")
    if tui:
        out.append("Published tuition is $%s a year%s."
                   % (format(int(tui), ",d"),
                      " (%s, %s)" % ((p.get("tuition_usd") or {}).get("src"),
                                     (p.get("tuition_usd") or {}).get("year"))
                      if (p.get("tuition_usd") or {}).get("src") else ""))
    cls = []
    if cs:
        cls.append("%s students" % format(int(cs), ",d"))
    gv = g.get("v") or gc.get("v")
    if gv:
        # The stat field is free text and sometimes carries a whole provenance note
        # ("avg, Class of 2026, range 560-760, edition not labeled"). Dropping that
        # into a sentence produced prose no one would quote, so only a recognised
        # one word statistic is used and anything else becomes "a reported".
        raw = (g.get("stat") or gc.get("stat") or "").strip().lower()
        word = {"average": "an average", "avg": "an average", "mean": "an average",
                "median": "a median"}.get(raw.split(",")[0].strip(), "a reported")
        cls.append("%s GMAT%s of %s" % (word, " Focus" if g.get("v") else "", gv))
    if cls:
        # class_year is stored variously as "2027" and "Class of 2027".
        cy = str(p.get("class_year") or "").strip()
        if re.fullmatch(r"\d{4}", cy):
            cy = "Class of %s" % cy
        out.append("The %s has %s." % (cy or "most recent class",
                                       " and ".join(cls) if len(cls) == 2 else cls[0]))
    if acc is not None:
        out.append("The reported acceptance rate is %s percent." % fmt_num(acc))
    if sal:
        out.append("Median starting salary is $%s." % format(int(sal), ",d"))
    if s.get("_score") is not None:
        out.append("Start From Nowhere ranks it number %d of the %d programs it scores, "
                   "on a composite that blends published rankings with outcomes and "
                   "selectivity." % (s["_rank"], s.get("_ranked_total") or s["_total"]))
    out.append("Every figure on this page carries the source it came from and the year it "
               "was published; anything unverified shows a dash rather than an estimate.")
    return " ".join(out)


def fmt_num(v):
    if isinstance(v, float) and abs(v - round(v)) < 1e-9:
        return str(int(round(v)))
    return str(v)


def esc(s):
    return html.escape(str(s), quote=True)

def field(school, name):
    f = (school.get("profile", {}) or {}).get(name) or {}
    return f.get("v")

def clamp01(x):
    return max(0.0, min(1.0, x))

def pub_component(s):
    pts, wsum, n = 0.0, 0.0, 0
    for k, w in WEIGHTS.items():
        r = (s.get("ranks", {}).get(k) or {}).get("rank")
        if isinstance(r, (int, float)) and r >= 1:
            pts += w * max(0.0, 101.0 - float(r))
            wsum += w
            n += 1
    return (pts / wsum if wsum else None), n

def sfn_score(s):
    comps = {}
    pub, nsrc = pub_component(s)
    if pub is not None:
        comps["publishers"] = pub
    outs = []
    sal = field(s, "salary_median_usd")
    if sal is not None:
        outs.append(clamp01((sal - 70000) / (190000 - 70000)) * 100)
    emp = field(s, "employment_rate_pct")
    if emp is not None:
        outs.append(clamp01((emp - 60) / 35) * 100)
    if outs:
        comps["outcomes"] = sum(outs) / len(outs)
    gf, gc = field(s, "gmat_focus"), field(s, "gmat_classic")
    if gf is not None:
        comps["gmat"] = clamp01((gf - 555) / 140) * 100
    elif gc is not None:
        comps["gmat"] = clamp01((gc - 605) / 140) * 100
    ar = field(s, "accept_rate_pct")
    if ar is not None:
        comps["accept"] = clamp01((60 - ar) / 54) * 100
    ok = ("publishers" in comps) or (len(comps) >= 2)
    if not ok or s.get("discontinued"):
        return None, nsrc
    wsum = sum(COMP_WEIGHTS[k] for k in comps)
    return round(sum(COMP_WEIGHTS[k] * v for k, v in comps.items()) / wsum, 1), nsrc

def tier(nsrc):
    if nsrc >= 3:
        return "Publisher Consensus", ""
    if nsrc >= 1:
        return "Partial Consensus", ""
    return "Data Score", " gold"

def fmt(v, suffix="", money=False):
    if v is None:
        return '<span class="na">-</span>'
    if money:
        return "$" + format(int(v), ",")
    return f"{v}{suffix}"

def host_of(url):
    m = re.match(r"https?://([^/]+)", str(url or ""), re.I)
    if not m:
        return ""
    h = m.group(1).lower()
    return h[4:] if h.startswith("www.") else h


def is_secondary(school, f):
    """Did this figure come from the school itself, or from somebody else?

    The source ladder in data/DATA.md always allowed a tracked publisher when a
    school does not publish a figure, but a reader could not tell which rows those
    were without opening every link. The test is mechanical rather than a list of
    names: a figure is primary when its source URL sits on the school's own domain,
    and secondary when it does not. Secondary figures are marked with an asterisk
    and listed in a footnote, so nothing is presented as coming from the school
    that did not come from the school.
    """
    if not f or f.get("v") is None or not f.get("url"):
        return False
    own = host_of(school.get("website"))
    src = host_of(f.get("url"))
    if not own or not src:
        return False
    return not (src == own or src.endswith("." + own) or own.endswith("." + src))


def src_cell(f):
    if not f or f.get("v") is None:
        return ""
    bits = [b for b in [f.get("src"), str(f.get("year") or "")] if b]
    t = ", ".join(bits)
    if f.get("url"):
        return f'<span class="src"><a href="{esc(f["url"])}" rel="noopener" target="_blank">{esc(t) or "source"}</a></span>'
    return f'<span class="src">{esc(t)}</span>'

SECONDARY_MARK = '<sup class="sec-mark" title="From a secondary source, not the school">*</sup>'

PROFILE_FIELDS = [
    ("gmat_focus", "GMAT Focus", "", False), ("gmat_classic", "GMAT Classic", "", False),
    ("gre_quant", "GRE Quant", "", False), ("gre_verbal", "GRE Verbal", "", False),
    ("gpa", "Undergrad GPA", "", False), ("accept_rate_pct", "Acceptance rate", "%", False),
    ("class_size", "Class size", "", False), ("work_exp_years", "Work experience", " yrs", False),
    ("women_pct", "Women", "%", False), ("intl_pct", "International", "%", False),
    ("tuition_usd", "Tuition per year", "", True), ("salary_median_usd", "Median base salary", "", True),
    ("employment_rate_pct", "Employed at 3 months", "%", False),
]

def federal_section(s):
    """Federal earnings records, next to what the school reports itself.

    Two different measurements of the same thing, so both are labelled for what they
    are. The school's own number comes from its employment report and covers the
    graduates who responded. The federal number comes from tax and aid records and
    covers only people who took federal aid, which at a school with large need based
    scholarships and many international students is a minority. Where it is a small
    minority the page says so on the row rather than in a footnote, because that is
    the difference between a useful second opinion and a misleading one.
    """
    f = s.get("federal") or {}
    if not f.get("matched"):
        reason = f.get("reason")
        if not reason:
            return ""
        return ('<div class="section"><h2>Federal Earnings Records</h2>'
                '<p class="note">The US Department of Education publishes median '
                'earnings and debt by field of study, but %s, so there is nothing to '
                'show here. The class profile above is unaffected.</p></div>' % esc(reason))

    def row(label, fld, note=""):
        v = (f.get(fld) or {}).get("v")
        return ('<tr><td>%s</td><td class="num">%s</td><td class="src">%s</td></tr>'
                % (esc(label), fmt(v, money=True), esc(note)))

    n = f.get("earn_n")
    cls = field(s, "class_size")
    warn = ""
    if f.get("low_coverage") and n:
        warn = ('<p class="note" style="background:var(--amber-50);border:1px solid #F3DDB3;'
                'border-radius:8px;padding:10px 12px;margin-top:12px"><strong>Read this one '
                'carefully.</strong> The federal figures below rest on %s graduates%s, '
                'because only students who took federal aid appear in these records. At a '
                'school with large need based scholarships and many international students '
                'that is a small and unrepresentative slice, and the gap with the school\'s '
                'own reported figure mostly reflects who is counted rather than what '
                'graduates earn.</p>'
                % (format(n, ",d"),
                   " out of a class of %s" % format(int(cls), ",d") if cls else ""))
    rows = "".join([
        row("Median earnings, 1 year after completing", "earn_1yr_usd"),
        row("Median earnings, 4 years after completing", "earn_4yr_usd"),
        row("Median federal graduate debt", "debt_median_usd"),
        row("National median for the field, 4 years", "national_earn_4yr_usd",
            "all US business master's programs"),
    ])
    count_line = ("Based on %s graduates with federal earnings records." % format(n, ",d")
                  if n else "")
    return ('<div class="section"><h2>Federal Earnings Records</h2>'
            '<table><thead><tr><th>Measure</th><th class="num">Value</th><th>Note</th></tr>'
            '</thead><tbody>%s</tbody></table>%s'
            '<p class="note" style="margin-top:12px">Source: US Department of Education '
            'College Scorecard field of study file, master\'s degrees in Business '
            'Administration (CIP 5202) at %s. %s This is an independent measurement from '
            'tax and federal aid records, not a survey, and it does not feed the SFN Score. '
            'Where it disagrees with the school\'s own reported salary, the two are '
            'counting different people.</p></div>'
            % (warn, rows, esc(f.get("instnm", "")), count_line))


def peer_block(s, ranked):
    """The schools nearest this one in our ranking, plus the obvious next steps.

    Adjacent by rank, three either side, trimmed at the ends of the list. Each peer
    carries the one figure most likely to separate it from its neighbours, which is
    the average GMAT where the school reports one and the acceptance rate otherwise.
    """
    mine = s.get("_rank")
    cards = []
    if mine:
        by_rank = {x.get("_rank"): x for x in ranked if x.get("_rank")}
        wanted = [r for r in range(mine - 3, mine + 4) if r != mine and r in by_rank]
        # At the top and bottom of the list, reach further the other way so the block
        # is never a lonely two cards.
        while len(wanted) < 6:
            lo, hi = min(wanted or [mine]), max(wanted or [mine])
            nxt = [r for r in (lo - 1, hi + 1) if r in by_rank and r not in wanted]
            if not nxt:
                break
            wanted += nxt
        for r in sorted(wanted)[:6]:
            o = by_rank[r]
            pr = o.get("profile", {})
            gf = (pr.get("gmat_focus") or {}).get("v")
            gc = (pr.get("gmat_classic") or {}).get("v")
            ar = (pr.get("accept_rate_pct") or {}).get("v")
            # Focus and Classic are different scales and are never mixed or converted,
            # so the edition is named on the figure rather than dropped to make the
            # cards look uniform. A card showing 689 beside 731 without saying which
            # edition each is would be comparing two different scales.
            if gf is not None:
                fig = '<span class="num">%s</span> GMAT Focus' % gf
            elif gc is not None:
                fig = '<span class="num">%s</span> GMAT Classic' % gc
            elif ar is not None:
                fig = '<span class="num">%s%%</span> acceptance rate' % round(ar, 1)
            else:
                fig = '<span class="pq">Neither figure published</span>'
            cards.append(
                '<a class="peer" href="/schools/%s/"><span class="pr">#%d</span>'
                '<span class="pn">%s</span><span class="pf">%s</span></a>'
                % (esc(o["slug"]), r, esc(o["name"]), fig))
    peers = ('<h2>Programs Ranked Either Side of This One</h2>'
             '<p class="note">Adjacent in our ranking, which is usually what a '
             'shortlist looks like. Every figure is the school\'s own published '
             'number.</p><div class="peergrid">%s</div>' % "".join(cards)) if cards else ""
    nxt = (
        '<h2>Next Steps</h2><div class="nextgrid">'
        '<a class="nx" href="/apply/"><strong>Application Checklist</strong>'
        '<span>Track every deadline and requirement for this school and the rest of '
        'your shortlist. Free, no account.</span></a>'
        '<a class="nx" href="/app/"><strong>Practise for the GMAT</strong>'
        '<span>Adaptive practice on the skills the score report names. No card, and '
        'the first round needs no account.</span></a>'
        '<a class="nx" href="/funding/"><strong>Paying for It</strong>'
        '<span>What changed when Grad PLUS ended, and which schools award aid '
        'automatically.</span></a>'
        '<a class="nx" href="/schools/"><strong>All %d Programs</strong>'
        '<span>Filter the full table by GMAT band, acceptance rate, cost and '
        'region.</span></a>'
        '</div>' % len(ranked))
    return '<section class="onward">%s%s</section>' % (peers, nxt)



# The name a searcher actually types.
#
# Search Console for the three months to 2026-09-19: 125 queries sat at position 8 to 20
# with 773 impressions and ZERO clicks between them. They are all school statistic
# intents ("notre dame mba cost", "mays mba", "ross class profile") and the pattern is
# the same every time: the query names the UNIVERSITY and the title named only the
# business school. "Mendoza College of Business MBA: Cost, GMAT, and Class Profile" has
# no Notre Dame in it, so someone scanning a results page for what they typed never sees
# it.
#
# The title now carries both, shortened to what fits. Deliberately conservative: a page
# whose name already holds the university's distinctive word, or its acronym, is left
# exactly as it was, and anything over 42 characters falls back to the original rather
# than shipping a truncated title. 62 of 91 pages change; the other 29 were already fine.
_SEO_GENERIC = re.compile(
    r'\s*(?:The\s+)?(?:Graduate\s+)?(?:School|College|Schools)\s+of\s+'
    r'(?:Business(?:\s+Administration)?|Management|Industrial Administration|Public Affairs)\s*$',
    re.I)


def _seo_drop_given(s):
    """Endowed schools are searched by surname: "ross class profile", not "stephen m ross"."""
    s = re.sub(r'^(?:[A-Z]\.\s*){1,3}', '', s)
    s = re.sub(r'^[A-Z][a-z]+\s+[A-Z]\.\s+', '', s)
    return s.strip()


def _seo_short_uni(u):
    s = re.sub(r'^The\s+', '', u or '')
    # Systems written one way and searched another. Getting this wrong is not cosmetic:
    # calling UT Dallas "Texas" points at Austin, a different school with different
    # numbers on the page.
    m = re.match(r'University of California[,\s]+(.+)$', s, re.I)
    if m:
        campus = m.group(1).strip()
        return 'UCLA' if campus.lower() == 'los angeles' else 'UC ' + campus
    m = re.match(r'University of Texas at\s+(.+)$', s, re.I)
    if m:
        return 'UT ' + m.group(1).strip()
    s = re.sub(r'\s+SUNY$', '', s)
    s = re.sub(r'^University of (?:the\s+)?', '', s)
    s = re.sub(r'\s+University$', '', s)
    s = re.sub(r'\s*,\s*[A-Z][A-Za-z\s.-]+$', '', s)
    s = re.sub(r'\s+at\s+[A-Z].*$', '', s)
    return s.strip(' ,')


def _seo_short_school(n, uni, su):
    s = re.sub(r'^The\s+', '', n or '')
    for pref in (uni, su):
        if pref and s.lower().startswith(pref.lower()):
            s = s[len(pref):].strip()
    s = _SEO_GENERIC.sub('', s)
    for pat in (r'\s*Business School\s*$', r'\s*School of Business\s*$',
                r'\s*College of Business(?: and Economics)?\s*$',
                r'\s*School of Management\s*$'):
        s = re.sub(pat, '', s, flags=re.I)
    return _seo_drop_given(s.strip()).strip(' ,')


def _seo_trim_generic(n):
    """Drop the generic tail from a name that already names its university."""
    s = re.sub(r'^The\s+', '', n or '')
    s = _SEO_GENERIC.sub('', s)
    for pat in (r'\s*Business School\s*$', r'\s*School of Business\s*$',
                r'\s*College of Business(?: and Economics)?\s*$',
                r'\s*School of Management\s*$'):
        s = re.sub(pat, '', s, flags=re.I)
    return s.strip(' ,')


def seo_name(school):
    """Title-facing name: university plus school, only where that adds something."""
    name = (school.get('name') or '').strip()
    uni = (school.get('university') or '').strip()
    su = _seo_short_uni(uni)
    if not su:
        return name
    words = set(re.findall(r'[a-z]+', name.lower()))
    if set(re.findall(r'[a-z]+', su.lower())) & words:
        # Already carries the university, so nothing to prepend. Still drop the generic
        # tail: "University of Southern California Marshall School of Business MBA:
        # Acceptance Rate, Cost, and Class Profile" is 107 characters and Google shows
        # about sixty, so the half a searcher sees ended before the numbers did.
        return _seo_trim_generic(name) or name
    # NYU inside "NYU Stern" already is New York University; so is FIU.
    acronym = ''.join(w[0] for w in re.findall(r'[A-Za-z]+', uni) if w[:1].isupper())
    if acronym and len(acronym) >= 3 and acronym in re.findall(r'[A-Z]{2,}', name):
        return name
    ss = _seo_short_school(name, uni, su)
    cand = re.sub(r'\s+', ' ', ('%s %s' % (su, ss)).strip() if ss else su).strip()
    return cand if cand and len(cand) <= 42 else name


def school_page(s, tpl, today, ranked=()):
    p = s.get("profile", {})
    rank_rows = []
    for k in WEIGHTS:
        r = s.get("ranks", {}).get(k) or {}
        if r.get("rank") is not None:
            link = f'<a href="{esc(r["url"])}" rel="noopener" target="_blank">source</a>' if r.get("url") else ""
            rank_rows.append(f'<tr><td>{SOURCE_LABEL[k]}</td><td>{esc(r.get("edition") or "")}</td><td class="num">#{r["rank"]}</td><td class="src">{link}</td></tr>')
    if not rank_rows:
        rank_rows.append('<tr><td colspan="4">Not currently ranked by the five publishers we track. Its SFN rank comes from published outcome and selectivity data instead.</td></tr>')
    prof_rows = []
    secondary = []
    for key, label, suf, money in PROFILE_FIELDS:
        f = p.get(key) or {}
        if f.get("v") is None:
            # Acceptance rate is the single most searched attribute in our tracked
            # queries and most full-time MBA programs deliberately never publish it.
            # Dropping the row left the page silent on the question people most often
            # arrived asking. Saying plainly that the school does not release it is
            # both true and an answer.
            if key == "accept_rate_pct":
                prof_rows.append(
                    '<tr><td>%s</td><td class="num"><span class="note">not published</span>'
                    '</td><td class="src">Most full-time MBA programs do not release an '
                    'acceptance rate. We show a figure only where the school or a tracked '
                    'publisher states one.</td></tr>' % label)
            continue
        stat = f' <span class="src">{esc(f["stat"])}</span>' if f.get("stat") else ""
        mark = ""
        if is_secondary(s, f):
            mark = SECONDARY_MARK
            secondary.append((label, f))
        prof_rows.append(f'<tr><td>{label}</td><td class="num">{fmt(f["v"], suf, money)}{mark}{stat}</td><td>{src_cell(f)}</td></tr>')
    if not prof_rows:
        prof_rows.append('<tr><td colspan="3">This school does not publish a detailed class profile, or we have not yet verified one.</td></tr>')
    if secondary:
        items = "; ".join("%s (%s)" % (esc(lbl), esc(f.get("src") or "secondary source"))
                          for lbl, f in secondary)
        many = len(secondary) > 1
        footnote = ('<p class="note" style="margin-top:10px"><strong>*</strong> This school '
                    'does not publish %s on its own site, so %s from a secondary source: '
                    '%s. We look for the school\'s own page first and replace a secondary '
                    'figure as soon as the school publishes its own, so treat %s as '
                    'indicative rather than official.</p>'
                    % ("these figures" if many else "this figure",
                       "they come" if many else "it comes",
                       items, "them" if many else "it"))
    else:
        footnote = ('<p class="note" style="margin-top:10px">Every figure above comes from '
                    'this school\'s own published pages. Nothing here relies on a '
                    'secondary source.</p>')
    specs = [x for x in (s.get("specialties") or []) if x.get("name")]
    spec_html = ""
    if specs:
        chips = "".join(f'<span class="chip" title="{esc((x.get("src") or "") + " " + str(x.get("year") or ""))}">{esc(x["name"])}</span>' for x in specs)
        spec_html = f'<div class="section"><h2>Recognized Strengths</h2><div class="chips">{chips}</div><p class="src" style="margin-top:10px">As recognized in published specialty rankings; hover for the source.</p></div>'
    g = p.get("gmat_focus") or {}
    gc = p.get("gmat_classic") or {}
    # What the snippet says decides whether anyone clicks it. Search Console showed 120
    # queries already ranking at position 20 or better returning one click from 679
    # impressions, against roughly twenty expected at a normal rate for those positions.
    # The problem was never the ranking. Someone searching "notre dame mba cost" saw a
    # title reading "Class Profile and Rankings", with the word cost nowhere on it, and
    # scrolled past. The three things people actually ask for, by impression volume, are
    # acceptance rate, cost, and the class profile, so the description leads with those
    # numbers rather than with a category name.
    bits = []
    acc = (p.get("accept_rate_pct") or {}).get("v")
    if acc is not None:
        bits.append("acceptance rate %s%%" % fmt_num(acc))
    if g.get("v"):
        bits.append(("average GMAT Focus %s" % g["v"]) if (g.get("stat") or "") != "median"
                    else "median GMAT Focus %s" % g["v"])
    elif gc.get("v"):
        bits.append("GMAT %s" % gc["v"])
    tui = (p.get("tuition_usd") or {}).get("v")
    if tui:
        bits.append("tuition $%s a year" % format(int(tui), ",d"))
    sal = (p.get("salary_median_usd") or {}).get("v")
    if sal:
        bits.append("median starting salary $%s" % format(int(sal), ",d"))
    cs = (p.get("class_size") or {}).get("v")
    if cs:
        bits.append("class of %s" % format(int(cs), ",d"))
    desc = (", ".join(bits) + ".") if bits else "cost, acceptance rate, class profile and rankings."
    # The title promises only what this page can actually show. Only 16 of 91 schools
    # publish an MBA acceptance rate, so a fixed title naming it would be a broken
    # promise on four pages out of five, and a visitor who clicks and does not find the
    # number leaves faster than one who never clicked.
    have = []
    if acc is not None:
        have.append("Acceptance Rate")
    if tui:
        have.append("Cost")
    if g.get("v") or gc.get("v"):
        have.append("GMAT")
    if sal:
        have.append("Salary")
    if len(have) >= 2:
        title_bits = "%s, %s, and Class Profile" % (have[0], have[1])
    elif have:
        title_bits = "%s and Class Profile" % have[0]
    else:
        title_bits = "Class Profile and Rankings"
    badge, badge_class = tier(s["_nsrc"])
    website_btn = f'<a class="btn sec" href="{esc(s["website"])}" rel="noopener" target="_blank">Official Program Site</a>' if s.get("website") else ""
    method = "This school is ranked from a weighted consensus of the major published rankings plus published outcomes and selectivity data." if s["_nsrc"] >= 3 else \
             "Fewer than three major publishers rank this school, so its SFN rank leans on published outcomes and selectivity data, weighted exactly as documented." if s["_nsrc"] >= 1 else \
             "The five publishers we track do not rank this school, so its SFN rank comes entirely from published outcomes and selectivity data, weighted exactly as documented."
    ld = json.dumps({"@context": "https://schema.org", "@type": "CollegeOrUniversity", "name": s["name"],
                     "parentOrganization": s.get("university"), "address": {"@type": "PostalAddress", "addressLocality": s.get("city"), "addressRegion": s.get("state")},
                     **({"url": s["website"]} if s.get("website") else {})})
    bc = json.dumps({"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "MBA Rankings", "item": SITE + "/schools/"},
        {"@type": "ListItem", "position": 2, "name": s["name"], "item": f'{SITE}/schools/{s["slug"]}/'}]})
    # unique intro from verified data only
    ip = []
    if s.get("_rank"):
        ip.append(f'{s["name"]} ranks #{s["_rank"]} of {s.get("_total", "")} full-time MBA programs on the SFN composite')
        usn = (s.get("ranks", {}).get("usnews") or {}).get("rank")
        if usn:
            ip.append(f'and #{usn} with US News')
    intro = (", ".join(ip) + ". ") if ip else ""
    gm = p.get("gmat_focus") or {}
    gcl = p.get("gmat_classic") or {}
    facts_bits = []
    if gm.get("v"):
        facts_bits.append(f'a {gm.get("stat") or "reported"} GMAT Focus of {gm["v"]}')
    elif gcl.get("v"):
        facts_bits.append(f'a {gcl.get("stat") or "reported"} GMAT of {gcl["v"]} (Classic edition)')
    if (p.get("class_size") or {}).get("v"):
        facts_bits.append(f'a class of {p["class_size"]["v"]}')
    if (p.get("accept_rate_pct") or {}).get("v") is not None:
        facts_bits.append(f'a {p["accept_rate_pct"]["v"]}% acceptance rate')
    if facts_bits:
        intro += f'The {p.get("class_year") or "latest"} profile reports ' + ", ".join(facts_bits) + ". "
    intro += "Every figure below links to its source."
    # FAQ generated only from verified fields
    qa = []
    if gm.get("v"):
        qa.append((f'What GMAT score do you need for {s["name"]}?',
                   f'There is no cutoff. The {p.get("class_year") or "latest"} profile lists a {gm.get("stat") or "reported"} GMAT Focus of {gm["v"]}' + (f' ({gm.get("src")}, {gm.get("year")}).' if gm.get("src") else ".") + " Published figures are context, not cutoffs."))
    elif gcl.get("v"):
        qa.append((f'What GMAT score do you need for {s["name"]}?',
                   f'The {p.get("class_year") or "latest"} profile lists a {gcl.get("stat") or "reported"} GMAT of {gcl["v"]} on the Classic 200 to 800 scale' + (f' ({gcl.get("src")}, {gcl.get("year")}).' if gcl.get("src") else ".")))
    ar = p.get("accept_rate_pct") or {}
    if ar.get("v") is None:
        qa.append((f'What is the acceptance rate at {s["name"]}?',
                   f'{s["name"]} does not publish an acceptance rate, and neither do most '
                   f'full-time MBA programs; class profiles typically report class size, '
                   f'test scores and GPA but not selectivity. We show a rate only where the '
                   f'school or a tracked publisher states one, rather than estimating it '
                   f'from application counts.'))
    if ar.get("v") is not None:
        qa.append((f'What is the acceptance rate at {s["name"]}?',
                   f'Its reported acceptance rate is {ar["v"]}%' + (f' ({ar.get("src")}, {ar.get("year")}).' if ar.get("src") else ".")))
    tu = p.get("tuition_usd") or {}
    if tu.get("v") is not None:
        qa.append((f'How much is tuition at {s["name"]}?',
                   f'Published tuition is ${tu["v"]:,} per year' + (f' ({tu.get("src")}, {tu.get("year")}).' if tu.get("src") else ".") + " Fees and living costs are additional; confirm on the school site."))
    faq_ld, faq_section = "", ""
    if len(qa) >= 2:
        faq_ld = '<script type="application/ld+json">' + json.dumps({"@context": "https://schema.org", "@type": "FAQPage",
            "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in qa]}) + "</script>"
        faq_section = '<div class="section"><h2>Quick Answers</h2>' + "".join(
            f'<p style="margin:0 0 12px"><b>{esc(q)}</b><br>{esc(a)}</p>' for q, a in qa) + "</div>"
    out = (tpl.replace("{{NAME}}", esc(s["name"]))
              .replace("{{TITLE_BITS}}", esc(title_bits))
              .replace("{{SEO_NAME}}", esc(seo_name(s)))
              .replace("{{LEAD}}", esc(lead_paragraph(s, p, g, gc, acc, tui, sal, cs)))
              .replace("{{DESC_BITS}}", esc(desc))
              .replace("{{SLUG}}", esc(s["slug"]))
              .replace("{{FEDERAL_SECTION}}", federal_section(s))
              .replace("{{SLUG_JSON}}", json.dumps(s["slug"]))
              .replace("{{NAME_JSON}}", json.dumps(s["name"]))
              .replace("{{GMAT_JSON}}", json.dumps(
                  {"v": g["v"], "ed": "Focus", "stat": g.get("stat") or ""} if g.get("v") else
                  ({"v": gc["v"], "ed": "Classic", "stat": gc.get("stat") or ""} if gc.get("v") else None)))
              .replace("{{UNIVERSITY}}", esc(s.get("university") or ""))
              .replace("{{CITY}}", esc(s.get("city") or "")).replace("{{STATE}}", esc(s.get("state") or ""))
              .replace("{{TYPE}}", esc(s.get("type") or "")).replace("{{CLASS_YEAR}}", esc((p.get("class_year") or "profile pending")))
              .replace("{{BADGE_CLASS}}", badge_class).replace("{{BADGE}}", badge)
              .replace("{{WEBSITE_BTN}}", website_btn)
              .replace("{{RANK_DISPLAY}}", "#" + str(s["_rank"]) if s.get("_rank") else "-")
              .replace("{{SCORE}}", str(s["_score"]) if s.get("_score") is not None else "n/a")
              .replace("{{SPECIALTIES_SECTION}}", spec_html)
              .replace("{{RANK_ROWS}}", "\n".join(rank_rows))
              .replace("{{PROFILE_ROWS}}", "\n".join(prof_rows))
              .replace("{{SOURCE_FOOTNOTE}}", footnote)
              .replace("{{METHOD_LINE}}", method)
              .replace("{{UPDATED}}", today)
              .replace("{{INTRO}}", esc(intro).replace("&#x27;", "'"))
              .replace("{{ONWARD}}", peer_block(s, ranked))
              .replace("{{FAQ_SECTION}}", faq_section)
              .replace("{{FAQ_LD}}", faq_ld)
              .replace("{{BREADCRUMB_LD}}", bc)
              .replace("{{LD}}", ld))
    return out

def load_schools():
    sdir = ROOT / "data" / "schools"
    if sdir.is_dir():
        return [json.loads(p.read_text()) for p in sorted(sdir.glob("*.json"))]
    legacy = ROOT / "data" / "schools.json"
    if legacy.exists():
        return json.loads(legacy.read_text())
    return None


def schol_cell(s):
    """Scholarship review policy as a badge. Sourced from the school's own aid pages; a
    school that does not state a policy renders as a dash rather than an assumption, and
    sorts last in both directions."""
    sch = s.get("scholarship") or {}
    rev = (sch.get("review") or {}).get("v")
    pct = (sch.get("pct_receiving") or {}).get("v")
    avg = (sch.get("avg_award_usd") or {}).get("v")
    # A school can publish what it awards without publishing how it reviews, and vice
    # versa. Show whichever half exists rather than hiding real data behind a missing field.
    badge = ""
    if rev == "automatic":
        badge = '<span class="schol ok">Automatic</span>'
    elif rev == "separate":
        badge = '<span class="schol warn">Apply separately</span>'
    bits = []
    if pct is not None:
        bits.append(f"{pct}% get one")
    if avg is not None:
        bits.append(f"avg ${avg:,.0f}/yr")
    note = f'<span class="note">{", ".join(bits)}</span>' if bits else ""
    if not badge and not note:
        return '<span class="note">-</span>'
    return badge + note


def main():
    schools = load_schools()
    if schools is None:
        print("build_rankings: no data/schools/ yet; skipping /schools/ build")
        return
    import validate_schools
    validate_schools.validate(schools)
    dropped = [s["slug"] for s in schools if s.get("discontinued")]
    if dropped:
        print("build_rankings: excluding discontinued programs:", ", ".join(dropped))
    schools = [s for s in schools if not s.get("discontinued")]
    for s in schools:
        s["_score"], s["_nsrc"] = sfn_score(s)
    for s in schools:
        s["_total"] = len(schools)
    ranked = sorted([s for s in schools if s["_score"] is not None], key=lambda s: -s["_score"])
    rank, prev = 0, None
    for i, s in enumerate(ranked):
        if s["_score"] != prev:
            rank = i + 1
            prev = s["_score"]
        s["_rank"] = rank
    unranked = [s for s in schools if s["_score"] is None]
    # "number 44 of 91" was wrong: 91 is every school in the library, but only the
    # scored ones carry a rank at all.
    for s in schools:
        s["_ranked_total"] = len(ranked)

    today = os.environ.get("BLOG_BUILD_DATE") or datetime.date.today().isoformat()
    tpl = (D / "rankings_template.html").read_text()
    stpl = (D / "school_template.html").read_text()

    rows = []
    for s in ranked + unranked:
        p = s.get("profile", {})
        gmat = p.get("gmat_focus") or {}
        gmat_v, gmat_note = gmat.get("v"), (gmat.get("stat") or "")[:3]
        gmat_ed = "Focus"
        if gmat_v is None:
            gc = p.get("gmat_classic") or {}
            gmat_v, gmat_note, gmat_ed = gc.get("v"), (gc.get("stat") or "")[:3], "Classic"
        ranks_cells = "".join(
            f'<td class="num colx">{fmt((s.get("ranks", {}).get(k) or {}).get("rank"))}</td>'
            for k in WEIGHTS)
        acc = field(s, "accept_rate_pct")
        acc_cls = " acc-hot" if (acc is not None and acc < 15) else (" acc-warm" if (acc is not None and acc < 25) else "")
        tuition = field(s, "tuition_usd")
        tuition_cell = f'<span title="${tuition:,} per year">${round(tuition / 1000)}K</span>' if tuition is not None else '<span class="na">-</span>'
        rows.append(
            f'<tr class="srow" data-slug="{esc(s["slug"])}" onclick="toggleDetail(\'{esc(s["slug"])}\')">'
            f'<td class="ckcell" onclick="event.stopPropagation()"><input type="checkbox" class="rowck" data-slug="{esc(s["slug"])}" '
            f'aria-label="Add {esc(s["name"])} to my list" onchange="toggleList(\'{esc(s["slug"])}\')"></td>'
            f'<td class="num rank">{s.get("_rank", "-")}</td>'
            f'<td><div class="sname">{esc(s["name"])}</div><div class="sloc">{esc(s.get("city", ""))}, {esc(s.get("state", ""))} · {esc(s.get("type", ""))}</div></td>'
            f'<td class="num">{fmt(s.get("_score"))}</td>'
            f'<td class="num">{fmt(gmat_v)}{("<span class=note>" + esc(gmat_ed) + " " + esc(gmat_note) + "</span>") if gmat_v is not None else ""}</td>'
            + ranks_cells +
            f'<td class="num colx">{fmt(field(s, "gpa"))}</td>'
            f'<td class="num{acc_cls}">{fmt(acc, "%")}</td>'
            f'<td class="num colx">{fmt(field(s, "class_size"))}</td>'
            f'<td class="num">{fmt(field(s, "intl_pct"), "%")}</td>'
            f'<td>{schol_cell(s)}</td>'
            f'<td class="num">{tuition_cell}</td>'
            f'<td class="num">{fmt(field(s, "employment_rate_pct"), "%")}</td>'
            f'<td class="expcell"><span class="car">&#9660;</span></td>'
            "</tr>")
    weights_rows = "".join(
        f"<tr><td>{SOURCE_LABEL[k]}</td><td class=\"num\">{int(w * 100)}%</td></tr>" for k, w in WEIGHTS.items())

    ld_items = "".join(
        f'{{"@type":"ListItem","position":{s["_rank"]},"name":{json.dumps(s["name"])},"url":"{SITE}/schools/{s["slug"]}/"}},'
        for s in ranked[:10]).rstrip(",")

    out = (tpl
           .replace("{{ROWS}}", "\n".join(rows))
           .replace("{{DATA}}", json.dumps(schools, separators=(",", ":")))
           .replace("{{WEIGHTS_ROWS}}", weights_rows)
           .replace("{{N}}", str(len(schools)))
           .replace("{{UPDATED}}", today)
           .replace("{{LD_ITEMS}}", ld_items))
    dest = ROOT / "schools"
    dest.mkdir(exist_ok=True)
    pages = [(dest / "index.html", out)]

    # /apply/ shares this school data so a shortlist built on /schools/ carries over.
    # Only the fields the checklist actually renders: name, location, international share.
    idx = {s["slug"]: {"n": s["name"],
                       "l": ", ".join(x for x in (s.get("city"), s.get("state")) if x),
                       "i": field(s, "intl_pct")}
           for s in schools if not s.get("discontinued")}
    apply_page = (D / "apply_template.html").read_text().replace(
        "{{SCHOOL_INDEX}}", json.dumps(idx, separators=(",", ":")))
    (ROOT / "apply").mkdir(exist_ok=True)
    pages.append((ROOT / "apply" / "index.html", apply_page))
    for s in schools:
        sd = dest / s["slug"]
        sd.mkdir(exist_ok=True)
        pages.append((sd / "index.html", school_page(s, stpl, today, schools)))
    pages = [(path, partials.apply_chrome(content, extra_legal=RANKINGS_LEGAL)) for path, content in pages]
    for path, content in pages:
        if "{{" in content:
            print(f"build_rankings: unresolved placeholder in {path}", file=sys.stderr)
            sys.exit(1)
        if "—" in content or "–" in content:
            print(f"build_rankings: em/en dash in {path}", file=sys.stderr)
            sys.exit(1)
        path.write_text(content)
    print(f"built schools/ index + {len(schools)} school pages ({len(ranked)} ranked, {len(unranked)} unscored); apply/ checklist with {len(idx)} schools")

if __name__ == "__main__":
    main()
