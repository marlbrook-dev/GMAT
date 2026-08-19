import pathlib, subprocess, sys, tempfile, os
d = pathlib.Path(__file__).parent; root = d.parent
BANK_FILES = ["bank_quant.js","bank_quant2.js","bank_quant3.js","bank_verbal.js","bank_verbal2.js","bank_verbal3.js","bank_di.js","bank_di2.js","bank_di3.js","cards.js"]
banks = "\n".join((d/f).read_text() for f in BANK_FILES)
engine = (d/"engine.js").read_text(); tpl = (d/"app_template.html").read_text()
out = tpl.replace("{{BANKS}}", banks).replace("{{ENGINE}}", engine)
(root/"app").mkdir(exist_ok=True); (root/"app"/"index.html").write_text(out); (root/"404.html").write_text(out)
(root/"index.html").write_text((d/"landing.html").read_text())

def check_scripts(path):
    # a single unescaped quote in generated JS once took down the whole app;
    # parse every inline script with node before letting a build succeed
    import re
    html = pathlib.Path(path).read_text()
    for i, m in enumerate(re.finditer(r"<script>([\s\S]*?)</script>", html)):
        with tempfile.NamedTemporaryFile("w", suffix=".js", delete=False) as f:
            f.write(m.group(1))
            tmp = f.name
        r = subprocess.run(["node", "--check", tmp], capture_output=True, text=True)
        os.unlink(tmp)
        if r.returncode != 0:
            print(f"SYNTAX ERROR in inline script {i} of {path}:\n{r.stderr.strip()}", file=sys.stderr)
            sys.exit(1)

for p in [root/"app"/"index.html", root/"index.html"]:
    check_scripts(p)
print("built app/index.html", len(out), "bytes; landing copied to index.html; inline scripts parse")
