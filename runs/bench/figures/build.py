"""Builds index.html (the published figures page) from figures.src.html and data.json, and a local preview copy."""
import sys
from pathlib import Path
here = Path(__file__).resolve().parent
page = (here / "figures.src.html").read_text().replace("__DATA__", (here / "data.json").read_text())
(here / "index.html").write_text(page)
if len(sys.argv) > 1:
    Path(sys.argv[1]).write_text('<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover"><style>body{margin:0}</style></head><body>' + page + '</body></html>')
print("built")
