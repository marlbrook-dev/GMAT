"""Builds /exams/ index and one hub page per exam from data/exams.json.

Every fact rendered carries the source and year recorded at collection;
null facts are simply omitted rather than guessed. Fees and policies
change, so each page carries a verify-with-the-maker note and the
official registration link.
"""
import json, pathlib, datetime, os, html, sys

D = pathlib.Path(__file__).parent
ROOT = D.parent
sys.path.insert(0, str(D))
import partials
SITE = "https://startfromnowhere.com"
LIVE = {"gmat"}  # exams with a live trainer today

# Plan feature matrix for /pricing/. Values: True = included, False = not
# included, string = shown verbatim. Order defines the page.
PRICING = [
    ("Training", [
        ("Adaptive questions per day", "10", "Unlimited", "Unlimited"),
        ("Original practice items (all plans, full bank)", True, True, True),
        ("Custom drills by skill and difficulty", True, True, True),
        ("Worked explanations that name the trap", True, True, True),
    ]),
    ("Mock Sections", [
        ("Full 45-minute sections under exam rules", "1 per month", "Unlimited", "Unlimited"),
        ("Bookmark and 3 answer changes, exactly like test day", True, True, True),
    ]),
    ("Games and Daily Habit", [
        ("Match, Memory, Blitz, Number crunch, Boss round", True, True, True),
        ("Question of the day with its own streak", True, True, True),
    ]),
    ("Lists and Rankings", [
        ("Full MBA rankings library with sourced data", True, True, True),
        ("List builder with CSV, PDF report, and share links", True, True, True),
        ("Target schools linked into your study plan", True, True, True),
    ]),
    ("Analytics and Planning", [
        ("Skill ratings and review queue", True, True, True),
        ("Full timing and skill analytics history", False, True, True),
    ]),
    ("Community", [
        ("Read every forum board", True, True, True),
        ("Post with a name or anonymously, no account needed", True, True, True),
    ]),
    ("Sync and Data", [
        ("Cross-device sync with a free account", True, True, True),
        ("Export and delete your data anytime", True, True, True),
    ]),
    ("Coaching", [
        ("SFN Assist AI coaching (as it ships)", False, False, "First access"),
        ("AI practice variants (as they ship)", False, False, True),
        ("Priority support", False, False, True),
    ]),
]

CHECK_SVG = ('<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
             'stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round" aria-label="Included">'
             '<path d="m5 13 4 4L19 7"/></svg>')

def pricing_cell(v):
    if v is True:
        return CHECK_SVG
    if v is False:
        return '<span class="no">-</span>'
    strong = "unlimited" in str(v).lower()
    return f'<span class="val{" strong" if strong else ""}">{esc(v)}</span>'

def pricing_rows():
    out = []
    for section, rows in PRICING:
        out.append(f'<div class="grp"><div>{esc(section)}</div></div>')
        for label, free, plus, pro in rows:
            out.append('<div class="prow frow">'
                       f'<div class="fn">{esc(label)}</div>'
                       f'<div class="fv">{pricing_cell(free)}</div>'
                       f'<div class="fv hl">{pricing_cell(plus)}</div>'
                       f'<div class="fv">{pricing_cell(pro)}</div></div>')
    return "\n".join(out)

def esc(s):
    return html.escape(str(s), quote=True)

def src_note(f):
    if not isinstance(f, dict):
        return ""
    bits = [b for b in [f.get("src"), str(f.get("year") or "")] if b]
    if not bits:
        return ""
    t = ", ".join(bits)
    if f.get("url"):
        return f' <span class="src">(<a href="{esc(f["url"])}" rel="noopener" target="_blank">{esc(t)}</a>)</span>'
    return f' <span class="src">({esc(t)})</span>'

def txt(f):
    return (f or {}).get("text")

def exam_page(e, tpl, today):
    live = e["slug"] in LIVE
    cta = ('<a class="btn" href="/app/">Start Training Free</a>' if live else
           f'<a class="btn" href="mailto:editors@startfromnowhere.com?subject={esc(e["short"])}%20waitlist">Join the {esc(e["short"])} Waitlist</a>')
    reg = (e.get("maker") or {}).get("register_url")
    reg_btn = f'<a class="btn sec" href="{esc(reg)}" rel="noopener" target="_blank">Register at {esc((e.get("maker") or {}).get("name") or "the official site")}</a>' if reg else ""
    def brief(s, cap=46):
        if not s:
            return s
        for sep in [";", ", always", " plus one", " including"]:
            if sep in s:
                s = s.split(sep)[0]
        return s if len(s) <= cap else s[:cap - 3].rstrip() + "..."
    tiles = []
    tt = txt(e.get("total_time"))
    if tt:
        tiles.append(("Total Time", brief(tt)))
    if e.get("sections"):
        tiles.append(("Sections", str(len(e["sections"]))))
    ss = txt(e.get("score_scale"))
    if ss:
        tiles.append(("Score Scale", brief(ss)))
    cost = (e.get("cost_usd") or {})
    if cost.get("v") is not None:
        tiles.append(("Cost", "$" + str(cost["v"])))
    elif cost.get("note"):
        import re as _re
        monies = _re.findall(r"\$\d+(?:\.\d+)?", cost["note"])
        tiles.append(("Cost", " / ".join(monies[:2]) if monies else brief(cost["note"])))
    val = (e.get("validity_years") or {})
    if val.get("v") is not None:
        tiles.append(("Scores Valid", f"{val['v']} years"))
    tiles_html = "".join(f'<div class="tile"><div class="l">{esc(l)}</div><div class="v">{esc(v)}</div></div>' for l, v in tiles[:5])

    sec_rows = ""
    for s in e.get("sections") or []:
        cells = [esc(s.get("name") or "")]
        cells.append(str(s["questions"]) if s.get("questions") is not None else "-")
        cells.append(f'{s["minutes"]} min' if s.get("minutes") is not None else "-")
        cells.append(esc(s.get("scale") or "-"))
        sec_rows += "<tr><td>" + "</td><td class=\"num\">".join(cells) + "</td></tr>"
    structure = f'<div class="section"><h2>Structure</h2><div class="tw"><table><thead><tr><th>Section</th><th class="num">Questions</th><th class="num">Time</th><th class="num">Scored</th></tr></thead><tbody>{sec_rows}</tbody></table></div>' if sec_rows else ""
    if structure and tt:
        structure += f'<p class="small">Total: {esc(tt)}.{src_note(e.get("total_time"))}</p>'
    structure += "</div>" if structure else ""

    rows = []
    def add(label, f, money=False):
        if isinstance(f, dict) and f.get("v") is not None:
            v = ("$" + str(f["v"])) if money else str(f["v"])
            rows.append((label, v + ((" " + f["note"]) if f.get("note") and money else ""), src_note(f)))
        elif isinstance(f, dict) and f.get("text"):
            rows.append((label, f["text"], src_note(f)))
    add("Cost", e.get("cost_usd"), money=True)
    add("Delivery", e.get("delivery"))
    add("Score Validity", {"v": f"{val['v']} years", "src": val.get("src"), "year": val.get("year"), "url": val.get("url")} if val.get("v") is not None else None)
    add("Retakes", e.get("retake_policy"))
    add("Score Release", e.get("score_release"))
    facts_rows = "".join(f'<tr><td>{esc(l)}</td><td>{esc(v)}{s}</td></tr>' for l, v, s in rows)
    logistics = f'<div class="section"><h2>Cost and Logistics</h2><div class="tw"><table><tbody>{facts_rows}</tbody></table></div><p class="small">Fees and policies change; confirm on the official registration page before booking.</p></div>' if facts_rows else ""

    used = txt(e.get("used_for")) or ""
    acc = txt(e.get("acceptance")) or ""
    usage = ""
    if used or acc:
        usage = '<div class="section"><h2>What It Is For and Who Accepts It</h2>'
        if used:
            usage += f'<p>{esc(used)}{src_note(e.get("used_for"))}</p>'
        if acc:
            usage += f'<p>{esc(acc)}{src_note(e.get("acceptance"))}</p>'
        usage += "</div>"

    kf = [f for f in (e.get("key_facts") or []) if f.get("text")]
    facts = ""
    if kf:
        lis = "".join(f'<li>{esc(f["text"])}{src_note(f)}</li>' for f in kf)
        facts = f'<div class="section"><h2>Worth Knowing</h2><ul class="kf">{lis}</ul></div>'

    prep = ('<div class="cta"><h2>Train for It Here</h2><p>The Start From Nowhere trainer is live for this exam: adaptive practice, mock sections, games, and flashcards, free to start with no account.</p><a class="btn" href="/app/">Open the trainer</a></div>' if live else
            f'<div class="cta"><h2>Prep Is on the Way</h2><p>Our adaptive trainer for the {esc(e["short"])} is in development: the same engine, games, and mock sections already live for the GMAT. Join the waitlist and you will be first in.</p>{cta}</div>')

    ld = json.dumps({"@context": "https://schema.org", "@type": "Article",
                     "headline": f'{e["name"]}: structure, timing, cost, and registration',
                     "author": {"@type": "Organization", "name": "Start From Nowhere"},
                     "publisher": {"@type": "Organization", "name": "Start From Nowhere"}})
    return (tpl.replace("{{NAME}}", esc(e["name"]))
               .replace("{{SHORT}}", esc(e["short"]))
               .replace("{{SLUG}}", esc(e["slug"]))
               .replace("{{AUDIENCE}}", esc(e.get("audience") or ""))
               .replace("{{STATUS}}", "Trainer Live" if live else "Trainer in Development")
               .replace("{{STATUS_CLASS}}", " live" if live else "")
               .replace("{{CTA}}", cta).replace("{{REG_BTN}}", reg_btn)
               .replace("{{TILES}}", tiles_html)
               .replace("{{STRUCTURE}}", structure)
               .replace("{{LOGISTICS}}", logistics)
               .replace("{{USAGE}}", usage)
               .replace("{{FACTS}}", facts)
               .replace("{{PREP}}", prep)
               .replace("{{UPDATED}}", today)
               .replace("{{LD}}", ld))

def main():
    data_path = ROOT / "data" / "exams.json"
    (ROOT / "pricing").mkdir(exist_ok=True)
    pricing = partials.apply_chrome((D / "pricing.html").read_text().replace("{{PRICING_ROWS}}", pricing_rows()))
    if "{{" in pricing:
        print("build_exams: unresolved placeholder in pricing.html", file=sys.stderr)
        sys.exit(1)
    if "—" in pricing or "–" in pricing:
        print("build_exams: em/en dash in pricing.html", file=sys.stderr)
        sys.exit(1)
    (ROOT / "pricing" / "index.html").write_text(pricing)
    if not data_path.exists():
        print("build_exams: no data/exams.json yet; built /pricing/ only")
        return
    exams = json.loads(data_path.read_text())
    today = os.environ.get("BLOG_BUILD_DATE") or datetime.date.today().isoformat()
    tpl = (D / "exam_template.html").read_text()
    itpl = (D / "exams_index_template.html").read_text()
    dest = ROOT / "exams"
    dest.mkdir(exist_ok=True)
    cards = []
    pages = []
    for e in exams:
        live = e["slug"] in LIVE
        sub = e.get("audience") or ""
        cards.append(f'<a class="card exam" href="/exams/{esc(e["slug"])}/"><div class="row"><span class="en">{esc(e["name"])}</span><span class="tag{" live" if live else " wait"}">{"Trainer Live" if live else "Guide"}</span></div><p>{esc(sub)}</p></a>')
        ed = dest / e["slug"]
        ed.mkdir(exist_ok=True)
        pages.append((ed / "index.html", exam_page(e, tpl, today)))
    pages.append((dest / "index.html", itpl.replace("{{CARDS}}", "\n".join(cards)).replace("{{UPDATED}}", today)))
    pages = [(path, partials.apply_chrome(content)) for path, content in pages]
    for path, content in pages:
        if "{{" in content:
            print(f"build_exams: unresolved placeholder in {path}", file=sys.stderr)
            sys.exit(1)
        if "—" in content or "–" in content:
            print(f"build_exams: em/en dash in {path}", file=sys.stderr)
            sys.exit(1)
        path.write_text(content)
    print(f"built exams/ index + {len(exams)} exam pages + pricing/")

if __name__ == "__main__":
    main()
