"""Junta src/ num único arquivo: python3 build.py  ->  dist/checagem.html"""
import re, pathlib
src = pathlib.Path(__file__).parent / "src"
html = (src / "index.html").read_text(encoding="utf-8")
html = re.sub(r"<!-- @css (\S+) -->", lambda m: "<style>\n" + (src/"css"/m.group(1)).read_text(encoding="utf-8") + "</style>", html)
html = re.sub(r"<!-- @js (\S+) -->", lambda m: "<script>\n" + (src/"js"/m.group(1)).read_text(encoding="utf-8") + "</script>", html)
out = src.parent / "dist" / "checagem.html"
out.write_text(html, encoding="utf-8")
print("gerado:", out)
