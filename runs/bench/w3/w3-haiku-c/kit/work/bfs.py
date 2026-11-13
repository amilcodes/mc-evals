# Logical search: which sequences of single piston strokes move a 3x3 door (12 stones) between open and closed.
# Region: 5x5 at z=0 minus corners. Pistons only at distance 2 outside frame (rows y=0..2 at x=-2,4; columns x=0..2 at y=-2,4).
from collections import deque
import sys

def inreg(c):
    x, y = c
    if not (-1 <= x <= 3 and -1 <= y <= 3): return False
    if x in (-1, 3) and y in (-1, 3): return False
    return True

cells = [(x, y) for x in range(-1, 4) for y in range(-1, 4) if inreg((x, y))]
idx = {c: i for i, c in enumerate(cells)}
D = [(x, y) for x in range(3) for y in range(3)]
F = [(-1, y) for y in range(3)] + [(3, y) for y in range(3)] + [(x, -1) for x in range(3)] + [(x, 3) for x in range(3)]
def bit(c): return 1 << idx[c]
def mask(cs):
    m = 0
    for c in cs: m |= bit(c)
    return m

pistons = []
for y in range(3):
    pistons.append(((-2, y), (1, 0)))
    pistons.append(((4, y), (-1, 0)))
for x in range(3):
    pistons.append(((x, -2), (0, 1)))
    pistons.append(((x, 4), (0, -1)))
P = len(pistons)

def shift_chain(S, start, d, sign_shift):
    """Chain of stones starting at 'start' going in direction d; shift them by sign*d if the end is free.
    Returns new S or None."""
    dx, dy = d
    chain = []
    c = start
    while c in idx and (S >> idx[c]) & 1:
        chain.append(c)
        c = (c[0] + dx, c[1] + dy)
    if not chain: return None
    # shift direction
    s = sign_shift
    sx, sy = dx * s, dy * s
    if s > 0:
        end = (chain[-1][0] + sx, chain[-1][1] + sy)
        # pushing +d: need the cell after the chain free
        if end not in idx or (S >> idx[end]) & 1: return None
    else:
        # pulling: target cell is start - d which must be free and in region
        tgt = (chain[0][0] + sx, chain[0][1] + sy)
        if tgt not in idx or (S >> idx[tgt]) & 1: return None
    newS = S
    for c in chain: newS &= ~bit(c)
    for c in chain: newS |= bit((c[0] + sx, c[1] + sy))
    return newS

def moves(state):
    S, H = state  # H: bitmask of extended heads, need per-piston flags: use ext bits
    ext = H >> 0
    res = []
    for i, ((px, py), (dx, dy)) in enumerate(pistons):
        hcell = (px + dx, py + dy)
        if not inreg(hcell): continue
        hb = bit(hcell)
        isext = (ext >> i) & 1
        if not isext:
            # extend
            if (S | (H & ~ext_mask_all())) & hb == 0 and True:
                pass
        # handled below via explicit state layout
    return res

# State layout: S (stone bits over cells), HEAD (bits over cells where heads are), EXT (bits over pistons).
def step_states(state):
    S, HEAD, EXT = state
    out = []
    for i, ((px, py), (dx, dy)) in enumerate(pistons):
        h = (px + dx, py + dy)
        hb = bit(h)
        d = (dx, dy)
        p2 = (px + 2 * dx, py + 2 * dy)
        if not (EXT >> i) & 1:
            # extend
            occupied = (S | HEAD) & hb
            if not occupied:
                out.append(('ext', i, (S, HEAD | hb, EXT | (1 << i))))
            elif (S & hb):
                newS = shift_chain(S, h, d, +1)
                if newS is not None:
                    out.append(('push', i, (newS, HEAD | hb, EXT | (1 << i))))
        else:
            # retract: remove head
            H2 = HEAD & ~hb
            E2 = EXT & ~(1 << i)
            out.append(('ret', i, (S, H2, E2)))
            if sticky[i] and p2 in idx and (S >> idx[p2]) & 1:
                newS = shift_chain(S, p2, d, -1)
                if newS is not None:
                    out.append(('pull', i, (newS, H2, E2)))
    return out

sticky = [True] * P
