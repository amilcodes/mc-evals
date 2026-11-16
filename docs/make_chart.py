"""Builds docs/media/volumes.svg: every finished run's final door volume, by task and model.

    python3 docs/make_chart.py
"""
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
runs = json.loads((ROOT / "runs/bench/dashboard/runs.json").read_text())

ROWS = [
    ("2×2 seamless", "2×2"),
    ("3×2 seamless", "3×2"),
    ("3×3 seamless", "3×3"),
    ("3×3 seamless (changed physics)", "3×3, changed physics"),
    ("4×4 seamless", "4×4"),
    ("4×4 seamless (kit 2)", "4×4, kit 2"),
]
MODELS = [("Opus 5.5", "#0072B2"), ("Fable 5.2", "#D55E00"), ("Sonnet 5.5", "#009E73"), ("Haiku 5.5", "#CC79A7")]
COLOR = dict(MODELS)

W, LEFT, RIGHT, TOP, ROW = 880, 190, 40, 70, 46
H = TOP + ROW * len(ROWS) + 70
lo, hi = math.log10(20), math.log10(6000)
x = lambda v: LEFT + (math.log10(v) - lo) / (hi - lo) * (W - LEFT - RIGHT)

s = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" font-family="-apple-system,Segoe UI,Helvetica,Arial,sans-serif">',
     f'<rect width="{W}" height="{H}" rx="12" fill="#ffffff"/>',
     f'<text x="24" y="34" font-size="17" font-weight="600" fill="#1f2328">Final door volume per run (lower is better)</text>',
     f'<text x="24" y="54" font-size="12.5" fill="#59636e">Each dot is one agent run that ended with a valid door. Log scale. Ringed dot = best for that model and task.</text>']
# grid
for v in (20, 50, 100, 200, 500, 1000, 2000, 5000):
    gx = x(v)
    s.append(f'<line x1="{gx:.1f}" y1="{TOP - 6}" x2="{gx:.1f}" y2="{TOP + ROW * len(ROWS)}" stroke="#eaeef2" stroke-width="1"/>')
    s.append(f'<text x="{gx:.1f}" y="{TOP + ROW * len(ROWS) + 18}" font-size="11.5" fill="#59636e" text-anchor="middle">{v:,}</text>')
s.append(f'<text x="{(LEFT + W - RIGHT) / 2:.0f}" y="{TOP + ROW * len(ROWS) + 36}" font-size="11.5" fill="#59636e" text-anchor="middle">volume (blocks in the swept bounding box)</text>')

for i, (task, label) in enumerate(ROWS):
    cy = TOP + ROW * i + ROW / 2
    s.append(f'<text x="{LEFT - 14}" y="{cy + 4:.1f}" font-size="13" fill="#1f2328" text-anchor="end">{label}</text>')
    if i:
        s.append(f'<line x1="24" y1="{TOP + ROW * i}" x2="{W - 24}" y2="{TOP + ROW * i}" stroke="#f0f2f4"/>')
    rr = [r for r in runs if r["task"] == task and r["status"] == "door" and r.get("volume")]
    if rr:
        best = min(r["volume"] for r in rr)
        s.append(f'<text x="{x(best) - 12:.1f}" y="{cy + 4:.1f}" font-size="12" font-weight="600" fill="#1f2328" text-anchor="end">{best}</text>')
    for j, (m, _) in enumerate(MODELS):
        mine = sorted(r["volume"] for r in rr if r["model"] == m)
        off = (j - 1.5) * 7
        for k, v in enumerate(mine):
            best = k == 0
            s.append(f'<circle cx="{x(v):.1f}" cy="{cy + off:.1f}" r="{5.5 if best else 4}" fill="{COLOR[m]}" fill-opacity="{1 if best else 0.55}"'
                     + (' stroke="#1f2328" stroke-width="1.4"' if best else '') + f'><title>{m}, {label}: {v:,}</title></circle>')

# legend
lx = 24
ly = H - 16
for m, c in MODELS:
    s.append(f'<circle cx="{lx + 6}" cy="{ly - 4}" r="5" fill="{c}"/><text x="{lx + 16}" y="{ly}" font-size="12.5" fill="#1f2328">{m}</text>')
    lx += 112
s.append("</svg>")
(ROOT / "docs/media/volumes.svg").write_text("\n".join(x for x in s if x))
print("wrote docs/media/volumes.svg")
