"""Builds /schools/ (MBA rankings) and one page per school from data/schools.json.

Two-layer ranking, both documented verbatim on the page:

1. Publisher consensus: each publisher rank converts to points (101 - rank,
   floor 0), combined as a weighted average over the publishers that rank
   the school (weights renormalized when a source is missing).

2. SFN Score (0 to 100): ranks every school, including those the big lists
   skip, from whatever verified data exists:
      publishers 50% + outcomes 20% + GMAT selectivity 20% + acceptance 10%
   with weights renormalized over available components. Outcomes = the mean
   of salary points (90k to 185k maps 0 to 100) and 3-month employment
   points (70% to 100% maps 0 to 100). GMAT maps Focus 555 to 695 or
   Classic 605 to 745 onto 0 to 100 (whichever edition the school
   publishes; never converted). Acceptance maps 60% down to 6% onto 0 to
   100. A school needs the publisher component or at least two other
   components to be scored; otherwise it is listed unscored. This mirrors
   how the major publishers weight outcomes and selectivity, applied
   transparently to published data instead of surveys.
"""
import json, pathlib, datetime, os, html, sys

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
        outs.append(clamp01((sal - 90000) / (185000 - 90000)) * 100)
    emp = field(s, "employment_rate_pct")
    if emp is not None:
        outs.append(clamp01((emp - 70) / 30) * 100)
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

def src_cell(f):
    if not f or f.get("v") is None:
        return ""
    bits = [b for b in [f.get("src"), str(f.get("year") or "")] if b]
    t = ", ".join(bits)
    if f.get("url"):
        return f'<span class="src"><a href="{esc(f["url"])}" rel="noopener" target="_blank">{esc(t) or "source"}</a></span>'
    return f'<span class="src">{esc(t)}</span>'

PROFILE_FIELDS = [
    ("gmat_focus", "GMAT Focus", "", False), ("gmat_classic", "GMAT Classic", "", False),
    ("gre_quant", "GRE Quant", "", False), ("gre_verbal", "GRE Verbal", "", False),
    ("gpa", "Undergrad GPA", "", False), ("accept_rate_pct", "Acceptance rate", "%", False),
    ("class_size", "Class size", "", False), ("work_exp_years", "Work experience", " yrs", False),
    ("women_pct", "Women", "%", False), ("intl_pct", "International", "%", False),
    ("tuition_usd", "Tuition per year", "", True), ("salary_median_usd", "Median base salary", "", True),
    ("employment_rate_pct", "Employed at 3 months", "%", False),
]

def school_page(s, tpl, today):
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
    for key, label, suf, money in PROFILE_FIELDS:
        f = p.get(key) or {}
        if f.get("v") is None:
            continue
        stat = f' <span class="src">{esc(f["stat"])}</span>' if f.get("stat") else ""
        prof_rows.append(f'<tr><td>{label}</td><td class="num">{fmt(f["v"], suf, money)}{stat}</td><td>{src_cell(f)}</td></tr>')
    if not prof_rows:
        prof_rows.append('<tr><td colspan="3">This school does not publish a detailed class profile, or we have not yet verified one.</td></tr>')
    specs = [x for x in (s.get("specialties") or []) if x.get("name")]
    spec_html = ""
    if specs:
        chips = "".join(f'<span class="chip" title="{esc((x.get("src") or "") + " " + str(x.get("year") or ""))}">{esc(x["name"])}</span>' for x in specs)
        spec_html = f'<div class="section"><h2>Recognized Strengths</h2><div class="chips">{chips}</div><p class="src" style="margin-top:10px">As recognized in published specialty rankings; hover for the source.</p></div>'
    g = p.get("gmat_focus") or {}
    gc = p.get("gmat_classic") or {}
    bits = []
    if g.get("v"):
        bits.append(f'GMAT Focus {g["v"]} {g.get("stat") or ""}'.strip() + ",")
    elif gc.get("v"):
        bits.append(f'GMAT {gc["v"]} {gc.get("stat") or ""}'.strip() + ",")
    cs = p.get("class_size") or {}
    if cs.get("v"):
        bits.append(f'class of {cs["v"]},')
    desc = (" ".join(bits) + " rankings from five major publishers.") if bits else "rankings, class profile, and sources."
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
        qa.append((f'What GMAT score does {s["name"]} report?',
                   f'The {p.get("class_year") or "latest"} profile lists a {gm.get("stat") or "reported"} GMAT Focus of {gm["v"]}' + (f' ({gm.get("src")}, {gm.get("year")}).' if gm.get("src") else ".") + " Published figures are context, not cutoffs."))
    elif gcl.get("v"):
        qa.append((f'What GMAT score does {s["name"]} report?',
                   f'The {p.get("class_year") or "latest"} profile lists a {gcl.get("stat") or "reported"} GMAT of {gcl["v"]} on the Classic 200 to 800 scale' + (f' ({gcl.get("src")}, {gcl.get("year")}).' if gcl.get("src") else ".")))
    ar = p.get("accept_rate_pct") or {}
    if ar.get("v") is not None:
        qa.append((f'How selective is {s["name"]}?',
                   f'Its reported acceptance rate is {ar["v"]}%' + (f' ({ar.get("src")}, {ar.get("year")}).' if ar.get("src") else ".")))
    tu = p.get("tuition_usd") or {}
    if tu.get("v") is not None:
        qa.append((f'How much does the {s["short"] if s.get("short") else s["name"]} MBA cost?',
                   f'Published tuition is ${tu["v"]:,} per year' + (f' ({tu.get("src")}, {tu.get("year")}).' if tu.get("src") else ".") + " Fees and living costs are additional; confirm on the school site."))
    faq_ld, faq_section = "", ""
    if len(qa) >= 2:
        faq_ld = '<script type="application/ld+json">' + json.dumps({"@context": "https://schema.org", "@type": "FAQPage",
            "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in qa]}) + "</script>"
        faq_section = '<div class="section"><h2>Quick Answers</h2>' + "".join(
            f'<p style="margin:0 0 12px"><b>{esc(q)}</b><br>{esc(a)}</p>' for q, a in qa) + "</div>"
    out = (tpl.replace("{{NAME}}", esc(s["name"]))
              .replace("{{DESC_BITS}}", esc(desc))
              .replace("{{SLUG}}", esc(s["slug"]))
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
              .replace("{{METHOD_LINE}}", method)
              .replace("{{UPDATED}}", today)
              .replace("{{INTRO}}", esc(intro).replace("&#x27;", "'"))
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
    for s in schools:
        sd = dest / s["slug"]
        sd.mkdir(exist_ok=True)
        pages.append((sd / "index.html", school_page(s, stpl, today)))
    pages = [(path, partials.apply_chrome(content, extra_legal=RANKINGS_LEGAL)) for path, content in pages]
    for path, content in pages:
        if "{{" in content:
            print(f"build_rankings: unresolved placeholder in {path}", file=sys.stderr)
            sys.exit(1)
        if "—" in content or "–" in content:
            print(f"build_rankings: em/en dash in {path}", file=sys.stderr)
            sys.exit(1)
        path.write_text(content)
    print(f"built schools/ index + {len(schools)} school pages ({len(ranked)} ranked, {len(unranked)} unscored)")

if __name__ == "__main__":
    main()
