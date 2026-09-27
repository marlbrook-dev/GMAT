"""Checks that read built pages, shared by the builders that write them.

python_reprs() looks for a Python data structure printed into a page. The /exams/ hub's
structured data described every exam as "Scored {'text': ..., 'src': 'GMAC', ...}"
because an f-string was handed a sourced record where its text was meant, and Python
formats a dict without complaint (INC-0131). Nothing on the site has a reason to contain
a printed dict, so finding one anywhere is a failure. Ordinary scripts are skipped,
because JavaScript can quote an object key, but structured data is not: it is where the
mistake was, and it is published text that no one sees rendered.

articles() looks for "a" or "an" before a number that is spoken the other way. MIT
Sloan's page read "a 18.8% acceptance rate" because a template chose the article before it
knew the number (INC-0134). article_for() is how a template should choose it instead.

trainer_claims() looks for a sentence calling a live trainer unfinished. The /exams/ hub's
meta description said only two trainers were live, eleven days after all five were
(INC-0138); a queued post said the same of the LSAT (INC-0137).

undefined_tokens() looks for a design token a page uses but never defines. The blog pasted
the shared header's CSS without the tokens it reads, and CSS let every one of them fall
back to nothing without a word, so the logo sat against the screen edge (INC-0139).

offsite_scripts() looks for a script loaded from another host. The trainer app loaded
supabase-js from cdn.jsdelivr.net ahead of its own code, so none of the app ran until
jsdelivr answered, and a slow response timed out CI's games smoke (INC-0148). Code a page
needs is served from this site, as /vendor/ now serves that library.

offsite_styles() does the same for stylesheets and fonts, following @import through every
stylesheet on this site a page links. Each page used to ask Google Fonts for its own list of
weights, so the shared header's 700 weight drew as 600 on the pages whose list stopped at
600 (INC-0163). The faces are served from /vendor/ through one stylesheet, and a page that
loads a font or stylesheet from anywhere else, or links one of ours that is not there, fails
the build.

untitled_headings() looks for an h1, h2 or h3 that breaks the house Title Case rule. The
blog build checked the headings inside each post (INC-0171), and the blog template's own
"Keep reading", the trainer app's "Review your section" and the test date pages' "When is
the next LSAT?" went unread, because no check looked at the pages as built (INC-0176).
title_case() is the rule, shared with the blog build. A heading a script assembles has no
fixed text to check, and a school's or college's name is a proper name, so both are left out.
"""
import html
import json
import pathlib
import re

# A quoted key followed by a colon and a space, which is how Python prints a dict and not
# how anyone writes prose, JSON or HTML.
_REPR = re.compile(r"""\{'[A-Za-z_][\w ]*': |, '(?:text|src|year|url|v|note)': """)
_CODE = re.compile(r"<script(?![^>]*application/ld\+json)[^>]*>[\s\S]*?</script>", re.I)


def python_reprs(root, paths):
    """[(page, fragment)] for every built page under `paths` that prints a Python dict."""
    root = pathlib.Path(root)
    found = []
    for rel in paths:
        base = root / rel
        pages = [base] if base.is_file() else sorted(base.rglob("*.html")) if base.is_dir() else []
        for page in pages:
            text = _CODE.sub(" ", page.read_text(encoding="utf-8", errors="replace"))
            m = _REPR.search(text)
            if m:
                found.append((page.relative_to(root).as_posix(),
                              text[max(0, m.start() - 40):m.end() + 40].replace("\n", " ")))
    return found


# A number is spoken with a leading vowel sound when it begins "eight" (8, 8.5, 80 to 89,
# 800, 8,000), or is eleven or eighteen on their own or before "thousand" (11, 11.3,
# 11,000, 18, 18.8). 1100 to 1199 and 1800 to 1899 can be read either way ("eleven
# hundred" or "one thousand one hundred"), so either article passes for those.
_ART = re.compile(r"\b(a|an) \$?(\d[\d,]*(?:\.\d+)?)(?![\d])")
_TAG = re.compile(r"<[^>]+>")
_STYLE = re.compile(r"<style[^>]*>[\s\S]*?</style>", re.I)


def vowel_sound(num):
    """True when the number as written is spoken with a leading vowel sound, False when it
    is not, None when it can honestly be read either way."""
    whole = str(num).lstrip("$").split(".")[0]
    if whole.startswith("8"):
        return True
    if whole.split(",")[0] in ("11", "18"):
        return True
    if len(whole) == 4 and whole[:2] in ("11", "18"):
        return None
    return False


def article_for(num):
    """The indefinite article a number takes: 'an 18.8% rate', 'a 19% rate'."""
    return "an" if vowel_sound(num) else "a"


def articles(root, paths):
    """[(page, fragment)] for every built page under `paths` that puts 'a' before a number
    spoken with a vowel sound, or 'an' before one spoken without. Reads the text a visitor
    or a search engine sees: tags, styles and ordinary scripts are dropped, structured
    data is kept."""
    import html
    root = pathlib.Path(root)
    found = []
    for rel in paths:
        base = root / rel
        pages = [base] if base.is_file() else sorted(base.rglob("*.html")) if base.is_dir() else []
        for page in pages:
            raw = page.read_text(encoding="utf-8", errors="replace")
            text = html.unescape(_TAG.sub(" ", _STYLE.sub(" ", _CODE.sub(" ", raw))))
            text = re.sub(r"\s+", " ", text)
            for m in _ART.finditer(text):
                v = vowel_sound(m.group(2))
                if v is None or m.group(1) == ("an" if v else "a"):
                    continue
                found.append((page.relative_to(root).as_posix(),
                              text[max(0, m.start() - 40):m.end() + 30]))
                break
    return found


# Words that call something unfinished. A sentence with one of these and the name of an exam
# whose trainer is live is a stale claim about the product (INC-0137, INC-0138).
NOT_LIVE = re.compile(r"in development|coming soon|wait ?list|not (?:yet )?live", re.I)
_META = re.compile(r'<meta\s+name="description"\s+content="([^"]*)"', re.I)
_BLOCK = re.compile(r"</?(?:p|li|ul|ol|div|h[1-6]|td|th|tr|table|section|nav|header|footer|main|"
                    r"article|aside|details|summary|button|label|option|select|br|script)\b[^>]*>", re.I)


def stale_sentences(text, names):
    """Sentences in `text` that call one of the live exams in `names` unfinished."""
    out = []
    for sentence in re.split(r"(?<=[.!?])\s+", re.sub(r"\s+", " ", text)):
        if NOT_LIVE.search(sentence) and any(re.search(r"\b%s\b" % re.escape(n), sentence) for n in names):
            out.append(sentence.strip())
    return out


def trainer_claims(root, paths, names):
    """[(page, sentence)] for every built page whose text or meta description calls a live
    trainer unfinished. Ordinary scripts are skipped, as elsewhere here."""
    import html
    root = pathlib.Path(root)
    found = []
    for rel in paths:
        base = root / rel
        pages = [base] if base.is_file() else sorted(base.rglob("*.html")) if base.is_dir() else []
        for page in pages:
            raw = page.read_text(encoding="utf-8", errors="replace")
            # Block elements end a sentence; inline ones (a link inside a paragraph) do not.
            # Without this the header's menu reads as one run-on sentence in which "Law
            # Schools, Coming Soon" sits beside "LSAT, Live".
            body = _BLOCK.sub("\n", _STYLE.sub(" ", _CODE.sub(" ", raw)))
            parts = _META.findall(raw) + _TAG.sub(" ", body).split("\n")
            hits = [h for part in parts for h in stale_sentences(html.unescape(part), names)]
            if hits:
                found.append((page.relative_to(root).as_posix(), hits[0][:200]))
    return found


_STYLE_BLOCK = re.compile(r"<style[^>]*>([\s\S]*?)</style>", re.I)
_SHEET = re.compile(r'<link[^>]+rel="stylesheet"[^>]+href="(/[^"]+)"|<link[^>]+href="(/[^"]+)"[^>]+rel="stylesheet"', re.I)


def undefined_tokens(root, paths, tokens):
    """[(page, [token, ...])] for every built page whose CSS uses one of `tokens` with no
    fallback, var(--x) rather than var(--x, y), and defines it nowhere: not inline, not in
    a local stylesheet it links."""
    root = pathlib.Path(root)
    found = []
    for rel in paths:
        base = root / rel
        pages = [base] if base.is_file() else sorted(base.rglob("*.html")) if base.is_dir() else []
        for page in pages:
            raw = page.read_text(encoding="utf-8", errors="replace")
            css = "\n".join(_STYLE_BLOCK.findall(raw))
            for a, b in _SHEET.findall(raw):
                sheet = root / (a or b).lstrip("/").split("?")[0]
                if sheet.is_file():
                    css += "\n" + sheet.read_text(encoding="utf-8", errors="replace")
            used = set(re.findall(r"var\((--[a-z0-9-]+)\)", css)) & set(tokens)
            missing = sorted(used - set(re.findall(r"(--[a-z0-9-]+)\s*:", css)))
            if missing:
                found.append((page.relative_to(root).as_posix(), missing))
    return found


_OFFSITE = re.compile(r"""<script\b[^>]*\bsrc\s*=\s*["']?((?:https?:)?//[^"'\s>]+)""", re.I)


def offsite_scripts(root, paths):
    """[(page, url)] for every built page under `paths` that loads a script from another host."""
    root = pathlib.Path(root)
    found = []
    for rel in paths:
        base = root / rel
        pages = [base] if base.is_file() else sorted(base.rglob("*.html")) if base.is_dir() else []
        for page in pages:
            for m in _OFFSITE.finditer(page.read_text(encoding="utf-8", errors="replace")):
                found.append((page.relative_to(root).as_posix(), m.group(1)))
    return found


_LINK_TAG = re.compile(r"<link\b[^>]*>", re.I)
_LINK_REL = re.compile(r"""\brel\s*=\s*["']?([^"'>]+)""", re.I)
_LINK_HREF = re.compile(r"""\bhref\s*=\s*["']?([^"'\s>]+)""", re.I)
_CSS_IMPORT = re.compile(r"""@import\s+(?:url\(\s*)?["']?([^"')\s;]+)""", re.I)
_CSS_URL = re.compile(r"""url\(\s*["']?([^"')\s]+)""", re.I)
_ELSEWHERE = re.compile(r"^(?:[a-z][a-z0-9+.-]*:)?//", re.I)


def _local(root, base_dir, ref):
    """The file a reference on this site names, resolved from the directory it appears in."""
    import posixpath
    ref = ref.split("#")[0].split("?")[0]
    path = ref if ref.startswith("/") else posixpath.join(base_dir, ref)
    return pathlib.Path(root) / posixpath.normpath(path).lstrip("/")


def _sheet_problems(root, sheet, seen, cache):
    """Problems in one stylesheet on this site and every stylesheet it imports."""
    key = sheet.as_posix()
    if key in cache:
        return cache[key]
    if key in seen:
        return []
    seen.add(key)
    rel = "/" + sheet.relative_to(root).as_posix()
    if not sheet.is_file():
        cache[key] = ["links %s, which is not there" % rel]
        return cache[key]
    css = sheet.read_text(encoding="utf-8", errors="replace")
    here = rel.rsplit("/", 1)[0] + "/"
    out = []
    imports = set(_CSS_IMPORT.findall(css))
    for ref in sorted(imports | set(_CSS_URL.findall(css))):
        if ref.startswith("data:"):
            continue
        if _ELSEWHERE.match(ref):
            out.append("%s loads %s from another host" % (rel, ref))
        elif ref in imports:
            out += _sheet_problems(root, _local(root, here, ref), seen, cache)
        elif not _local(root, here, ref).is_file():
            out.append("%s names %s, which is not there" % (rel, ref))
    cache[key] = out
    return out


def offsite_styles(root, paths):
    """[(page, problem)] for every built page under `paths` that loads a stylesheet or a font
    from another host, in a link tag, in its own CSS, or through @import in a stylesheet of
    ours it links; or that links a stylesheet of ours, or names a file from one, that is not
    there."""
    root = pathlib.Path(root)
    found, cache = [], {}
    for rel in paths:
        base = root / rel
        pages = [base] if base.is_file() else sorted(base.rglob("*.html")) if base.is_dir() else []
        for page in pages:
            raw = page.read_text(encoding="utf-8", errors="replace")
            name = page.relative_to(root).as_posix()
            here = "/" + name.rsplit("/", 1)[0] + "/" if "/" in name else "/"
            problems = []
            for tag in _LINK_TAG.findall(raw):
                rel_m, href_m = _LINK_REL.search(tag), _LINK_HREF.search(tag)
                if not rel_m or not href_m:
                    continue
                kinds = rel_m.group(1).lower().split()
                href = href_m.group(1)
                if "stylesheet" not in kinds and "preload" not in kinds:
                    continue
                if _ELSEWHERE.match(href):
                    problems.append("loads %s from another host" % href)
                elif "stylesheet" in kinds and not href.startswith("data:"):
                    problems += _sheet_problems(root, _local(root, here, href), set(), cache)
            css = "\n".join(_STYLE_BLOCK.findall(raw))
            for ref in sorted(set(_CSS_IMPORT.findall(css)) | set(_CSS_URL.findall(css))):
                if _ELSEWHERE.match(ref):
                    problems.append("loads %s from another host in its own CSS" % ref)
            for pr in dict.fromkeys(problems):
                found.append((name, pr))
    return found


def _selfcheck_offsite_styles():
    """INC-0163: a Google Fonts link, an @import of it from a stylesheet of ours, and a
    stylesheet of ours that is missing are each reported; a page on the site's own font
    stylesheet is not."""
    import tempfile
    with tempfile.TemporaryDirectory() as d:
        d = pathlib.Path(d)
        (d / "vendor" / "f").mkdir(parents=True)
        (d / "vendor" / "f" / "a.woff2").write_bytes(b"wOF2")
        (d / "vendor" / "f" / "fonts.css").write_text("@font-face{src:url(a.woff2)}")
        (d / "css").mkdir()
        (d / "css" / "g.css").write_text("@import url('https://fonts.googleapis.com/css2?family=X');")
        (d / "css" / "ok.css").write_text("@import url('../vendor/f/fonts.css');")
        pages = {
            "good.html": '<link rel="stylesheet" href="/vendor/f/fonts.css"><link rel="stylesheet" href="/css/ok.css">',
            "google.html": '<link href="https://fonts.googleapis.com/css2?family=X" rel="stylesheet">',
            "imported.html": '<link rel="stylesheet" href="/css/g.css">',
            "missing.html": '<link rel="stylesheet" href="/vendor/old/fonts.css">',
            "inline.html": "<style>@import url(https://fonts.googleapis.com/css2?family=X);</style>",
        }
        for n, body in pages.items():
            (d / n).write_text("<head>%s</head>" % body)
        got = {p for p, _ in offsite_styles(d, list(pages))}
        want = {"google.html", "imported.html", "missing.html", "inline.html"}
        if got != want:
            raise SystemExit("page_checks: offsite_styles self-check flagged %s, expected %s"
                             % (sorted(got), sorted(want)))



SMALL_WORDS = frozenset("a an the of and or to for by in on at vs".split())
_LEAD = re.compile(r"^([^A-Za-z0-9]*)([A-Za-z]+)(.*)$")


def title_case(h):
    """A heading in the house Title Case. A word that already carries a capital (GMAT,
    GMAC's, iPad) keeps its letters; an all lower case word is capitalised, and a small
    word is lowered anywhere but first, last, or first after a colon, a question mark, an
    exclamation mark or a numbered prefix such as "1." (INC-0176). Hyphenated parts are
    treated as words, and the first part of a compound is capitalised whatever it is. A
    single capital with a full stop is an initial ("Richard A. Chaifetz"), and a small word
    joined to more letters by & is part of a name ("Texas A&M"): both keep their letters."""
    toks = h.split(" ")
    last = max((i for i, t in enumerate(toks) if re.search(r"[A-Za-z0-9]", t)), default=-1)
    out, first = [], True
    for i, tok in enumerate(toks):
        parts = tok.split("-")
        for j, part in enumerate(parts):
            m = _LEAD.match(part)
            if not m:
                continue
            pre, word, rest = m.groups()
            edge = (first and j == 0) or (i == last and j == len(parts) - 1)
            # The first part of a hyphenated compound is capitalised whatever it is:
            # "On-Screen", not "on-Screen".
            lead = len(parts) > 1 and j == 0
            named = (len(word) == 1 and word.isupper() and rest.startswith(".")) or rest[:1] == "&"
            if word.lower() in SMALL_WORDS and not edge and not lead and not named:
                word = word.lower()
            elif word.islower():
                word = word[0].upper() + word[1:]
            parts[j] = pre + word + rest
        out.append("-".join(parts))
        if re.search(r"[A-Za-z0-9]", tok):
            first = tok.endswith((":", "?", "!")) or bool(re.fullmatch(r"\d+[.)]", tok))
    return " ".join(out)


_HEADING = re.compile(r"<(h[1-3])\b[^>]*>([\s\S]*?)</\1\s*>", re.I)
# Concatenation or a template placeholder: a heading built by a script from parts.
_ASSEMBLED = re.compile(r"""['"`]\s*\+|\+\s*['"`]|\$\{|\{\{""")


def entity_names(root):
    """The names of every school and college in the data, which are proper names and keep
    their own capitals ("Universidad del Sagrado Corazon")."""
    root = pathlib.Path(root)
    names = set()
    for d in ("schools", "colleges"):
        for f in sorted((root / "data" / d).glob("*.json")):
            rec = json.loads(f.read_text())
            names.update(n for n in (rec.get("name"), rec.get("university")) if n)
    return names


# Names whose capitals are their own, whatever the rule would make of them: the blog's name.
PROPER = ("The Study Room",)


def untitled_headings(root, paths, names=()):
    """(page, heading, as it should read) for each h1, h2 or h3 on the built pages under
    paths that breaks the Title Case rule, headings written into a script's strings
    included, since the trainer app draws most of its own."""
    root = pathlib.Path(root)
    out = []
    for rel in paths:
        base = root / rel
        files = [base] if base.is_file() else sorted(base.rglob("*.html")) if base.is_dir() else []
        for f in files:
            for m in _HEADING.finditer(f.read_text(errors="replace")):
                inner = m.group(2)
                if _ASSEMBLED.search(inner):
                    continue
                h = re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", "", inner))).strip()
                if not h or h in names:
                    continue
                want = title_case(h)
                for name in PROPER:
                    if name in h:
                        want = re.sub(re.escape(name), name, want, flags=re.I)
                if want != h:
                    out.append((str(f.relative_to(root)), h, want))
    return out


def _selfcheck_title_case():
    """INC-0171 and INC-0176: the rule's own examples, a small word at each end, after a
    colon, a question mark or a numbered prefix, and the initials and names it keeps."""
    cases = {
        "What does GMAC's retake policy allow?": "What Does GMAC's Retake Policy Allow?",
        "Submit Early, On Purpose": "Submit Early, on Purpose",
        "What Are the ACT Percentiles for 2026?": "What Are the ACT Percentiles for 2026?",
        "MBA Salary by School: the Class of 2025": "MBA Salary by School: The Class of 2025",
        "Where to begin": "Where to Begin",
        "What is a two-minute rule for?": "What Is a Two-Minute Rule For?",
        "11th Grade": "11th Grade",
        "How should you use the on-screen calculator?": "How Should You Use the On-Screen Calculator?",
        "Day-to-day review": "Day-to-Day Review",
        "Should You Retake the GMAT? A Decision Framework": "Should You Retake the GMAT? A Decision Framework",
        "1. The Short Version": "1. The Short Version",
        "Raymond A. Mason School of Business": "Raymond A. Mason School of Business",
        "Texas A&M University-Kingsville": "Texas A&M University-Kingsville",
        "Keep reading": "Keep Reading",
        "GMAT vs. the GRE": "GMAT vs. the GRE",
    }
    for h, want in cases.items():
        if title_case(h) != want:
            raise SystemExit("page_checks: title_case(%r) gave %r, expected %r (INC-0176)" % (h, title_case(h), want))
    import tempfile
    with tempfile.TemporaryDirectory() as d:
        page = pathlib.Path(d) / "p.html"
        page.write_text("<h1>Frequently asked questions</h1><h2>Keep Reading</h2><h2>Introducing The Study Room</h2>"
                        "<script>x='<h2>'+esc(t)+'</h2>'; y='<h3>Review your section</h3>';</script>"
                        "<h2>Universidad del Sagrado Corazon</h2>")
        got = [h for _, h, _ in untitled_headings(d, ["p.html"], {"Universidad del Sagrado Corazon"})]
        if got != ["Frequently asked questions", "Review your section"]:
            raise SystemExit("page_checks: untitled_headings found %r (INC-0176)" % got)
