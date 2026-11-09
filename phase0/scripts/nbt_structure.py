"""Minimal NBT writer and block-list -> vanilla structure (.nbt) converter.

No third-party dependencies. A block list is a list of
    {"pos": [x, y, z], "id": "minecraft:piston", "props": {"facing": "east"}, "nbt": {...}}
where "props" and "nbt" are optional. Positions are relative to the structure origin
and must be non-negative.

Palette entries use the Java 26.x keys ("id", "properties"). Older versions used
"Name"/"Properties"; a 26.3 server silently places those as air.
"""
import gzip
import struct

TAG_END, TAG_BYTE, TAG_SHORT, TAG_INT, TAG_LONG = 0, 1, 2, 3, 4
TAG_STRING, TAG_LIST, TAG_COMPOUND = 8, 9, 10


class Byte(int):
    """Marks an int that must be written as TAG_Byte (e.g. booleans in block entity data)."""


def _tag_of(v):
    if isinstance(v, Byte):
        return TAG_BYTE
    if isinstance(v, bool):
        return TAG_BYTE
    if isinstance(v, int):
        return TAG_INT
    if isinstance(v, str):
        return TAG_STRING
    if isinstance(v, list):
        return TAG_LIST
    if isinstance(v, dict):
        return TAG_COMPOUND
    raise TypeError(f"unsupported NBT value: {v!r}")


def _str(s):
    b = s.encode("utf-8")
    return struct.pack(">H", len(b)) + b


def _payload(v):
    t = _tag_of(v)
    if t == TAG_BYTE:
        return struct.pack(">b", int(v))
    if t == TAG_INT:
        return struct.pack(">i", v)
    if t == TAG_STRING:
        return _str(v)
    if t == TAG_LIST:
        if not v:
            return struct.pack(">bi", TAG_END, 0)
        et = _tag_of(v[0])
        if any(_tag_of(e) != et for e in v):
            raise TypeError("NBT lists must be homogeneous")
        return struct.pack(">bi", et, len(v)) + b"".join(_payload(e) for e in v)
    if t == TAG_COMPOUND:
        out = b""
        for k, e in v.items():
            out += struct.pack(">b", _tag_of(e)) + _str(k) + _payload(e)
        return out + struct.pack(">b", TAG_END)
    raise AssertionError


def dumps(root):
    """Serialize a dict as a gzip-compressed NBT file with an unnamed root compound."""
    raw = struct.pack(">b", TAG_COMPOUND) + _str("") + _payload(root)
    return gzip.compress(raw, mtime=0)


def structure_from_blocks(blocks, data_version, size=None):
    """Build the structure-file NBT dict for a block list."""
    palette, index, out = [], {}, []
    mx = [0, 0, 0]
    for b in blocks:
        x, y, z = b["pos"]
        if min(x, y, z) < 0:
            raise ValueError(f"negative position {b['pos']}")
        mx = [max(mx[0], x + 1), max(mx[1], y + 1), max(mx[2], z + 1)]
        props = {k: str(v) for k, v in sorted((b.get("props") or {}).items())}
        key = (b["id"], tuple(props.items()))
        if key not in index:
            index[key] = len(palette)
            entry = {"id": b["id"]}
            if props:
                entry["properties"] = props
            palette.append(entry)
        rec = {"pos": [x, y, z], "state": index[key]}
        if b.get("nbt"):
            rec["nbt"] = b["nbt"]
        out.append(rec)
    return {
        "DataVersion": data_version,
        "size": list(size or mx),
        "palette": palette,
        "blocks": out,
        "entities": [],
    }


def write_structure(path, blocks, data_version, size=None):
    with open(path, "wb") as f:
        f.write(dumps(structure_from_blocks(blocks, data_version, size)))
