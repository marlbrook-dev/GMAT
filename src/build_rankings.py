"""Builds /schools/ (MBA rankings pilot) from data/schools.json.

Composite method: each publisher rank is converted to points (101 - rank,
floor 0), then combined as a weighted average across the publishers that
rank the school (weights renormalized when a source is missing). Schools
are ordered by composite points; ties share a rank. Weights live in
WEIGHTS below and are shown verbatim on the page, so the page and the
math can never disagree.
"""
import json, pathlib, datetime, os, html, sys

D = pathlib.Path(__file__).parent
ROOT = D.parent
SITE = "https://startfromnowhere.com"

WEIGHTS = {"usnews": 0.30, "ft": 0.25, "bloomberg": 0.15, "qs": 0.15, "pq": 0.15}
MIN_SOURCES = 3  # a school needs ranks from at least this many publishers to get a composite rank
SOURCE_LABEL = {"usnews": "US News", "ft": "Financial Times", "bloomberg": "Bloomberg", "qs": "QS", "pq": "Poets and Quants"}

def esc(s):
    return html.escape(str(s), quote=True)

def composite(school):
    pts, wsum, n = 0.0, 0.0, 0
    for k, w in WEIGHTS.items():
        r = (school.get("ranks", {}).get(k) or {}).get("rank")
        if isinstance(r, (int, float)) and r >= 1:
            pts += w * max(0.0, 101.0 - float(r))
            wsum += w
            n += 1
    return round(pts / wsum, 1) if n >= MIN_SOURCES else None

def field(school, name):
    f = (school.get("profile", {}) or {}).get(name) or {}
    return f.get("v")

def fmt(v, suffix="", money=False):
    if v is None:
        return '<span class="na">-</span>'
    if money:
        return "$" + format(int(v), ",")
    return f"{v}{suffix}"

def main():
    data_path = ROOT / "data" / "schools.json"
    if not data_path.exists():
        print("build_rankings: no data/schools.json yet; skipping /schools/ build")
        return
    schools = json.loads(data_path.read_text())
    for s in schools:
        s["_score"] = composite(s)
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
            f'<td class="num">{fmt((s.get("ranks", {}).get(k) or {}).get("rank"))}</td>'
            for k in WEIGHTS)
        rows.append(
            f'<tr class="srow" data-slug="{esc(s["slug"])}" onclick="toggleDetail(\'{esc(s["slug"])}\')">'
            f'<td class="num rank">{s.get("_rank", "-")}</td>'
            f'<td><div class="sname">{esc(s["name"])}</div><div class="sloc">{esc(s.get("city", ""))}, {esc(s.get("state", ""))} · {esc(s.get("type", ""))}</div></td>'
            + ranks_cells +
            f'<td class="num">{fmt(gmat_v)}{("<span class=note>" + esc(gmat_ed) + " " + esc(gmat_note) + "</span>") if gmat_v is not None else ""}</td>'
            f'<td class="num">{fmt(field(s, "gpa"))}</td>'
            f'<td class="num">{fmt(field(s, "accept_rate_pct"), "%")}</td>'
            f'<td class="num">{fmt(field(s, "class_size"))}</td>'
            f'<td class="num">{fmt(field(s, "tuition_usd"), money=True)}</td>'
            f'<td><button class="addbtn" data-slug="{esc(s["slug"])}" onclick="event.stopPropagation();toggleList(\'{esc(s["slug"])}\')">+ List</button></td>'
            "</tr>")
    weights_rows = "".join(
        f"<tr><td>{SOURCE_LABEL[k]}</td><td class=\"num\">{int(w * 100)}%</td></tr>" for k, w in WEIGHTS.items())

    ld_items = "".join(
        f'{{"@type":"ListItem","position":{s["_rank"]},"name":{json.dumps(s["name"])}}},'
        for s in ranked[:10]).rstrip(",")

    out = (tpl
           .replace("{{ROWS}}", "\n".join(rows))
           .replace("{{DATA}}", json.dumps(schools, separators=(",", ":")))
           .replace("{{WEIGHTS_ROWS}}", weights_rows)
           .replace("{{N}}", str(len(schools)))
           .replace("{{UPDATED}}", today)
           .replace("{{LD_ITEMS}}", ld_items))
    if "{{" in out:
        print("build_rankings: unresolved placeholder", file=sys.stderr)
        sys.exit(1)
    for ch in out:
        if ch in "–—":
            print("build_rankings: em/en dash found", file=sys.stderr)
            sys.exit(1)
    dest = ROOT / "schools"
    dest.mkdir(exist_ok=True)
    (dest / "index.html").write_text(out)
    print(f"built schools/ with {len(ranked)} ranked + {len(unranked)} unranked programs")

if __name__ == "__main__":
    main()
