"""Renders a recorded door run (a kit-2 film plus hallway walls) as isometric video frames.

    python render.py opus_5236_film.json frames/ --scale 11 --speed 0.5

Every tick of every flip becomes one frame (more at --speed below 1), with short holds at rest.
Blocks are drawn as cubes in painter's order, seen from the front-left above the doorway.
"""
import argparse
import json
import math
import re
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

BG = (17, 19, 24)
PANEL = (28, 31, 38)
TEXT = (232, 230, 225)
MUTED = (150, 152, 160)
DOORWAY = (255, 196, 60)

BASE = {
    "stone": (138, 138, 138), "smooth_stone": (160, 160, 160), "iron_block": (210, 210, 214),
    "obsidian": (34, 24, 52), "glass": (190, 225, 240), "slime_block": (118, 190, 90), "honey_block": (232, 160, 58),
    "observer": (92, 92, 96), "piston": (150, 150, 150), "sticky_piston": (150, 150, 150), "piston_head": (180, 138, 82),
    "moving_piston": (255, 214, 120), "redstone_block": (190, 30, 20), "target": (230, 210, 200), "note_block": (110, 74, 50),
    "repeater": (165, 165, 165), "comparator": (165, 165, 165), "lever": (120, 92, 60),
    "redstone_torch": (220, 40, 20), "redstone_wall_torch": (220, 40, 20),
}
FLAT = {"redstone_wire": 0.06, "repeater": 0.14, "comparator": 0.14}   # height of thin blocks
SMALL = {"lever", "redstone_torch", "redstone_wall_torch"}


def parse(state):
    m = re.match(r"([a-z_]+)(?:\[(.*)\])?", state)
    props = dict(kv.split("=") for kv in m.group(2).split(",")) if m.group(2) else {}
    return m.group(1), props


def shade(c, f):
    return tuple(max(0, min(255, int(v * f))) for v in c)


def colours(state):
    """(top, left, front) colours for one block state; None for air."""
    name, p = parse(state)
    if name == "air":
        return None
    if name == "redstone_wire":
        pw = int(p.get("power", 0))
        c = (70 + int(185 * pw / 15), 8 + int(30 * pw / 15), 6)
        return c, c, c
    c = BASE.get(name, (200, 0, 200))
    top = c
    if name in ("piston", "sticky_piston"):
        facing = p.get("facing")
        face = (120, 170, 80) if name == "sticky_piston" else (180, 138, 82)
        top = face if facing == "up" else c
        if p.get("extended") == "true":
            top = shade(top, 0.85)
    if name == "observer" and p.get("powered") == "true":
        top = (220, 60, 40)
    if name in ("repeater", "comparator"):
        top = (205, 70, 50) if p.get("powered") == "true" else (175, 170, 165)
    if name == "lever":
        top = (220, 60, 40) if p.get("powered") == "true" else (150, 120, 80)
    return top, shade(c, 0.78), shade(c, 0.62)


class Camera:
    """Isometric view from the front-left, above: shows the top, -x and -z faces of each cube."""

    def __init__(self, scale, ox, oy):
        self.s, self.ox, self.oy = scale, ox, oy
        self.cx, self.cy = math.cos(math.radians(30)), math.sin(math.radians(30))

    def p(self, x, y, z):
        u, w = -x, -z
        return (self.ox + (u - w) * self.cx * self.s, self.oy + (-y + (u + w) * self.cy) * self.s)


def cube(draw, cam, pos, cols, h=1.0, inset=0.0, outline=None):
    x, y, z = pos
    a, b = x + inset, x + 1 - inset
    c, d = z + inset, z + 1 - inset
    y0, y1 = y, y + h
    top, left, front = cols
    P = cam.p
    draw.polygon([P(a, y1, c), P(b, y1, c), P(b, y1, d), P(a, y1, d)], fill=top, outline=outline)                 # +y
    draw.polygon([P(a, y0, c), P(a, y1, c), P(a, y1, d), P(a, y0, d)], fill=left, outline=outline)                # -x
    draw.polygon([P(a, y0, c), P(b, y0, c), P(b, y1, c), P(a, y1, c)], fill=front, outline=outline)               # -z


def draw_world(img, cam, world, walls, glass_layer):
    draw = ImageDraw.Draw(img)
    gdraw = ImageDraw.Draw(glass_layer)
    cells = [(p, s) for p, s in world.items()]
    cells += [(tuple(w), "wall") for w in walls]
    cells.sort(key=lambda it: (-it[0][0] + it[0][1] - it[0][2]))
    for pos, state in cells:
        if state == "wall":
            cube(gdraw, cam, pos, ((70, 76, 92, 40), (70, 76, 92, 34), (70, 76, 92, 28)), outline=(110, 118, 140, 55))
            continue
        name, _ = parse(state)
        cols = colours(state)
        if cols is None:
            continue
        if name == "glass":
            cube(gdraw, cam, pos, ((190, 225, 240, 34), (190, 225, 240, 26), (190, 225, 240, 22)), outline=(200, 230, 245, 90))
            continue
        if name in FLAT:
            cube(draw, cam, pos, cols, h=FLAT[name], inset=0.06 if name == "redstone_wire" else 0.0)
        elif name in SMALL:
            cube(draw, cam, pos, cols, h=0.5, inset=0.35)
        elif name == "piston_head":
            cube(draw, cam, pos, cols, h=1.0, inset=0.18)
        else:
            cube(draw, cam, pos, cols, outline=shade(cols[2], 0.75))
    return img


def doorway_outline(draw, cam, n=4):
    P = cam.p
    pts = [P(0, 0, 0), P(n, 0, 0), P(n, n, 0), P(0, n, 0)]
    draw.line(pts + [pts[0]], fill=DOORWAY, width=2)


def door_inset(draw, font, rows, x0, y0, cell=16):
    draw.text((x0, y0 - 22), "doorway", fill=MUTED, font=font)
    for r, row in enumerate(rows.split("/")):
        for c, ch in enumerate(row):
            fill = {"#": (170, 170, 170), ".": (40, 44, 52), "m": (255, 214, 120)}.get(ch, (220, 90, 60))
            draw.rectangle([x0 + c * (cell + 3), y0 + r * (cell + 3), x0 + c * (cell + 3) + cell, y0 + r * (cell + 3) + cell], fill=fill)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("film")
    ap.add_argument("out")
    ap.add_argument("--scale", type=float, default=60, help="largest pixels per block; the view is fitted to the frame below this")
    ap.add_argument("--speed", type=float, default=0.5, help="game ticks per frame relative to 20 fps real time (0.5 = half speed)")
    ap.add_argument("--title", default="")
    ap.add_argument("--subtitle", default="")
    a = ap.parse_args()
    film = json.loads(Path(a.film).read_text())
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    for f in out.glob("*.png"):
        f.unlink()

    W, H = 1280, 720
    world = {(b[0], b[1], b[2]): b[3] for b in film["start"]["blocks"]}
    lever = tuple(film["lever"])
    # fit the view to everything the run ever occupies
    lo, hi = film["swept_box"]["min"], film["swept_box"]["max"]
    corners = [(x, y, z) for x in (lo[0], hi[0] + 1) for y in (lo[1], hi[1] + 1) for z in (lo[2], hi[2] + 1)]
    probe = Camera(1, 0, 0)
    xs = [probe.p(*c)[0] for c in corners]
    ys = [probe.p(*c)[1] for c in corners]
    top_band, bottom_band = 112, 64
    scale = min((W - 80) / (max(xs) - min(xs)), (H - top_band - bottom_band - 20) / (max(ys) - min(ys)), a.scale)
    ox = (W - (max(xs) - min(xs)) * scale) / 2 - min(xs) * scale
    oy = top_band + 10 + (H - top_band - bottom_band - 20 - (max(ys) - min(ys)) * scale) / 2 - min(ys) * scale
    cam = Camera(scale, ox, oy)

    font_t = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 26)
    font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 18)
    font_s = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 15)
    frame = 0

    def render(label, tick, rows, lever_on):
        nonlocal frame
        img = Image.new("RGB", (W, H), BG)
        glass = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        draw_world(img, cam, world, film["walls"], glass)
        img = Image.alpha_composite(img.convert("RGBA"), glass).convert("RGB")
        d = ImageDraw.Draw(img)
        doorway_outline(d, cam)
        d.rectangle([0, 0, W, 104], fill=PANEL)
        d.text((28, 20), a.title, fill=TEXT, font=font_t)
        d.text((28, 60), a.subtitle, fill=MUTED, font=font)
        d.text((28, H - 46), label, fill=TEXT, font=font)
        if tick is not None:
            d.text((W - 300, H - 46), f"game tick {tick:>3}   ({a.speed:g}× speed)", fill=MUTED, font=font)
        d.text((W - 300, 20), "lever", fill=MUTED, font=font_s)
        d.ellipse([W - 252, 22, W - 238, 36], fill=(220, 60, 40) if lever_on else (90, 90, 96))
        d.text((W - 230, 20), "on" if lever_on else "off", fill=TEXT, font=font_s)
        door_inset(d, font_s, rows, W - 120, 40, cell=12)
        img.save(out / f"f{frame:05d}.png")
        frame += 1

    def hold(label, rows, lever_on, seconds=1.2):
        for _ in range(int(20 * seconds)):
            render(label, None, rows, lever_on)

    start_rows = film["start"]["doorway"]
    hold("At rest: door open, lever off", start_rows, False)
    lever_on = False
    for fl in film["flips"]:
        lever_on = fl["lever"] == "on"
        world[lever] = world.get(lever, "lever").replace("powered=false", "powered=true") if lever_on else world.get(lever, "lever").replace("powered=true", "powered=false")
        verb = "closing" if lever_on else "opening"
        reps = max(1, round(1 / a.speed))
        for tick in fl["ticks"]:
            for x, y, z, _, after in tick["changes"]:
                if after == "air":
                    world.pop((x, y, z), None)
                else:
                    world[(x, y, z)] = after
            for _ in range(reps):
                render(f"Flip {fl['flip']}: lever {fl['lever']}, door {verb}", tick["t"], tick["doorway"], lever_on)
        end = fl["ticks"][-1]["doorway"]
        hold(f"At rest: door {'closed' if lever_on else 'open'} after {fl['last_change_tick']} ticks", end, lever_on)
    print(f"{frame} frames in {out}")


if __name__ == "__main__":
    main()
