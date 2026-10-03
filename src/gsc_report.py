"""Read a Google Search Console "Performance on Search" export and say what it means.

    python3 src/gsc_report.py path/to/export.xlsx            the report
    python3 src/gsc_report.py export.xlsx --json out.json    also write the aggregates
    python3 src/gsc_report.py new.xlsx --since old.xlsx      also say what changed between two

Search Console's own interface answers one question at a time. The decisions this site
makes from it need four answers side by side: which KIND of page earns impressions, what
the people seeing it were ASKING, how close each query is to page one, and whether a URL
still drawing impressions still exists. The last one is the check that would have caught
the withdrawn exam guides still ranking into a 404 (INC-0109), so it runs against the
built site in this checkout, not against a list of sections.

Search Console exports a window ("Last 3 months"), so two exports a week apart mostly
overlap, and comparing their totals compares two windows that share most of their days.
--since takes the earlier export and reports only the days the later one adds: the daily
rows exactly, and each page type as the later total minus the earlier, with the average
position those added impressions must have had. That subtraction holds only while both
windows start on the same day, so the tool checks and says when they do not. It is not done
by intent: the Pages sheet lists nearly every impression, but the Queries sheet lists well
under half of them (Search Console withholds rare queries and stops at 1,000 rows), and the
share it covers moves between exports, so a difference by intent would mostly measure that.

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
    # Written with search operators: a leading + or %, or a quoted figure. People rarely
    # type these; tools that check a page's numbers do, and counted as brand searches or
    # listed as striking distance they look like demand that is not there.
    ("operator syntax", r'^[+%]|"[$\d][\d,.]*"'),
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


def retired():
    """The Worker's RETIRED table, old path to new, read from src/worker.mjs so the report
    and the redirect cannot disagree about what is already handled (INC-0198)."""
    f = ROOT / "src" / "worker.mjs"
    if not f.exists():
        return {}
    src = f.read_text()
    m = re.search(r"const RETIRED = \{(.*?)\};", src, re.S)
    table = dict(re.findall(r'"(/[^"]*)"\s*:\s*"([^"]*)"', m.group(1))) if m else {}
    # A table the parser cannot read would switch the exclusion off without a word and
    # bring the false alarm back, so a format change has to update this function.
    if "RETIRED" in src and (not m or (not table and m.group(1).strip())):
        raise SystemExit("gsc_report: src/worker.mjs has a RETIRED table this parser cannot "
                         "read; update retired() to its format")
    return table


def url_path(url):
    """The path the Worker looks up: no host, query or fragment, with a trailing slash."""
    p = re.sub(r"^https?://[^/]+", "", url or "").split("?")[0].split("#")[0] or "/"
    return p if p.endswith("/") else p + "/"


def sums(rows, key):
    """Impressions, clicks and impression-weighted position summed per key, unrounded,
    so two exports can be subtracted without the rounding of group() leaking in."""
    agg = collections.OrderedDict()
    for r in rows:
        a = agg.setdefault(key(r), [0.0, 0.0, 0.0])
        a[0] += num(r[2])
        a[1] += num(r[1])
        a[2] += num(r[4]) * num(r[2])
    return agg


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
        # Operator queries are left out: they are tools checking a figure, not people a
        # better page would win.
        "striking_distance": [{"query": r[0], "impressions": int(num(r[2])), "position": round(num(r[4]), 1),
                               "clicks": int(num(r[1]))}
                              for r in sorted((r for r in Q if num(r[4]) <= 15 and intent(r[0]) != "operator syntax"),
                                              key=lambda r: -num(r[2]))[:25]],
    }
    table = retired()
    gone, redirected = [], []
    for r in P:
        row = {"url": r[0], "impressions": int(num(r[2])), "position": round(num(r[4]), 1)}
        path = url_path(r[0])
        if path in table:
            row["to"] = table[path]
            redirected.append(row)
        elif built(r[0]) is False:
            gone.append(row)
    out["not_built"] = sorted(gone, key=lambda x: -x["impressions"])
    out["redirected"] = sorted(redirected, key=lambda x: -x["impressions"])
    out["not_built_checked"] = (ROOT / "index.html").exists()
    return out


def since(new_path, old_path):
    """The days the later export adds to the earlier one (see the module docstring)."""
    old, new = load(old_path), load(new_path)
    co = {str(r[0]): r for r in old.get("Chart", []) if r and r[0]}
    cn = {str(r[0]): r for r in new.get("Chart", []) if r and r[0]}
    if not co or not cn:
        raise SystemExit("gsc_report: --since needs the Chart sheet (the daily rows) in both exports")
    added = sorted(d for d in cn if d > max(co))
    last7 = sorted(co)[-7:]
    out = {
        "old_range": [min(co), max(co)], "new_range": [min(cn), max(cn)],
        "same_start": min(co) == min(cn),
        "days": [{"date": d, "clicks": int(num(cn[d][1])), "impressions": int(num(cn[d][2])),
                  "position": round(num(cn[d][4]), 1)} for d in added],
        "old_last7_per_day": int(sum(num(co[d][2]) for d in last7) / len(last7)),
    }
    imp = sum(x["impressions"] for x in out["days"])
    out["added"] = {"impressions": imp, "clicks": sum(x["clicks"] for x in out["days"]),
                    "position": round(sum(num(cn[d][4]) * num(cn[d][2]) for d in added) / imp, 1) if imp else None}
    # Subtracting totals is only meaningful while both windows start on the same day;
    # once the three months roll, the earlier export holds days the later one dropped.
    if out["same_start"] and added:
        def delta(rows_old, rows_new, key):
            a, b = sums(rows_old, key), sums(rows_new, key)
            res = []
            for k, (bi, bc, bw) in b.items():
                ai, ac, aw = a.get(k, (0.0, 0.0, 0.0))
                di = bi - ai
                res.append({"key": k, "impressions": int(round(di)), "clicks": int(round(bc - ac)),
                            "position": round((bw - aw) / di, 1) if di >= 1 else None,
                            "position_before": round(aw / ai, 1) if ai else None})
            return sorted(res, key=lambda x: -x["impressions"])
        P0 = [r for r in old["Pages"] if r and r[0]]
        P1 = [r for r in new["Pages"] if r and r[0]]
        out["page_types"] = delta(P0, P1, lambda r: page_type(r[0]))
    # How much of each export's total its sheets account for. Pages lists nearly every
    # impression, so page types subtract cleanly. Queries does not: Search Console withholds
    # rare queries and lists at most 1,000, so the share it covers moves between exports and
    # a subtraction by intent would mostly measure that movement, so it is not attempted.
    def cover(sheets, chart, name):
        tot = sum(num(r[2]) for r in chart.values())
        got = sum(num(r[2]) for r in sheets.get(name, []) if r and r[0])
        return round(100 * got / tot, 1) if tot else None
    out["coverage"] = {name: [cover(old, co, name), cover(new, cn, name)] for name in ("Pages", "Queries")}
    return out


def show_since(s):
    w = print
    w("\nSince the earlier export (%s to %s), this one adds %d day(s)" % (s["old_range"][0], s["old_range"][1], len(s["days"])))
    if not s["days"]:
        return
    w("  %-10s %7s %6s %8s" % ("date", "impr", "clicks", "position"))
    for d in s["days"]:
        w("  %-10s %7s %6d %8s" % (d["date"], format(d["impressions"], ",d"), d["clicks"], d["position"]))
    a = s["added"]
    w("  %s impressions, %d clicks, position %s; the earlier export's last 7 days averaged %s a day"
      % (format(a["impressions"], ",d"), a["clicks"], a["position"], format(s["old_last7_per_day"], ",d")))
    if not s["same_start"]:
        w("\n  The two windows start on different days (%s and %s), so the earlier export holds days\n"
          "  the later one dropped; only the daily rows above compare, and the breakdowns are skipped."
          % (s["old_range"][0], s["new_range"][0]))
        return
    cp, cq = s["coverage"]["Pages"], s["coverage"]["Queries"]
    w("\nAdded days by page type: the later export minus the earlier, and the position those added")
    w("impressions averaged (the Pages sheet lists %s%% and %s%% of each export's impressions)" % (cp[0], cp[1]))
    w("  %-26s %7s %6s %8s %8s" % ("section", "impr", "clicks", "position", "before"))
    for x in s["page_types"]:
        if x["impressions"] == 0 and x["clicks"] == 0:
            continue
        pos = x["position"] if x["position"] is not None and 1 <= x["position"] <= 200 else "-"
        w("  %-26s %7s %6d %8s %8s" % (str(x["key"])[:26], format(x["impressions"], ",d"), x["clicks"], pos,
                                      x["position_before"] if x["position_before"] is not None else "-"))
    w("\n  Intents are not subtracted: the Queries sheet lists only %s%% and %s%% of the impressions,\n"
      "  because Search Console withholds rare queries and stops at 1,000 rows, so the difference\n"
      "  would mostly measure which queries made the list." % (cq[0], cq[1]))


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
    if r["redirected"]:
        w("\nURLs with impressions that the Worker already redirects (RETIRED in src/worker.mjs); nothing\n"
          "to do, and they fade as Google recrawls them:")
        for x in r["redirected"]:
            w("  %5d impr  pos %5.1f  %s -> %s" % (x["impressions"], x["position"], x["url"], x["to"]))
    if not r["not_built_checked"]:
        w("\nNo built site in this checkout, so URLs were not checked; run python3 src/build.py first.")
    elif r["not_built"]:
        w("\nURLs with impressions that this build does NOT produce and nothing redirects (add them to\n"
          "RETIRED in src/worker.mjs):")
        for x in r["not_built"]:
            w("  %5d impr  pos %5.1f  %s" % (x["impressions"], x["position"], x["url"]))
    else:
        w("\nEvery other URL with impressions is produced by this build.")


def main(argv):
    opts = {"--json", "--since"}
    args = [a for i, a in enumerate(argv) if not a.startswith("--") and (i == 0 or argv[i - 1] not in opts)]
    if not args:
        raise SystemExit(__doc__)
    r = report(args[0])
    show(r)
    if "--since" in argv:
        r["since"] = since(args[0], argv[argv.index("--since") + 1])
        show_since(r["since"])
    if "--json" in argv:
        i = argv.index("--json")
        dest = pathlib.Path(argv[i + 1])
        dest.write_text(json.dumps(r, indent=1) + "\n")
        print("\nwrote %s" % dest)


if __name__ == "__main__":
    main(sys.argv[1:])
