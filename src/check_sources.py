"""Checks each exam fact's figures against the page it cites (INC-0130).

    python3 src/check_sources.py              fetch every cited source and report
    python3 src/check_sources.py --cache DIR  keep what was fetched in DIR between runs
    python3 src/check_sources.py --render     read pages built by JavaScript in Chromium
    python3 src/check_sources.py --schools    check the MBA school library instead

The school library cites a College Scorecard figure to the Scorecard's data page, which
offers the dataset rather than printing any one school's numbers, so those figures are
counted and set aside: checking them means reading the dataset, not the page.

validate_exams.py proves that every published exam figure names a source, a year and a
URL. It cannot prove the source says it, and the GRE guide credited ETS with a combined
260 to 340 score that the ETS page it cited never mentions (INC-0130). This fetches every
page or PDF that data/exams.json cites and reports each number in a fact that its source
does not contain.

A fact may carry numbers it derives by arithmetic on its source, stated with the working:

    "derived": {"171": "50 + 45 + 36 + 40, the section question counts"}

A derived number is not looked for itself; the numbers in its working are, so the
arithmetic has to rest on figures the source prints. A number counted off the page, such
as the entries in a list, says so: "count: the US schools listed, counted 2026-09-26". What this finds is a report for a
person rather than a fix: a miss can be a paraphrase (five for 5) as easily as a wrong
figure, and only reading the source tells which.

It needs the network, so it runs in the weekly audit rather than in the build.
"""
import datetime
import hashlib
import html
import io
import json
import os
import pathlib
import re
import ssl
import sys
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parent.parent
EXAMS = ROOT / "data" / "exams.json"
SCHOOLS = ROOT / "data" / "schools"
# Where a fact keeps numbers its source must print. An exam fact's note carries sourced
# detail (a fee's regional prices); a school figure's note is our own commentary, such as
# why a score must be on the classic scale, so --schools leaves it out.
FIELDS = ["text", "note", "stat"]
UA = "Mozilla/5.0 (compatible; StartFromNowhere source check; +https://startfromnowhere.com)"
# A number as a fact writes it: thousands commas allowed, decimals allowed. The commas are
# dropped before comparing, so 2,004,965 on the page matches 2004965 anywhere.
NUM = re.compile(r"(?<![\w.])\d{1,3}(?:,\d{3})+(?:\.\d+)?|(?<![\w.,])\d+(?:\.\d+)?")
# Sources write small numbers as words ("up to five times"), and a fact that writes 5 is
# saying the same thing, so the words count as their numbers on the source side.
WORDS = {w: str(i) for i, w in enumerate(
    "zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen "
    "fifteen sixteen seventeen eighteen nineteen twenty".split())}
WORDS.update({"thirty": "30", "forty": "40", "fifty": "50", "sixty": "60", "seventy": "70",
              "eighty": "80", "ninety": "90", "hundred": "100", "once": "1", "twice": "2"})
# A page that yields less readable text than this served a bot challenge or builds itself
# with JavaScript, and a number missing from it says nothing about the fact.
MIN_TEXT = 400


def norm(n):
    n = n.replace(",", "")
    return n.rstrip("0").rstrip(".") if "." in n else n


# "2026-27" names two years; the page may print "2026-2027", so both are read in full.
SPAN = re.compile(r"\b((?:19|20)(\d\d))[-/](\d\d)\b")


# "$175K" and "$47 M" are 175000 and 47000000 on the page, and a fact records them in full.
SUFFIX = re.compile(r"(\d[\d,]*(?:\.\d+)?)\s?([kKmM])\b")
# "$30-70 k" puts the suffix on both ends of the range.
RANGE_SUFFIX = re.compile(r"(\d[\d,]*(?:\.\d+)?)\s?[\u2013\u2014-]\s?\d[\d,]*(?:\.\d+)?\s?([kKmM])\b")
# Constants a derivation may use that no source needs to print: months in a year and the
# base of a percentage.
UNIT = {"12", "100"}


def numbers(text, words=False):
    text = SPAN.sub(lambda m: "%s %s%s" % (m.group(1), m.group(1)[:2], m.group(3)), str(text or ""))
    out = {norm(n) for n in NUM.findall(text)}
    for n, unit in SUFFIX.findall(text) + RANGE_SUFFIX.findall(text):
        out.add(norm("%.6f" % (float(n.replace(",", "")) * (1000 if unit in "kK" else 1000000))))
    if words:
        out |= {WORDS[w] for w in re.findall(r"[a-z]+", text.lower()) if w in WORDS}
    return out


def facts(exams):
    """(slug, where, fact) for every published figure that cites a URL."""
    out = []

    def walk(slug, where, o):
        if isinstance(o, dict):
            if o.get("url") and (o.get("text") is not None or o.get("v") is not None):
                out.append((slug, where, o))
            for k, v in o.items():
                walk(slug, "%s.%s" % (where, k) if where else k, v)
        elif isinstance(o, list):
            for i, v in enumerate(o):
                walk(slug, "%s[%d]" % (where, i), v)
    for e in exams:
        walk(e.get("slug"), "", e)
    return out


def ssl_context():
    for var in ("SSL_CERT_FILE", "REQUESTS_CA_BUNDLE"):
        if os.environ.get(var) and os.path.exists(os.environ[var]):
            return ssl.create_default_context(cafile=os.environ[var])
    if os.path.exists("/root/.ccr/ca-bundle.crt"):
        return ssl.create_default_context(cafile="/root/.ccr/ca-bundle.crt")
    return ssl.create_default_context()


def to_text(body, ctype):
    """The readable text of a fetched page or PDF."""
    if body[:5] == b"%PDF-" or "pdf" in ctype:
        try:
            from pdfminer.high_level import extract_text
        except ImportError:
            raise RuntimeError("a PDF, and pdfminer.six is not installed")
        return extract_text(io.BytesIO(body))
    t = body.decode("utf-8", errors="replace")
    t = re.sub(r"<(script|style|noscript)[\s\S]*?</\1>", " ", t, flags=re.I)
    return html.unescape(re.sub(r"<[^>]+>", " ", t))


RENDER_JS = r"""
const { chromium } = require('playwright');
// Under node -e the script has no file name, so its arguments start at argv[1].
const [, helper, url, ua] = process.argv;
const { chromiumPath } = require(helper);
(async () => {
  const b = await chromium.launch({ executablePath: chromiumPath() });
  const p = await b.newPage({ userAgent: ua });
  await p.goto(url, { waitUntil: 'networkidle', timeout: 60000 });
  process.stdout.write(await p.evaluate(() => document.body.innerText));
  await b.close();
})().catch(e => { console.error(String(e)); process.exit(1); });
"""


def render(url):
    """The page as a browser shows it, for a source that builds its text with JavaScript."""
    import subprocess
    r = subprocess.run(["node", "-e", RENDER_JS, "--", str(ROOT / "src" / "chromium_path.js"),
                        url, UA], capture_output=True, text=True, timeout=120,
                       cwd=str(ROOT))
    if r.returncode != 0:
        raise RuntimeError("could not render: " + (r.stderr.strip()[:200] or "no output"))
    return r.stdout


def fetch(url, cache, rendered=False):
    key = hashlib.sha1((("render:" if rendered else "") + url).encode()).hexdigest()
    if cache:
        hit = cache / (key + ".txt")
        if hit.exists():
            return hit.read_text(encoding="utf-8")
    if rendered:
        text = render(url)
    else:
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        with urllib.request.urlopen(req, timeout=45, context=ssl_context()) as r:
            text = to_text(r.read(), r.headers.get("Content-Type", "").lower())
    text = re.sub(r"\s+", " ", text)
    if cache:
        (cache / (key + ".txt")).write_text(text, encoding="utf-8")
    return text


def printed(fact):
    """The numbers a fact expects its source to print, leaving out the ones it derives."""
    want = set().union(*(numbers(fact.get(k)) for k in FIELDS))
    if isinstance(fact.get("v"), (int, float)):
        want.add(norm("%g" % fact["v"]))
    return want - set(fact.get("derived") or {})


def check(fact, source_nums):
    """The numbers in a fact that its source does not print, as (number, why)."""
    derived = fact.get("derived") or {}
    want = set().union(*(numbers(fact.get(k)) for k in FIELDS))
    if isinstance(fact.get("v"), (int, float)):
        want.add(norm("%g" % fact["v"]))
    missing = []
    for n in sorted(want, key=lambda x: float(x)):
        if n in source_nums:
            continue
        if n in derived:
            if str(derived[n]).startswith("count:"):
                continue
            inputs = numbers(derived[n]) - {n} - UNIT
            gone = sorted(inputs - source_nums, key=float)
            if gone:
                missing.append((n, "derived from %s, which the source does not print"
                                % ", ".join(gone)))
            continue
        missing.append((n, "not in the source"))
    return missing


# A page that describes itself as covering a year: "For the 2025-2026 testing year, the LSAT
# fee is $253." LSAC left that page up after the year ended, and a fact cited to it stayed
# wrong in words the number check could not see (INC-0136).
PERIOD = re.compile(r"\b[Ff]or the (\d{4})[-\u2013](\d{4}|\d{2}) (?:testing|academic|school|application|"
                    r"admissions|award|reporting) year\b")


def ended_periods(text, today):
    """The periods a page says it covers that ended before `today`, as 'YYYY-YYYY'. A
    testing or school year ends by June 30 of its second year."""
    out = set()
    for a, b in PERIOD.findall(text):
        end = int(b) if len(b) == 4 else int(a[:2] + b)
        if datetime.date(end, 6, 30) < today:
            out.add("%s-%d" % (a, end))
    return sorted(out)


def main(argv):
    cache = None
    if "--cache" in argv:
        cache = pathlib.Path(argv[argv.index("--cache") + 1])
        cache.mkdir(parents=True, exist_ok=True)
    if "--schools" in argv:
        records = [json.loads(p.read_text()) for p in sorted(SCHOOLS.glob("*.json"))]
        FIELDS[:] = ["text", "stat"]
    else:
        records = json.loads(EXAMS.read_text())
    todo = facts(records)
    dataset = [t for t in todo if "scorecard" in str(t[2].get("src", "")).lower()]
    todo = [t for t in todo if t not in dataset]
    sources, unread, periods = {}, {}, {}
    today = datetime.date.fromisoformat(os.environ.get("BLOG_BUILD_DATE") or datetime.date.today().isoformat())
    for url in sorted({f["url"] for _, _, f in todo}):
        try:
            text = fetch(url, cache)
            # A page that builds itself with JavaScript reads as nearly empty, or as
            # navigation without its figures, until a browser runs it. If the browser
            # cannot load it either, the static text is still evidence when there is
            # enough of it, so it is kept rather than thrown away.
            if "--render" in argv and (len(text) < MIN_TEXT or any(
                    check(f, numbers(text, True)) for _, _, f in todo if f["url"] == url)):
                try:
                    text = fetch(url, cache, rendered=True)
                except Exception as e:
                    print("render failed for %s, using the page as served (%s)"
                          % (url, str(e).splitlines()[0][:120]))
            if len(text) < MIN_TEXT:
                raise RuntimeError("only %d characters of text, a bot challenge or a page "
                                   "built by JavaScript" % len(text))
            sources[url] = numbers(text, words=True)
            periods[url] = ended_periods(text, today)
        except Exception as e:
            unread[url] = "%s: %s" % (type(e).__name__, e)
    # A page that prints none of the figures cited to it, when two or more are, has not
    # shown its data at all: a class profile drawn by JavaScript reads as prose with no
    # numbers until a browser runs it. Every figure on it would be reported as missing,
    # which says nothing about the figures, so the page is reported once instead.
    by_url = {}
    for _, _, f in todo:
        by_url.setdefault(f["url"], []).append(f)
    # Years do not count as evidence: "Class of 2027" is in the prose of a class profile
    # whose statistics never rendered.
    year = re.compile(r"(19|20)\d\d")
    evidence = lambda f: {n for n in printed(f) if not year.fullmatch(n)}
    blank = set()
    for u, fs in by_url.items():
        counted = [f for f in fs if evidence(f)]
        if u in sources and len(counted) >= 2 and not any(evidence(f) & sources[u] for f in counted):
            blank.add(u)
    bad = 0
    for slug, where, f in todo:
        if f["url"] not in sources or f["url"] in blank:
            continue
        miss = check(f, sources[f["url"]])
        if miss:
            bad += 1
            print("%s.%s  %s" % (slug, where, f["url"]))
            print("    %s" % str(f.get("text") or f.get("v"))[:220])
            for n, why in miss:
                print("    %s: %s" % (n, why))
    # The exam guides only: a school's fee page naming last year is the tuition queue's
    # business, and a reason to read the page rather than a fact about the exam.
    stale = 0
    if "--schools" not in argv:
        for slug, where, f in todo:
            ended = periods.get(f["url"]) or []
            seen = set((f.get("period_checked") or {}).get("periods") or [])
            if ended and not set(ended) <= seen:
                stale += 1
                print("%s.%s  %s" % (slug, where, f["url"]))
                print("    %s" % str(f.get("text") or f.get("v"))[:220])
                print("    the page says it covers the %s %s, which has ended: read the fact against a "
                      "current page, and if it still holds record that in its period_checked"
                      % (", ".join(ended), "year" if len(ended) == 1 else "years"))
    for url in sorted(blank):
        print("shows none of its %d figures, probably built by JavaScript: %s"
              % (len(by_url[url]), url))
    for url, why in sorted(unread.items()):
        print("could not read %s (%s)" % (url, why))
    print("\n%d facts checked against %d sources; %d with a number their source does not "
          "print; %d resting on a page about a period that has ended; %d sources unreadable, "
          "%d showing none of their figures%s"
          % (len(todo), len(sources), bad, stale, len(unread), len(blank),
          "; %d dataset figures set aside" % len(dataset) if dataset else ""))
    return 1 if bad or stale else (2 if unread else 0)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
