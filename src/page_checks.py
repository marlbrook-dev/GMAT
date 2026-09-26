"""Checks that read built pages, shared by the builders that write them.

python_reprs() looks for a Python data structure printed into a page. The /exams/ hub's
structured data described every exam as "Scored {'text': ..., 'src': 'GMAC', ...}"
because an f-string was handed a sourced record where its text was meant, and Python
formats a dict without complaint (INC-0131). Nothing on the site has a reason to contain
a printed dict, so finding one anywhere is a failure. Ordinary scripts are skipped,
because JavaScript can quote an object key, but structured data is not: it is where the
mistake was, and it is published text that no one sees rendered.
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
