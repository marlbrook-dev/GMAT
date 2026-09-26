"""Checks each exam fact's figures against the page it cites (INC-0130).

    python3 src/check_sources.py              fetch every cited source and report
    python3 src/check_sources.py --cache DIR  keep what was fetched in DIR between runs
    python3 src/check_sources.py --render     read pages built by JavaScript in Chromium

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


def numbers(text, words=False):
    text = str(text or "")
    out = {norm(n) for n in NUM.findall(text)}
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


def check(fact, source_nums):
    """The numbers in a fact that its source does not print, as (number, why)."""
    derived = fact.get("derived") or {}
    want = numbers(fact.get("text")) | numbers(fact.get("note"))
    if isinstance(fact.get("v"), (int, float)):
        want.add(norm("%g" % fact["v"]))
    missing = []
    for n in sorted(want, key=lambda x: float(x)):
        if n in source_nums:
            continue
        if n in derived:
            if str(derived[n]).startswith("count:"):
                continue
            inputs = numbers(derived[n]) - {n}
            gone = sorted(inputs - source_nums, key=float)
            if gone:
                missing.append((n, "derived from %s, which the source does not print"
                                % ", ".join(gone)))
            continue
        missing.append((n, "not in the source"))
    return missing


def main(argv):
    cache = None
    if "--cache" in argv:
        cache = pathlib.Path(argv[argv.index("--cache") + 1])
        cache.mkdir(parents=True, exist_ok=True)
    exams = json.loads(EXAMS.read_text())
    todo = facts(exams)
    sources, unread = {}, {}
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
        except Exception as e:
            unread[url] = "%s: %s" % (type(e).__name__, e)
    bad = 0
    for slug, where, f in todo:
        if f["url"] not in sources:
            continue
        miss = check(f, sources[f["url"]])
        if miss:
            bad += 1
            print("%s.%s  %s" % (slug, where, f["url"]))
            print("    %s" % str(f.get("text") or f.get("v"))[:220])
            for n, why in miss:
                print("    %s: %s" % (n, why))
    for url, why in sorted(unread.items()):
        print("could not read %s (%s)" % (url, why))
    print("\n%d facts checked against %d sources; %d with a number their source does not "
          "print; %d sources unreadable" % (len(todo), len(sources), bad, len(unread)))
    return 1 if bad else (2 if unread else 0)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
