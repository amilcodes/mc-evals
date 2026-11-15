"""Inspect AI task for the piston-door eval.

    inspect eval inspect_task/piston_door.py --model <provider/model> -T sizes=2,3 -T tracks=seamless

Each sample is one door size and track. The agent gets the task brief, six door tools and
six lab tools (a free-form world for trying out parts one tick at a time). The
tools and the scorer run in the Inspect host process, outside any sandbox the agent has, so
the simulator, the server-side log and the final-test parameters are out of the agent's reach.
With use_sandbox=true the agent also gets bash and python in a Docker sandbox and may pass
the path of a design file instead of JSON text.
"""
import json
import os
import sys
from pathlib import Path

import anyio
from inspect_ai import Task, task
from inspect_ai.agent import AgentSubmit, react
from inspect_ai.dataset import Sample
from inspect_ai.scorer import Score, Target, mean, scorer, stderr
from inspect_ai.solver import Generate, TaskState, solver
from inspect_ai.tool import bash, python, tool
from inspect_ai.util import sandbox, store

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from pdgrader import kit, references, rules, server  # noqa: E402
from pdgrader.kernel import Kernel  # noqa: E402
from pdgrader.session import Session  # noqa: E402

LOG_DIR = Path(os.environ.get("PD_LOG_DIR", ROOT.parent / "runs" / "inspect"))
_SESSIONS, _KERNELS = {}, {}


async def _call(name, **args):
    for key in ("design", "blocks"):   # JSON text, or the path of a file in the sandbox
        value = args.get(key)
        if isinstance(value, str):
            text = value.strip()
            if not text.startswith(("{", "[")):
                try:
                    text = await sandbox().read_file(text)
                except Exception as e:
                    return f"could not read a file at {value!r}: {e}"
            try:
                args[key] = json.loads(text)
            except ValueError as e:
                return f"the {key} argument is not valid JSON: {e}"
    session = _SESSIONS[store().get("pd_key")]
    return await anyio.to_thread.run_sync(lambda: session.call(name, args))


@tool
def pd_status():
    async def execute() -> str:
        """Show the task, the remaining call budget and the best result so far."""
        return await _call("status")

    return execute


@tool
def pd_blocks():
    async def execute() -> str:
        """List the allowed blocks and their properties."""
        return await _call("blocks")

    return execute


@tool
def pd_test():
    async def execute(design: str) -> str:
        """Run the full test on a design: valid or not, why not, volume and timings. Uses one test call.

        Args:
            design: The design as JSON text.
        """
        return await _call("test", design=design)

    return execute


@tool
def pd_trace():
    async def execute(design: str, flips: int = 2, ticks: int = 0, grep: str = "") -> str:
        """Show every block change, tick by tick, after placement and after each lever flip. Uses one trace/view call.

        Args:
            design: The design as JSON text.
            flips: Number of lever flips to simulate.
            ticks: Maximum ticks to run after each flip; 0 means the task's time cap.
            grep: If set, only show change lines containing this text, for example "piston".
        """
        return await _call("trace", design=design, flips=flips, ticks=ticks or None, grep=grep or None)

    return execute


@tool
def pd_view():
    async def execute(design: str, flips: int = 0, z: str = "") -> str:
        """Draw the build as ASCII, one grid per z layer. Uses one trace/view call.

        Args:
            design: The design as JSON text.
            flips: Show the state after this many lever flips.
            z: Only these layers, for example "0" or "-1..2". Empty means all layers the build touches.
        """
        return await _call("view", design=design, flips=flips, z=z or None)

    return execute


@tool
def pd_submit():
    async def execute(design: str) -> str:
        """Nominate a design for final scoring. You may call this again; the last one counts.

        Args:
            design: The design as JSON text.
        """
        return await _call("submit", design=design)

    return execute


@tool
def pd_lab_new():
    async def execute(blocks: str, walls: bool = False) -> str:
        """Empty the lab world and place these blocks in it. The lab clock restarts at 0. Free.

        Args:
            blocks: A JSON list of blocks, or a whole design, as JSON text. The door rules do not apply.
            walls: Also place the hallway walls.
        """
        return await _call("lab_new", blocks=blocks, walls=walls)

    return execute


@tool
def pd_lab_flip():
    async def execute(x: int, y: int, z: int) -> str:
        """Flip the lever at a position in the lab. No tick passes. Free.

        Args:
            x: The lever's x.
            y: The lever's y.
            z: The lever's z.
        """
        return await _call("lab_flip", pos=[x, y, z])

    return execute


@tool
def pd_lab_step():
    async def execute(ticks: int = 1, grep: str = "") -> str:
        """Advance the lab by exactly this many game ticks and list every block change. Uses that many lab ticks.

        Args:
            ticks: How many ticks to advance, from 1 to 2000.
            grep: If set, only show change lines containing this text.
        """
        return await _call("lab_step", ticks=ticks, grep=grep or None)

    return execute


@tool
def pd_lab_rest():
    async def execute(max_ticks: int = 200, grep: str = "") -> str:
        """Advance the lab until no block has changed for 20 ticks in a row. Uses one lab tick per tick advanced.

        Args:
            max_ticks: Give up after this many ticks.
            grep: If set, only show change lines containing this text.
        """
        return await _call("lab_rest", max_ticks=max_ticks, grep=grep or None)

    return execute


@tool
def pd_lab_look():
    async def execute(cells: str = "", grep: str = "") -> str:
        """Show the current state of the lab's blocks and of the doorway. No tick passes. Free.

        Args:
            cells: Only these cells, as a JSON list such as [[1, 3, 0], [1, 4, 0]]. Empty means every block.
            grep: If set, only show lines containing this text.
        """
        try:
            wanted = json.loads(cells) if cells.strip() else None
        except ValueError as e:
            return f"cells is not valid JSON: {e}"
        return await _call("lab_look", cells=wanted, grep=grep or None)

    return execute


@tool
def pd_lab_view():
    async def execute(z: str = "") -> str:
        """Draw the lab as it is now as ASCII, one grid per z layer. No tick passes. Free.

        Args:
            z: Only these layers, for example "0" or "-1..2". Empty means all layers the blocks touch.
        """
        return await _call("lab_view", z=z or None)

    return execute


@solver
def open_session(tests: int, sims: int, lab_ticks: int, minutes):
    async def solve(state: TaskState, generate: Generate) -> TaskState:
        key = f"{state.sample_id}-e{state.epoch}-{state.uuid}"
        log = LOG_DIR / f"{key}.jsonl"

        def start():
            k = Kernel()
            return k, Session(k, state.metadata["n"], state.metadata["track"], log,
                              budget={"test": tests, "sim": sims, "lab": lab_ticks},
                              variant=state.metadata.get("variant", "scratch"), minutes=minutes)

        _KERNELS[key], _SESSIONS[key] = await anyio.to_thread.run_sync(start)
        store().set("pd_key", key)
        store().set("pd_log", str(log))
        return state

    return solve


async def close_session(state: TaskState) -> None:
    key = state.store.get("pd_key")
    s = _SESSIONS.pop(key, None)
    if s:
        await anyio.to_thread.run_sync(s.close)   # the lab's simulator, if one was started
    k = _KERNELS.pop(key, None)
    if k:
        await anyio.to_thread.run_sync(k.close)


@scorer(metrics=[mean(), stderr()])
def final_test():
    """The final test in a fresh simulator. Value: reference / volume, or 1 for valid when no reference exists."""

    async def score(state: TaskState, target: Target) -> Score:
        n, track = state.metadata["n"], state.metadata["track"]
        ref = references.reference(n, track)
        r = await anyio.to_thread.run_sync(lambda: server.score(state.store.get("pd_log"), reference=ref))
        if not r["valid"]:
            value = 0.0
            why = "; ".join(f["code"] for f in r.get("final_failures") or []) or "no design to score"
            explanation = f"invalid: {why}; furthest progress in any test {r.get('best_partial', 0.0)}"
        else:
            value = r["score"] if ref else 1.0
            t = r.get("translations") or {}
            explanation = (f"valid, volume {r['volume']} {r['dims']}" + (f", {'reference' if references.verified(n, track) else 'unverified reference'} {ref}" if ref else ", no reference yet")
                           + (f", shifted/turned placements {t['passed']}/{t['of']}" if t else ""))
        return Score(value=value, answer=str(r["volume"]), explanation=explanation,
                     metadata={k: v for k, v in r.items() if k != "candidate"})

    return score


def _list(v, cast):
    if isinstance(v, (list, tuple)):
        return [cast(x) for x in v]
    return [cast(x) for x in str(v).split(",") if str(x).strip()]


@task
def piston_door(sizes="2,3", tracks="open,seamless", variants="scratch", tests: int = 120, sims: int = 300,
                lab_ticks: int = 50000, minutes: int = 0, use_sandbox: bool = False, message_limit: int = 600):
    """variants: "scratch" (design from nothing), "improve" (shrink a working but bulky design), or both.

    The improve variant exists only for tasks with a starting design in references.py; others are skipped.
    minutes: wall-clock limit counted from the agent's first tool call; 0 means none.
    """
    budget = {"test": tests, "sim": sims, "lab": lab_ticks}
    samples = []
    for n in [rules.norm(s) for s in _list(sizes, str)]:
        for track in _list(tracks, str):
            for variant in _list(variants, str):
                start, start_volume = None, None
                if variant == "improve":
                    start_path, start_volume = references.starting(n, track)
                    if not start_path:
                        continue
                    start = json.loads(start_path.read_text())
                samples.append(Sample(
                    id=f"{rules.label(n)}-{track}-{variant}",
                    input=kit.brief(n, track, budget, "tools", start, start_volume, sandbox=use_sandbox, minutes=minutes or None),
                    metadata={"n": list(n) if isinstance(n, tuple) else n, "track": track, "variant": variant},
                ))
    tools = [pd_status(), pd_blocks(), pd_test(), pd_trace(), pd_view(), pd_submit(),
             pd_lab_new(), pd_lab_flip(), pd_lab_step(), pd_lab_rest(), pd_lab_look(), pd_lab_view()]
    if use_sandbox:
        tools += [bash(timeout=180), python(timeout=180)]
    return Task(
        dataset=samples,
        setup=open_session(tests, sims, lab_ticks, minutes or None),
        solver=react(tools=tools, submit=AgentSubmit(name="finish", description="End the run. Call pd_submit first.")),
        scorer=final_test(),
        cleanup=close_session,
        sandbox="docker" if use_sandbox else None,
        message_limit=message_limit,
        # The tools refuse work after `minutes`; this ends the sample itself 10 minutes later.
        time_limit=(minutes + 10) * 60 if minutes else None,
    )
