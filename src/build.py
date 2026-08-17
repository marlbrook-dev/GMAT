import pathlib
d = pathlib.Path(__file__).parent; root = d.parent
banks = "\n".join((d/f).read_text() for f in ["bank_quant.js","bank_quant2.js","bank_verbal.js","bank_verbal2.js","bank_di.js","bank_di2.js","cards.js"])
engine = (d/"engine.js").read_text(); tpl = (d/"app_template.html").read_text()
out = tpl.replace("{{BANKS}}", banks).replace("{{ENGINE}}", engine)
(root/"app").mkdir(exist_ok=True); (root/"app"/"index.html").write_text(out); (root/"404.html").write_text(out)
(root/"index.html").write_text((d/"landing.html").read_text())
print("built app/index.html", len(out), "bytes; landing copied to index.html")
