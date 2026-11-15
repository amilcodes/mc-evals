"""Reference volumes per task, and the starting designs handed to agents.

STATUS: provisional. Entries with verified=False are builders' own claims from video
descriptions. They have not been rebuilt in this grader, and they were made under community
rules (often a button input, no rest requirement), so scores computed from them are
indicative only. Replace each with a volume this grader has measured before publishing.
A verified entry is the best design this grader has seen, not a proven optimum; a score
above 1 means the reference was beaten.
"""
from pathlib import Path

DESIGNS = Path(__file__).resolve().parent.parent / "reference_designs"

# (n, track) -> {"volume", "source", "verified"}. "verified" means this grader measured the
# volume on a design kept in reference_designs/ ("file").
REFERENCES = {
    (2, "seamless"): {"volume": 30, "source": "pilot 2026-11-09: 6x5x1, reached independently by two agents on their first test",
                      "verified": True, "file": "ref_2x2_seamless_30.json"},
    (2, "open"): {"volume": 24, "source": "the 2x2 seamless reference with its two floor frame blocks removed (6x4x1)",
                  "verified": True, "file": "ref_2x2_open_24.json"},
    # Far from the community claim of 56 (SacredRedstone 7x8x1 entity-free 3x3, 2017, self-reported,
    # not rebuilt here). The pilot door was made under rules 0.2; its one pre-powered repeater, there
    # to cancel the old placement pulse, is un-powered in the stored file so that it passes rules 0.3.
    (3, "seamless"): {"volume": 192, "source": "pilot 2026-11-09: 8x8x3, designed from scratch by one agent run", "verified": True,
                      "file": "ref_3x3_seamless_192.json", "community_claim": 56},
    (3, "open"): {"volume": 126, "source": "pilot 2026-11-09: 7x9x2, designed from scratch by one agent run", "verified": True,
                  "file": "ref_3x3_open_126.json"},
    # 3 wide, 2 tall. Four Fable and Opus runs reached 42 independently by three layouts and none went lower in three continues.
    ((3, 2), "seamless"): {"volume": 42, "source": "benchmark wave 4, 2026-11-15: 6x7x1, run w4-3x2-opus-b; passes all 11 placements",
                           "verified": True, "file": "ref_3x2_seamless_42.json"},
    (4, "seamless"): {"volume": 132, "source": "Br1ckcraft3r no-entity 0.9 s 4x4, 2026 (self-reported)", "verified": False},
    (5, "seamless"): {"volume": 504, "source": "WolfieNamira entityless observerless 5x5, 2022 (self-reported)", "verified": False},
}

# (n, track) -> (file in reference_designs/, measured volume). Working but deliberately bulky:
# what the improve variant hands the agent.
STARTING = {
    (2, "seamless"): ("start_2x2_110.json", 110),
    (2, "open"): ("start_2x2_110.json", 110),
    (3, "seamless"): ("start_3x3_1430.json", 1430),
    (3, "open"): ("start_3x3_1430.json", 1430),
}


# Changed-physics tasks: (n, track, sorted physics items) -> entry. A vanilla reference never
# applies to a changed-physics task.
PHYSICS_REFERENCES = {}


def _key(n, track):
    from .rules import norm
    return norm(n), track


def _entry(n, track, physics=None):
    if physics:
        from .rules import norm
        return PHYSICS_REFERENCES.get((norm(n), track, tuple(sorted(physics.items()))))
    return REFERENCES.get(_key(n, track))


def reference(n, track, physics=None):
    r = _entry(n, track, physics)
    return r["volume"] if r else None


def starting(n, track):
    s = STARTING.get(_key(n, track))
    return (DESIGNS / s[0], s[1]) if s else (None, None)


def verified(n, track, physics=None):
    r = _entry(n, track, physics)
    return bool(r and r["verified"])
