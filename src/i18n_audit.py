"""Measure the translation surface of the built site.

Answering "how hard would it be to ship this in another language" with a number
instead of an opinion. Run after a build; it reads the generated pages, not the
templates, so it counts what a reader actually sees.

Three buckets, in increasing order of difficulty:

  markup    text in HTML text nodes. Browser translation and Google Translate
            already reach this, and a build-time catalog can replace it.
  script    UI copy inside inline <script> string literals: button labels,
            status messages, generated headings. Machine translation cannot
            reach any of it, so every string needs a catalog lookup before the
            page can ship in another language. This is the real cost.

  data      strings inside the large generated data payloads the build injects
            (the question banks, the school table). User-visible, but content
            rather than chrome, and priced separately because translating a
            question bank is an editorial project, not an engineering one.
  attr      user-visible attribute values (title, placeholder, aria-label,
            alt, and the meta description). Easy to miss, easy to translate.

Usage:  python3 src/i18n_audit.py [--json]
"""
import json, pathlib, re, sys, html as _html

ROOT = pathlib.Path(__file__).parent.parent
# Generated trees, in the order a reader is likely to meet them.
TARGETS = [
    ("landing", ["index.html"]),
    ("rankings", ["schools/index.html"]),
    ("school page", ["schools/stanford-gsb/index.html"]),
    ("international", ["international/index.html"]),
    ("checklist", ["apply/index.html"]),
    ("exams index", ["exams/index.html"]),
    ("exam page", ["exams/gmat/index.html"]),
    ("pricing", ["pricing/index.html"]),
    ("community", ["community/index.html"]),
    ("blog index", ["blog/index.html"]),
    ("trainer (GMAT)", ["app/index.html"]),
    ("trainer (SAT)", ["sat/app/index.html"]),
]
VISIBLE_ATTRS = ("title", "placeholder", "aria-label", "alt")
SKIP_TAGS = ("script", "style", "template")
# A string worth translating has at least two words and a lowercase letter, which
# drops class names, hex colors, ids, urls and single-token labels like "OK".
WORDY = re.compile(r"[A-Za-z][a-z]{2,}(\s+\S+)+")


def strip_blocks(text):
    """Remove script/style bodies, returning (markup_only, list_of_script_bodies)."""
    scripts = re.findall(r"<script\b[^>]*>([\s\S]*?)</script>", text, re.I)
    for tag in SKIP_TAGS:
        text = re.sub(rf"<{tag}\b[^>]*>[\s\S]*?</{tag}>", " ", text, flags=re.I)
    return text, scripts


def markup_strings(markup):
    out = []
    for raw in re.split(r"<[^>]+>", markup):
        s = _html.unescape(raw).strip()
        if len(s) > 2 and WORDY.search(s):
            out.append(s)
    return out


def attr_strings(text):
    out = []
    for attr in VISIBLE_ATTRS:
        for m in re.finditer(rf'\b{attr}="([^"]{{3,}})"', text, re.I):
            s = _html.unescape(m.group(1)).strip()
            if WORDY.search(s):
                out.append(s)
    m = re.search(r'<meta name="description" content="([^"]+)"', text, re.I)
    if m:
        out.append(m.group(1))
    return out


# The build injects question banks and the school table as ALL_CAPS assignments.
# Those are content, not chrome, so they are counted separately.
DATA_ASSIGN = re.compile(r"(?:var\s+)?\b([A-Z][A-Z0-9_]{2,})\s*=\s*[\[{]")


def split_data_regions(body):
    """Return (ui_text, data_text): the big generated payloads, and everything else."""
    spans = []
    for m in DATA_ASSIGN.finditer(body):
        i = m.end() - 1
        open_ch, close_ch = body[i], {"[": "]", "{": "}"}[body[i]]
        depth, j, instr, esc, quote = 0, i, False, False, ""
        while j < len(body):
            c = body[j]
            if instr:
                if esc:
                    esc = False
                elif c == "\\":
                    esc = True
                elif c == quote:
                    instr = False
            elif c in "\"'":
                instr, quote = True, c
            elif c == open_ch:
                depth += 1
            elif c == close_ch:
                depth -= 1
                if depth == 0:
                    break
            j += 1
        # Only treat it as a data payload if it is genuinely large.
        if j - i > 2000:
            spans.append((i, j + 1))
    if not spans:
        return body, ""
    spans.sort()
    ui, data, prev = [], [], 0
    for a, b in spans:
        ui.append(body[prev:a])
        data.append(body[a:b])
        prev = b
    ui.append(body[prev:])
    return "".join(ui), "".join(data)


def _literals(src):
    out = []
    for m in re.finditer(r"'((?:[^'\\\n]|\\.){4,})'|\"((?:[^\"\\\n]|\\.){4,})\"", src):
        s = (m.group(1) or m.group(2)).strip()
        if not WORDY.search(s):
            continue
        if s.startswith(("http", "/", "./", "#", "data:")) or "</" in s:
            continue
        out.append(s)
    return out


def script_strings(bodies):
    ui, data = [], []
    for body in bodies:
        u, d = split_data_regions(body)
        ui += _literals(u)
        data += _literals(d)
    return ui, data


def audit_file(path):
    text = path.read_text()
    markup, scripts = strip_blocks(text)
    ui, data = script_strings(scripts)
    return {
        "markup": markup_strings(markup),
        "attr": attr_strings(text),
        "script": ui,
        "data": data,
    }


def main():
    as_json = "--json" in sys.argv
    report, totals = [], {"markup": 0, "attr": 0, "script": 0, "data": 0, "words": 0}
    missing = []
    for label, rels in TARGETS:
        for rel in rels:
            p = ROOT / rel
            if not p.exists():
                missing.append(rel)
                continue
            r = audit_file(p)
            uniq = {k: sorted(set(v)) for k, v in r.items()}
            words = sum(len(s.split()) for k, v in uniq.items() if k != "data" for s in v)
            row = {"page": label, "path": rel, "words": words,
                   **{k: len(v) for k, v in uniq.items()},
                   "sample_script": uniq["script"][:3]}
            report.append(row)
            for k in ("markup", "attr", "script", "data"):
                totals[k] += len(uniq[k])
            totals["words"] += words

    if as_json:
        print(json.dumps({"pages": report, "totals": totals, "missing": missing}, indent=1))
        return
    if missing:
        print("not built, skipped: " + ", ".join(missing) + "\n")
    w = max(len(r["page"]) for r in report)
    hdr = f"{'page'.ljust(w)}  {'markup':>7} {'attr':>5} {'script':>7} {'data':>7} {'ui words':>9}"
    print(hdr); print("-" * len(hdr))
    for r in report:
        print(f"{r['page'].ljust(w)}  {r['markup']:>7} {r['attr']:>5} {r['script']:>7} {r['data']:>7} {r['words']:>9}")
    print("-" * len(hdr))
    print(f"{'total'.ljust(w)}  {totals['markup']:>7} {totals['attr']:>5} {totals['script']:>7} {totals['data']:>7} {totals['words']:>9}")
    print()
    print(f"markup + attr = {totals['markup'] + totals['attr']} strings, roughly {totals['words']} words of UI copy.")
    print("Browser and search-engine translation already reach these.")
    print(f"script = {totals['script']} strings of UI copy that machine translation cannot reach;")
    print("each needs a catalog lookup before a page can ship in another language.")
    print(f"data = {totals['data']} strings in the generated banks and school table, which is an")
    print("editorial translation project priced separately. See I18N.md.")


if __name__ == "__main__":
    main()
