"""LSAC's LSAT percentile table, read from the page that prints it.

    python3 src/lsat_percentiles.py --write   rebuild data/lsat_percentiles.json from LSAC's pages
    python3 src/lsat_percentiles.py --check   re-read the table and report any difference

The LSAT calculator shows, for every score from 120 to 180, the percentage of test scores
lower than it across the three testing years LSAC's table covers. The table comes from
LSAC's Data Library; the scale, what a score report's percentile rank means and when LSAC
updates it come from LSAC's LSAT Scoring page, and what a score band is from its LSAT
Score Bands page. Nothing in the data file is typed: --write parses the table and quotes
each sentence it relies on only if the page prints it word for word.

LSAC says percentiles are updated every year by the end of July, so the weekly source job
runs --check, which fails when a cell, a row or the testing years no longer match. LSAC's
pages send a Last-Modified header that is the time of the request, so the table is dated by
the testing years it names rather than by that header. Exit codes: 0 in step, 1 different,
2 unreadable.
"""
import html
import json
import pathlib
import re
import sys
import urllib.request

D = pathlib.Path(__file__).parent
ROOT = D.parent
sys.path.insert(0, str(D))
from check_sources import UA, ssl_context

OUT = ROOT / "data" / "lsat_percentiles.json"
TABLE = "https://www.lsac.org/data-research/data/lsat-percentiles"
SCORING = "https://www.lsac.org/lsat/lsat-scoring"
BANDS = "https://www.lsac.org/lsat/lsat-scoring/lsat-score-bands"
HEADER = ["LSAT Score", "Percent Below (Hundredths)", "Percent Below (Tenths)",
          "Percent Below (Whole Numbers)"]
WINDOW = re.compile(r"This table of percentiles shows the distribution of LSAT scores for the "
                    r"(\d{4}-\d{4}), (\d{4}-\d{4}), and (\d{4}-\d{4}) testing years\.")
DEFINITION = ("The percentile rank for any given test score, reported in the second through "
              "fourth columns of the table, is the percentage of test scores that are lower than "
              "the given scaled score.")
SCALE = ("The LSAT scale ranges from 120 to 180, with 120 being the lowest possible score and "
         "180 being the highest possible score.")
REPORT = ("Your percentile rank , which reflects the percentage of test takers whose scores "
          "were lower than yours during the previous three testing years.")
UPDATED = "Note that percentiles for all reported scores will be updated every year by the end of July."
YEARS = "LSAT testing years run from July 1 through June 30."
BAND = ("The score band indicates a range of scores , including scores slightly higher and "
        "slightly lower than the score received, because a test taker’s actual proficiency "
        "in the skills tested on the LSAT may be slightly higher or slightly lower than that "
        "reflected by the score received on an officially administered LSAT.")
CELL = {"hundredths": re.compile(r"^\d{1,2}\.\d{2}%$"), "tenths": re.compile(r"^\d{1,2}\.\d%$"),
        "whole": re.compile(r"^\d{1,2}%$")}


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=60, context=ssl_context()) as r:
        return r.read().decode("utf-8", errors="replace")


def plain(fragment):
    fragment = re.sub(r"<script.*?</script>|<style.*?</style>", " ", fragment, flags=re.S)
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", fragment)))


def parse(page):
    """The table, the testing years and the definition, or a list of what did not parse."""
    body = re.sub(r"<script.*?</script>|<style.*?</style>", " ", page, flags=re.S)
    text = plain(body)
    bad = []
    tables = re.findall(r"<table.*?</table>", body, flags=re.S)
    if len(tables) != 1:
        return None, ["expected one table, found %d" % len(tables)]
    rows = []
    for tr in re.findall(r"<tr.*?</tr>", tables[0], flags=re.S):
        rows.append([plain(c).strip() for c in re.findall(r"<t[hd][^>]*>(.*?)</t[hd]>", tr, flags=re.S)])
    if rows[0] != HEADER:
        bad.append("the table's header changed: %r" % rows[0])
    ranks = {}
    for row in rows[1:]:
        if len(row) != 4 or not all(CELL[k].match(c) for k, c in zip(CELL, row[1:])):
            bad.append("an unexpected row: %r" % row)
            continue
        ranks[row[0]] = {k: c.rstrip("%") for k, c in zip(CELL, row[1:])}
    if list(ranks) != [str(s) for s in range(180, 119, -1)]:
        bad.append("the rows are not every score from 180 down to 120")
    m = WINDOW.search(text)
    if not m:
        bad.append("the page no longer names the three testing years it covers")
    if DEFINITION not in text:
        bad.append("the page no longer prints its definition word for word")
    return {"window": list(m.groups()) if m else None, "ranks": ranks}, bad


def write(read_date):
    data, bad = parse(fetch(TABLE))
    scoring = plain(fetch(SCORING))
    for q in (SCALE, REPORT, UPDATED, YEARS):
        if q not in scoring:
            bad.append("the LSAT Scoring page no longer prints %r" % q[:60])
    if BAND not in plain(fetch(BANDS)):
        bad.append("the LSAT Score Bands page no longer prints its band sentence")
    if bad:
        sys.exit("lsat_percentiles: " + "; ".join(bad))
    scoring_ref = {"src": "LSAC", "year": int(read_date[:4]), "url": SCORING, "title": "LSAT Scoring"}
    out = {
        "what": "LSAC's LSAT percentile table: for every score from 120 to 180, the percentage of "
                "test scores lower than it in the three testing years the table covers.",
        "src": "LSAC", "year": int(read_date[:4]), "url": TABLE, "title": "LSAT Percentiles",
        "read": read_date,
        "window": data["window"],
        "definition": DEFINITION,
        "ranks": data["ranks"],
        "scale": dict(text=SCALE, **scoring_ref),
        "report": dict(text=REPORT.replace("rank ,", "rank,") + " " + UPDATED, **scoring_ref),
        "years": dict(text=YEARS, **scoring_ref),
        "band": dict(text=BAND.replace("scores ,", "scores,").replace("’", "'"), src="LSAC",
                     year=int(read_date[:4]), url=BANDS, title="LSAT Score Bands"),
    }
    s = json.dumps(out, indent=1, ensure_ascii=False)
    if "—" in s or "–" in s:
        sys.exit("lsat_percentiles: the data file would carry a dash")
    OUT.write_text(s + "\n")
    print("wrote %s: %d scores, testing years %s" % (OUT.relative_to(ROOT), len(data["ranks"]),
                                                     ", ".join(data["window"])))


def check():
    have = json.loads(OUT.read_text())
    try:
        page = fetch(have["url"])
    except Exception as e:  # noqa: BLE001 - any failure to read is reported, not raised
        print("could not read %s (%s: %s)" % (have["url"], type(e).__name__, e))
        return 2
    data, bad = parse(page)
    if data:
        if data["window"] != have["window"]:
            bad.append("the table now covers %s, not %s" % (data["window"], have["window"]))
        diff = [k for k in sorted(set(have["ranks"]) | set(data["ranks"]), key=int, reverse=True)
                if have["ranks"].get(k) != data["ranks"].get(k)]
        if diff:
            bad.append("percentiles changed at %d scores, e.g. %s: %s now %s"
                       % (len(diff), diff[0], have["ranks"].get(diff[0]), data["ranks"].get(diff[0])))
    for line in bad:
        print("  " + line)
    print("LSAT percentile table: %s" % ("changed on LSAC's page; run python3 src/lsat_percentiles.py "
          "--write and read the diff" if bad else "in step with LSAC's page"))
    return 1 if bad else 0


if __name__ == "__main__":
    if "--write" in sys.argv:
        import datetime
        write(datetime.date.today().isoformat())
    elif "--check" in sys.argv:
        sys.exit(check())
    else:
        sys.exit(__doc__)
