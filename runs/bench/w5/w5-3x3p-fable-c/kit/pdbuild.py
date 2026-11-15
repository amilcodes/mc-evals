"""Small helper for writing designs in Python. Optional; a design is just a JSON file.

    from pdbuild import Design
    d = Design("open")
    d.set(-2, 0, 0, "sticky_piston", facing="east")
    d.fill(0, -1, 0, 1, -1, 0, "stone")
    d.save("door.json")
"""
import json

_FLIP = {"east": "west", "west": "east"}


class Design:
    def __init__(self, initial_state="open"):
        self.initial_state = initial_state
        self.blocks = {}

    def set(self, x, y, z, block, **props):
        self.blocks[(x, y, z)] = (block, {k: str(v).lower() if isinstance(v, bool) else str(v) for k, v in props.items()})
        return self

    def remove(self, x, y, z):
        self.blocks.pop((x, y, z), None)
        return self

    def get(self, x, y, z):
        return self.blocks.get((x, y, z))

    def fill(self, x0, y0, z0, x1, y1, z1, block, **props):
        for x in range(min(x0, x1), max(x0, x1) + 1):
            for y in range(min(y0, y1), max(y0, y1) + 1):
                for z in range(min(z0, z1), max(z0, z1) + 1):
                    self.set(x, y, z, block, **props)
        return self

    def translate(self, dx, dy, dz):
        """Moves this design in place and returns it. Use copy() first to keep the original."""
        self.blocks = {(x + dx, y + dy, z + dz): b for (x, y, z), b in self.blocks.items()}
        return self

    def copy(self):
        """An independent copy: changing one does not change the other."""
        out = Design(self.initial_state)
        out.blocks = {pos: (block, dict(props)) for pos, (block, props) in self.blocks.items()}
        return out

    def mirrored_x(self, total):
        """A copy reflected left-right: x becomes total - x. East/west facings and wire sides swap."""
        out = Design(self.initial_state)
        for (x, y, z), (block, props) in self.blocks.items():
            p = dict(props)
            if "facing" in p:
                p["facing"] = _FLIP.get(p["facing"], p["facing"])
            if "east" in p or "west" in p:
                p["east"], p["west"] = p.get("west", "none"), p.get("east", "none")
            out.blocks[(total - x, y, z)] = (block, p)
        return out

    def merge(self, other):
        self.blocks.update(other.blocks)
        return self

    def bbox(self):
        ps = list(self.blocks)
        return [min(p[i] for p in ps) for i in range(3)], [max(p[i] for p in ps) for i in range(3)]

    def to_json(self):
        blocks = []
        for (x, y, z), (block, props) in sorted(self.blocks.items()):
            b = {"pos": [x, y, z], "id": block}
            if props:
                b["props"] = props
            blocks.append(b)
        return {"initial_state": self.initial_state, "blocks": blocks}

    def save(self, path):
        data = self.to_json()
        with open(path, "w") as f:  # one block per line
            f.write('{"initial_state": ' + json.dumps(data["initial_state"]) + ',\n "blocks": [\n  ')
            f.write(",\n  ".join(json.dumps(b) for b in data["blocks"]) + "\n ]}\n")
        return path

    @classmethod
    def load(cls, path):
        with open(path) as f:
            data = json.load(f)
        d = cls(data.get("initial_state", "open"))
        for b in data["blocks"]:
            d.set(*b["pos"], b["id"], **(b.get("props") or {}))
        return d
