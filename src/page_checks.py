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
"""
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
