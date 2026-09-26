"""Read a Google Search Console "Performance on Search" export and say what it means.

    python3 src/gsc_report.py path/to/export.xlsx            the report
    python3 src/gsc_report.py export.xlsx --json out.json    also write the aggregates

Search Console's own interface answers one question at a time. The decisions this site
makes from it need four answers side by side: which KIND of page earns impressions, what
the people seeing it were ASKING, how close each query is to page one, and whether a URL
still drawing impressions still exists. The last one is the check that would have caught
the withdrawn exam guides still ranking into a 404 (INC-0109), so it runs against the
built site in this checkout, not against a list of sections.

The export is the owner's analytics and this repository is public, so the raw file is
never committed. The tool reads it from wherever it was downloaded, and --json writes
only aggregates plus the short striking-distance list.

Needs openpyxl (pip install openpyxl); the build never imports this file.
"""
import collections
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).parent.parent

# What a searcher was asking, in the order the patterns are tried. First match wins, so
# the more specific intents come first. Anything unmatched is brand or navigational
# ("kellogg mba"), where the school's own site will always rank first.
INTENTS = [
    ("acceptance rate", r"acceptance|admit rate|admission rate|admissions rate|selectiv"),
    ("gmat/gre average", r"(average|avg|median|mean).*(gmat|gre)|(gmat|gre).*(average|median)|gmat score for|gre score for"),
    ("class profile", r"class profile|\bprofile\b|class size"),
    ("cost/tuition", r"cost|tuition|\bfee|price|expens|afford"),
    ("ranking", r"\brank"),
    ("salary", r"salary|\bpay\b|earn"),
    ("exam format/length", r"length|how long is|format|structure|sections|how many questions|duration"),
    ("study plan/prep", r"study|\bprep|prepare|schedule|\bplan\b"),
    ("score chart/percentile", r"chart|percentile|good .*score|score scale|scoring"),
    ("comparison", r"\bvs\b|versus|\bor gre\b|compare"),
    ("deadline", r"deadline|\bround\b"),
]

BUCKETS = [(3, "1-3"), (10, "4-10"), (20, "11-20"), (30, "21-30"), (50, "31-50"), (10 ** 9, "51+")]


def load(path):
    try:
        import openpyxl
    except ImportError:
        raise SystemExit("gsc_report: needs openpyxl (pip install openpyxl)")
    wb = openpyxl.load_workbook(path, read_only=True)
    sheets = {}
    for ws in wb.worksheets:
        rows = [r for r in ws.iter_rows(values_only=True)]
        sheets[ws.title] = rows[1:] if rows else []
    for need in ("Queries", "Pages"):
        if need not in sheets:
            raise SystemExit("gsc_report: %s has no %r sheet; is it a Performance export?" % (path, need))
    return sheets


def num(v):
    return float(v) if isinstance(v, (int, float)) else 0.0


def page_type(url):
    p = re.sub(r"^https?://[^/]+", "", url or "")
    seg = p.strip("/").split("/")[0] if p.strip("/") else "(home)"
    return seg


def intent(q):
    for name, rx in INTENTS:
        if re.search(rx, q or ""):
            return name
    return "brand/other"


def bucket(pos):
    for hi, label in BUCKETS:
        if pos <= hi:
            return label
    return "51+"


def built(url):
    """Does this checkout's built site serve the URL? None when nothing is built here."""
    if not (ROOT / "index.html").exists():
        return None
    p = re.sub(r"^https?://[^/]+", "", url or "").split("?")[0].split("#")[0]
    if p in ("", "/"):
        return True
    rel = p.lstrip("/")
    cands = [ROOT / rel, ROOT / rel / "index.html", ROOT / (rel.rstrip("/") + ".html")]
    return any(c.is_file() for c in cands)


def group(rows, key):
    agg = collections.OrderedDict()
    for r in rows:
        k = key(r)
        a = agg.setdefault(k, {"n": 0, "clicks": 0.0, "impressions": 0.0, "wpos": 0.0})
        a["n"] += 1
        a["clicks"] += num(r[1])
        a["impressions"] += num(r[2])
        a["wpos"] += num(r[4]) * num(r[2])
    out = []
    for k, a in agg.items():
        imp = a["impressions"]
        out.append({"key": k, "rows": a["n"], "clicks": int(a["clicks"]), "impressions": int(imp),
                    "position": round(a["wpos"] / imp, 1) if imp else None})
    return sorted(out, key=lambda x: -x["impressions"])


def report(path):
    sh = load(path)
    Q = [r for r in sh["Queries"] if r and r[0]]
    P = [r for r in sh["Pages"] if r and r[0]]
    chart = [r for r in sh.get("Chart", []) if r and r[0]]
    dates = [str(r[0]) for r in chart]
    total_imp = sum(num(r[2]) for r in chart) or sum(num(r[2]) for r in P)
    total_clk = sum(num(r[1]) for r in chart) or sum(num(r[1]) for r in P)
    out = {
        "range": [dates[0], dates[-1]] if dates else None,
        "impressions": int(total_imp), "clicks": int(total_clk),
        "ctr_pct": round(100 * total_clk / total_imp, 3) if total_imp else None,
        "devices": [{"device": r[0], "clicks": int(num(r[1])), "impressions": int(num(r[2])),
                     "position": round(num(r[4]), 1)} for r in sh.get("Devices", []) if r and r[0]],
        "page_types": group(P, lambda r: page_type(r[0])),
        "intents": group(Q, lambda r: intent(r[0])),
        "query_positions": group(Q, lambda r: bucket(num(r[4]))),
        "striking_distance": [{"query": r[0], "impressions": int(num(r[2])), "position": round(num(r[4]), 1),
                               "clicks": int(num(r[1]))}
                              for r in sorted((r for r in Q if num(r[4]) <= 15), key=lambda r: -num(r[2]))[:25]],
    }
    gone = []
    for r in P:
        b = built(r[0])
        if b is False:
            gone.append({"url": r[0], "impressions": int(num(r[2])), "position": round(num(r[4]), 1)})
    out["not_built"] = sorted(gone, key=lambda x: -x["impressions"])
    out["not_built_checked"] = (ROOT / "index.html").exists()
    return out


def show(r):
    w = print
    w("Search Console, %s to %s" % tuple(r["range"]) if r["range"] else "Search Console export")
    w("  %s impressions, %s clicks, CTR %s%%" % (format(r["impressions"], ",d"), r["clicks"], r["ctr_pct"]))
    for d in r["devices"]:
        w("  %-8s %7s impressions  %3d clicks  position %s" % (d["device"], format(d["impressions"], ",d"), d["clicks"], d["position"]))

    def table(title, rows, label):
        w("\n%s" % title)
        w("  %-26s %5s %6s %8s %8s" % (label, "rows", "clicks", "impr", "position"))
        for x in rows:
            w("  %-26s %5d %6d %8s %8s" % (str(x["key"])[:26], x["rows"], x["clicks"],
                                         format(x["impressions"], ",d"), x["position"]))

    table("By page type (first path segment)", r["page_types"], "section")
    table("By what the searcher asked", r["intents"], "intent")
    order = [b[1] for b in BUCKETS]
    table("Queries by average position", sorted(r["query_positions"], key=lambda x: order.index(x["key"])), "position")
    w("\nStriking distance: queries averaging position 15 or better, by impressions")
    for x in r["striking_distance"]:
        w("  %5d impr  pos %5.1f  clicks %d  %s" % (x["impressions"], x["position"], x["clicks"], x["query"]))
    if not r["not_built_checked"]:
        w("\nNo built site in this checkout, so URLs were not checked; run python3 src/build.py first.")
    elif r["not_built"]:
        w("\nURLs with impressions that this build does NOT produce (redirect them, see RETIRED in src/worker.mjs):")
        for x in r["not_built"]:
            w("  %5d impr  pos %5.1f  %s" % (x["impressions"], x["position"], x["url"]))
    else:
        w("\nEvery URL with impressions is produced by this build.")


def main(argv):
    args = [a for a in argv if not a.startswith("--")]
    if not args:
        raise SystemExit(__doc__)
    r = report(args[0])
    show(r)
    if "--json" in argv:
        i = argv.index("--json")
        dest = pathlib.Path(argv[i + 1])
        dest.write_text(json.dumps(r, indent=1) + "\n")
        print("\nwrote %s" % dest)


if __name__ == "__main__":
    main(sys.argv[1:])
