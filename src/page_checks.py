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
