"""Minimal NBT writer and block-list -> vanilla structure (.nbt) converter. No dependencies.

Palette entries use the Java 26.x keys ("id", "properties"). Older versions used
"Name"/"Properties"; a 26.3 server accepts those without error and places them as air.
"""
import gzip
import struct

TAG_END, TAG_BYTE, TAG_INT, TAG_STRING, TAG_LIST, TAG_COMPOUND = 0, 1, 3, 8, 9, 10


def _tag_of(v):
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
    out = b""
    for k, e in v.items():
        out += struct.pack(">b", _tag_of(e)) + _str(k) + _payload(e)
    return out + struct.pack(">b", TAG_END)


def dumps(root):
    """Serialize a dict as gzip-compressed NBT with an unnamed root compound."""
    return gzip.compress(struct.pack(">b", TAG_COMPOUND) + _str("") + _payload(root), mtime=0)


def structure_bytes(blocks, data_version, size):
    """blocks: [{"pos": [x, y, z], "id": str, "props": {..}, "nbt": {..}}] -> structure file bytes."""
    palette, index, out = [], {}, []
    for b in blocks:
        props = {k: str(v) for k, v in sorted((b.get("props") or {}).items())}
        key = (b["id"], tuple(props.items()))
        if key not in index:
            index[key] = len(palette)
            entry = {"id": b["id"]}
            if props:
                entry["properties"] = props
            palette.append(entry)
        rec = {"pos": list(b["pos"]), "state": index[key]}
        if b.get("nbt"):
            rec["nbt"] = b["nbt"]
        out.append(rec)
    return dumps({"DataVersion": data_version, "size": list(size), "palette": palette, "blocks": out, "entities": []})
