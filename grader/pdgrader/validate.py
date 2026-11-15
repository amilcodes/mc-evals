"""Static validation of a submission. Nothing is simulated here.

A submission is {"initial_state": "open" | "closed", "blocks": [{"pos": [x, y, z], "id": str,
"props": {...}}]}. validate() returns (errors, blocks) where blocks maps position -> (id, props).
Each error is {"code", "message", "pos"?}.
"""
from . import rules

MAX_ERRORS = 50


def _err(code, message, pos=None):
    e = {"code": code, "message": message}
    if pos is not None:
        e["pos"] = list(pos)
    return e


def _read_blocks(items, n, errors, blocks, door, walls):
    """Checks each listed block and fills `blocks`. `door`: the hallway is off limits.
    `walls`: the hallway-wall cells are off limits. Returns False if it gave up on too many errors."""
    for i, b in enumerate(items):
        if len(errors) >= MAX_ERRORS:
            errors.append(_err("too_many_errors", "further errors suppressed"))
            return False
        if not isinstance(b, dict):
            errors.append(_err("bad_block", f"blocks[{i}] is not an object"))
            continue
        pos = b.get("pos")
        if not (isinstance(pos, list) and len(pos) == 3 and all(type(c) is int for c in pos)):
            errors.append(_err("bad_pos", f"blocks[{i}].pos must be three integers"))
            continue
        pos = tuple(pos)
        block_id = b.get("id")
        if not isinstance(block_id, str):
            errors.append(_err("bad_block", f"blocks[{i}].id must be a string", pos))
            continue
        if ":" not in block_id:
            block_id = "minecraft:" + block_id
        props = b.get("props") or {}
        if not isinstance(props, dict):
            errors.append(_err("bad_property", "props must be an object", pos))
            continue
        props = {str(k): str(v).lower() if isinstance(v, bool) else str(v) for k, v in props.items()}

        if block_id == "minecraft:air":
            continue
        if not rules.in_region(n, pos):
            lo, hi = rules.region(n)
            errors.append(_err("out_of_region", f"position is outside the test volume {list(lo)}..{list(hi)}", pos))
            continue
        if pos in blocks:
            errors.append(_err("duplicate_pos", "two blocks share this position", pos))
            continue
        if block_id not in rules.ALLOWED:
            errors.append(_err("block_not_allowed", f"{block_id} is not on the allow-list", pos))
            continue
        allowed = rules.ALLOWED[block_id]
        bad = False
        for k, v in props.items():
            if k not in allowed:
                errors.append(_err("bad_property", f"{block_id} has no settable property {k!r}; allowed: {sorted(allowed)}", pos))
                bad = True
            elif v not in allowed[k]:
                errors.append(_err("bad_property_value", f"{block_id} {k}={v!r} is not allowed; allowed: {list(allowed[k])}", pos))
                bad = True
        if bad:
            continue
        if door and rules.in_hallway(n, pos):
            errors.append(_err("in_hallway", "the hallway must stay empty", pos))
            continue
        if walls and rules.in_shell(n, pos):
            errors.append(_err("in_shell", "this cell is a hallway wall and belongs to the harness", pos))
            continue
        blocks[pos] = (block_id, props)
    return True


def _check_pistons(blocks, errors):
    # Pistons and heads must agree, so a build cannot start with a half-formed piston.
    for pos, (bid, props) in blocks.items():
        if bid in ("minecraft:piston", "minecraft:sticky_piston") and props.get("extended") == "true":
            facing = props.get("facing", "north")
            want = "sticky" if bid == "minecraft:sticky_piston" else "normal"
            head = blocks.get(rules.step(pos, facing))
            if not head or head[0] != "minecraft:piston_head" or head[1].get("facing", "north") != facing \
                    or head[1].get("type", "normal") != want:
                errors.append(_err("piston_head_mismatch", f"extended piston needs a {want} piston_head facing {facing} in front of it", pos))
        if bid == "minecraft:piston_head":
            facing = props.get("facing", "north")
            want = "minecraft:sticky_piston" if props.get("type", "normal") == "sticky" else "minecraft:piston"
            base = blocks.get(rules.step(pos, facing, -1))
            if not base or base[0] != want or base[1].get("extended") != "true" or base[1].get("facing", "north") != facing:
                errors.append(_err("piston_head_mismatch", f"piston_head needs an extended {want} facing {facing} behind it", pos))


def validate_part(items, n, walls=False):
    """Checks a free-standing set of blocks for the lab. The allow-list, property and piston
    rules of a design apply; the door rules (one lever, doorway contents, empty hallway) do not.
    With `walls`, the hallway walls are present and their cells cannot be used."""
    errors, blocks = [], {}
    if not isinstance(items, list):
        return [_err("bad_format", "the lab takes a list of blocks, or a design object with a \"blocks\" list")], blocks
    if len(items) > rules.MAX_BLOCKS:
        return [_err("too_many_blocks", f"more than {rules.MAX_BLOCKS} blocks")], blocks
    if _read_blocks(items, n, errors, blocks, door=False, walls=walls):
        _check_pistons(blocks, errors)
    return errors[: MAX_ERRORS + 1], blocks


def validate(sub, n):
    errors, blocks = [], {}
    if not rules.valid_size(n):
        return [_err("bad_size", f"door size must be one of {rules.SIZES} or a [w, h] pair with sides 1..{rules.MAX_SIDE}, got {n!r}")], blocks
    if not isinstance(sub, dict) or not isinstance(sub.get("blocks"), list):
        return [_err("bad_format", 'submission must be an object with a "blocks" list')], blocks
    if sub.get("initial_state") not in ("open", "closed"):
        errors.append(_err("bad_initial_state", '"initial_state" must be "open" or "closed"'))
    if len(sub["blocks"]) > rules.MAX_BLOCKS:
        return errors + [_err("too_many_blocks", f"more than {rules.MAX_BLOCKS} blocks")], blocks

    if not _read_blocks(sub["blocks"], n, errors, blocks, door=True, walls=True):
        return errors, blocks

    levers = [p for p, (bid, _) in blocks.items() if bid == "minecraft:lever"]
    if len(levers) != 1:
        errors.append(_err("lever_count", f"exactly one lever is required, found {len(levers)}"))

    _check_pistons(blocks, errors)

    state = sub.get("initial_state")
    for cell in rules.doorway(n):
        got = blocks.get(cell)
        if state == "open" and got:
            errors.append(_err("doorway_block", "initial_state is open, so doorway cells must be empty", cell))
        elif state == "closed" and (not got or got[0] != rules.DOOR_BLOCK):
            errors.append(_err("doorway_block", f"initial_state is closed, so every doorway cell must hold {rules.DOOR_BLOCK}", cell))
        elif got and got[0] != rules.DOOR_BLOCK:
            errors.append(_err("doorway_block", f"doorway cells may only hold {rules.DOOR_BLOCK}", cell))
    return errors[: MAX_ERRORS + 1], blocks
