"""Download the site's three faces from Google Fonts into vendor/fonts-<date>/.

python3 src/vendor_fonts.py [out_dir]

Every page used to link fonts.googleapis.com, which fetched a stylesheet from Google and
the font files from fonts.gstatic.com. A slow or blocked Google held up first paint on
every page, each visit told Google who came, and each of 30 page sources asked for its own
list of weights, so the shared header's 700 weight drew as 600 on 25 of them (INC-0163).
Pages now link one stylesheet on this site, partials.FONTS_CSS, and this is how it and its
files were made.

It asks Google for the union of every face any page uses, with a current Chrome user agent
so the answer is WOFF2 split by unicode-range as browsers receive it, downloads each file
once, and rewrites the stylesheet to point at the local copies. The files are Google's, byte
for byte; nothing is subset or renamed. Each family's SIL Open Font License is saved beside
them, and README.md records the request, the date and a sha256 for every file.

/vendor/ is versioned by directory, and the trainers' service workers treat anything under
it as immutable (INC-0148). So a refresh goes to a new directory: run this, point
partials.FONTS_CSS at the new one, and delete the old one once nothing links it.
"""
import datetime
import hashlib
import os
import pathlib
import re
import ssl
import sys
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parent.parent

# Every face a page uses, and no other. Source Serif 4 sets headings (600 and 700) and the
# blog's italic quotes (400 italic); IBM Plex Sans sets everything else, 700 included
# because the shared header asks for it; IBM Plex Mono sets figures in columns.
FAMILIES = ("family=Source+Serif+4:ital,opsz,wght@0,8..60,600;0,8..60,700;1,8..60,400"
            "&family=IBM+Plex+Sans:wght@400;500;600;700"
            "&family=IBM+Plex+Mono:wght@400;500&display=swap")
CSS_URL = "https://fonts.googleapis.com/css2?" + FAMILIES
# Google answers with the formats the user agent can read; this one gets WOFF2 by subset.
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
      "Chrome/124.0 Safari/537.36")
LICENSES = {
    "Source Serif 4": "https://raw.githubusercontent.com/google/fonts/main/ofl/sourceserif4/OFL.txt",
    "IBM Plex Sans": "https://raw.githubusercontent.com/google/fonts/main/ofl/ibmplexsans/OFL.txt",
    "IBM Plex Mono": "https://raw.githubusercontent.com/google/fonts/main/ofl/ibmplexmono/OFL.txt",
}
FACE = re.compile(r"/\*\s*([\w-]+)\s*\*/\s*@font-face\s*\{([^}]*)\}")


def ssl_context():
    for var in ("SSL_CERT_FILE", "REQUESTS_CA_BUNDLE"):
        if os.environ.get(var) and os.path.exists(os.environ[var]):
            return ssl.create_default_context(cafile=os.environ[var])
    if os.path.exists("/root/.ccr/ca-bundle.crt"):
        return ssl.create_default_context(cafile="/root/.ccr/ca-bundle.crt")
    return ssl.create_default_context()


def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=60, context=ssl_context()) as r:
        return r.read()


def slug(family):
    return re.sub(r"[^a-z0-9]+", "-", family.lower()).strip("-")


def faces(css):
    """[{subset, family, style, weight, url, range}] in the order Google lists them."""
    out = []
    for subset, body in FACE.findall(css):
        prop = dict((k.strip(), v.strip()) for k, v in
                    (line.split(":", 1) for line in body.split(";") if ":" in line))
        url = re.search(r"url\(([^)]+)\)", prop["src"]).group(1)
        out.append({"subset": subset, "family": prop["font-family"].strip("'\""),
                    "style": prop["font-style"], "weight": prop["font-weight"],
                    "url": url, "range": prop.get("unicode-range", "")})
    return out


def names(fs):
    """A local file name for each Google URL. A file Google serves for one weight is named
    for it; a variable file serving several is named without one."""
    weights = {}
    for f in fs:
        weights.setdefault(f["url"], set()).add(f["weight"])
    out = {}
    for f in fs:
        if f["url"] in out:
            continue
        parts = [slug(f["family"])]
        if f["style"] != "normal":
            parts.append(f["style"])
        if len(weights[f["url"]]) == 1:
            parts.append(f["weight"])
        parts.append(f["subset"])
        out[f["url"]] = "-".join(parts) + ".woff2"
    if len(set(out.values())) != len(out):
        raise SystemExit("vendor_fonts: two Google files would share a local name")
    return out


def main(argv):
    today = datetime.date.today().isoformat()
    out = pathlib.Path(argv[1]) if len(argv) > 1 else ROOT / "vendor" / ("fonts-" + today)
    css = get(CSS_URL).decode("utf-8")
    fs = faces(css)
    if not fs or len(fs) != css.count("@font-face"):
        raise SystemExit("vendor_fonts: could not read every @font-face in Google's answer")
    local = names(fs)
    out.mkdir(parents=True, exist_ok=True)
    sums = []
    for url, name in local.items():
        body = get(url)
        if body[:4] != b"wOF2":
            raise SystemExit("vendor_fonts: %s is not a WOFF2 file" % url)
        (out / name).write_bytes(body)
        sums.append((name, len(body), hashlib.sha256(body).hexdigest(), url))
    sheet = ["/* The site's three faces, served from this site. Written by src/vendor_fonts.py",
             "   from Google Fonts on %s; the files are Google's, unchanged. SIL Open Font" % today,
             "   License 1.1: see the OFL files beside this one. */"]
    for f in fs:
        sheet += ["/* %s */" % f["subset"], "@font-face {",
                  "  font-family: '%s';" % f["family"], "  font-style: %s;" % f["style"],
                  "  font-weight: %s;" % f["weight"], "  font-display: swap;",
                  "  src: url(%s) format('woff2');" % local[f["url"]]]
        if f["range"]:
            sheet.append("  unicode-range: %s;" % f["range"])
        sheet.append("}")
    (out / "fonts.css").write_text("\n".join(sheet) + "\n", encoding="utf-8")
    for family, url in LICENSES.items():
        (out / ("OFL-%s.txt" % slug(family))).write_bytes(get(url))
    readme = ["# Fonts", "",
              "Written by `src/vendor_fonts.py` on %s from this Google Fonts request:" % today, "",
              "    " + CSS_URL, "",
              "%d faces in %d files, each byte for byte what Google serves. Source Serif 4 and "
              "IBM Plex are licensed under the SIL Open Font License 1.1; each family's license "
              "is in its `OFL-*.txt` file here." % (len(fs), len(local)), "",
              "| File | Bytes | sha256 | Google URL |", "|---|---|---|---|"]
    readme += ["| %s | %d | `%s` | %s |" % s for s in sorted(sums)]
    (out / "README.md").write_text("\n".join(readme) + "\n", encoding="utf-8")
    print("vendor_fonts: %d faces in %d files, %d bytes, written to %s"
          % (len(fs), len(local), sum(s[1] for s in sums), out.relative_to(ROOT) if out.is_relative_to(ROOT) else out))


if __name__ == "__main__":
    main(sys.argv)
