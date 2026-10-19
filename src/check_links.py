"""Every internal link in the built site has to resolve to something the deploy serves.

    python3 src/check_links.py        after python3 src/build.py && python3 src/build_blog.py

The GRE, SAT, LSAT and ACT calculators each linked /guide/<exam>/, a page that has never
existed, and every click on those buttons landed on the 404 page (INC-0213). The links were
typed by hand from the pattern of the exam pages, and nothing resolved a hand typed link
against the built site: smoke_launch.js follows links only from the pages it opens.

So this reads every built page, takes every href and src outside inline scripts, and
resolves each internal one the way the live site would:

  - a path ending in / needs its index.html;
  - /page needs page, page.html or page/index.html (Cloudflare's html_handling);
  - a path the Worker redirects (RETIRED in src/worker.mjs) counts as resolved;
  - anything .assetsignore keeps out of the deploy does NOT count, however present it is in
    this checkout, because the live site answers it with a 404;
  - a #fragment on another page needs an element with that id on the target page.

It needs a full build first, and fails with the list of broken targets and a page that
links each one.
"""
import html
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
SITE = "https://startfromnowhere.com"

# What .assetsignore keeps out of the deploy, as path prefixes. design/ is excluded except
# for the three things the pages load from it.
NOT_SERVED = ("src/", "data/", "supabase/", "playbook/", "docs/", ".github/", ".claude/",
              ".git/", "node_modules/")
DESIGN_SERVED = ("design/assets/", "design/tokens/", "design/styles.css")
NOT_SERVED_FILES = {"CLAUDE.md", "README.md", "ROADMAP.md", "HANDOFF.md", "DEVSECOPS.md",
                    "GROWTH.md", "INTEGRATIONS.md", "I18N.md", "DATA_COLLECTION.md",
                    "CONNECTORS.md", "wrangler.jsonc", ".gitignore", ".assetsignore"}

# Pages whose script reads location.hash as a route rather than as an anchor: the trainers
# open #cards or #account as views, and the forum routes #/c/<category>. A fragment on one of
# these is not an element id, so it is not checked as one. /colleges/ also picks a tab from
# its hash, but each tab carries the category as its id, so its links are checked.
HASH_ROUTED = {"/app/", "/sat/app/", "/gre/app/", "/lsat/app/", "/act/app/", "/community/"}

ATTR = re.compile(r"""\b(?:href|src)\s*=\s*["']([^"']+)["']""")
SCRIPT = re.compile(r"<script\b[^>]*>.*?</script>", re.S | re.I)
IDS = re.compile(r"""\bid\s*=\s*["']([^"']+)["']""")


def served(rel):
    if rel in NOT_SERVED_FILES:
        return False
    if rel.startswith(NOT_SERVED):
        return False
    if rel.startswith("design/") and not rel.startswith(DESIGN_SERVED):
        return False
    return True


def retired():
    text = (ROOT / "src" / "worker.mjs").read_text(encoding="utf-8")
    block = re.search(r"const RETIRED = \{(.*?)\};", text, re.S)
    return set(re.findall(r'"(/[^"]*)"\s*:', block.group(1))) if block else set()


def resolve(path):
    """The built file a site path serves, or None."""
    rel = path.lstrip("/")
    candidates = ([rel + "index.html"] if path.endswith("/") or not rel
                  else [rel, rel + ".html", rel + "/index.html"])
    for c in candidates:
        f = ROOT / c
        if f.is_file() and served(c):
            return f
    return None


def pages():
    for f in ROOT.rglob("*.html"):
        rel = f.relative_to(ROOT).as_posix()
        if served(rel):
            yield f


def main():
    redirects = retired()
    id_cache = {}
    broken = {}
    count = 0
    for page in pages():
        rel_dir = "/" + page.relative_to(ROOT).parent.as_posix()
        text = SCRIPT.sub(" ", page.read_text(encoding="utf-8", errors="ignore"))
        for raw in ATTR.findall(text):
            url = html.unescape(raw).strip()
            if url.startswith(SITE):
                url = url[len(SITE):] or "/"
            if not url or url.startswith(("#", "mailto:", "tel:", "data:", "javascript:", "//",
                                          "http://", "https://", "{{")):
                continue
            path, _, frag = url.partition("#")
            path = path.split("?")[0]
            if not path.startswith("/"):
                path = str(pathlib.PurePosixPath(rel_dir) / path)
                path = re.sub(r"/\./", "/", path)
                if url.split("#")[0].split("?")[0].endswith("/") and not path.endswith("/"):
                    path += "/"
            count += 1
            if path in redirects:
                continue
            target = resolve(path)
            if target is None:
                broken.setdefault(path, page.relative_to(ROOT).as_posix())
                continue
            if frag and target.suffix == ".html" and path not in HASH_ROUTED and not frag.startswith("/"):
                if target not in id_cache:
                    id_cache[target] = set(IDS.findall(target.read_text(encoding="utf-8",
                                                                         errors="ignore")))
                if frag not in id_cache[target]:
                    broken.setdefault(path + "#" + frag, page.relative_to(ROOT).as_posix())
    if broken:
        print("check_links: %d internal link target(s) do not resolve on the deploy:" % len(broken))
        for target, src in sorted(broken.items()):
            print("  %s   (linked from %s)" % (target, src))
        return 1
    print("check_links: all %d internal links resolve" % count)
    return 0


if __name__ == "__main__":
    sys.exit(main())
