"""Runs the Inspect task end to end with a scripted mock model (no API key needed)."""
import json
import sys
from pathlib import Path

from inspect_ai import eval as inspect_eval
from inspect_ai.model import ModelOutput, get_model

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from piston_door import piston_door  # noqa: E402

M = "mockllm/model"
design = (HERE.parent / "fixtures" / "good_2x2.json").read_text()
LEVER = next(b["pos"] for b in json.loads(design)["blocks"] if b["id"] == "lever")
broken = json.dumps({"initial_state": "open", "blocks": [{"pos": [0, 0, 1], "id": "stone"}]})
script = [
    ModelOutput.for_tool_call(M, "pd_status", {}),
    ModelOutput.for_tool_call(M, "pd_test", {"design": broken}),
    ModelOutput.for_tool_call(M, "pd_test", {"design": design}),
    ModelOutput.for_tool_call(M, "pd_view", {"design": design, "flips": 1, "z": "0"}),
    ModelOutput.for_tool_call(M, "pd_trace", {"design": design, "flips": 1, "grep": "piston_head"}),
    ModelOutput.for_tool_call(M, "pd_lab_new", {"blocks": design, "walls": True}),
    ModelOutput.for_tool_call(M, "pd_lab_flip", {"x": LEVER[0], "y": LEVER[1], "z": LEVER[2]}),
    ModelOutput.for_tool_call(M, "pd_lab_step", {"ticks": 3, "grep": "piston_head"}),
    ModelOutput.for_tool_call(M, "pd_lab_rest", {}),
    ModelOutput.for_tool_call(M, "pd_lab_look", {"cells": "[[0, 0, 0], [1, 1, 0]]"}),
    ModelOutput.for_tool_call(M, "pd_lab_view", {"z": "0"}),
    ModelOutput.for_tool_call(M, "pd_submit", {"design": design}),
    ModelOutput.for_tool_call(M, "finish", {"answer": "submitted"}),
]
logs = inspect_eval(piston_door(sizes="2", tracks="seamless", tests=5, sims=5, minutes=30), model=get_model(M, custom_outputs=script),
                    log_dir=str(HERE.parent.parent / "runs" / "inspect" / "logs"), display="none")
log = logs[0]
print("status:", log.status)
sample = log.samples[0]
for m in sample.messages:
    if m.role == "tool":
        print(f"--- tool {m.function}:\n" + "\n".join(str(m.content).splitlines()[:6]))
tool_text = {m.function: str(m.content) for m in sample.messages if m.role == "tool"}
lab_ok = ("Lab 1 started" in tool_text["pd_lab_new"] and "switched on" in tool_text["pd_lab_flip"]
          and "t=0 -> t=3" in tool_text["pd_lab_step"] and "at rest" in tool_text["pd_lab_rest"]
          and "doorway ##/##" in tool_text["pd_lab_look"] and "Lab at t=" in tool_text["pd_lab_view"]
          and all("[time left: " in t for t in tool_text.values()) and "**30 minutes**" in sample.input)
for name, s in sample.scores.items():
    print("score:", name, s.value, "|", s.explanation)
# The mock submits the bulky 110-volume starting door; the verified 2x2 reference is 30.
ok = log.status == "success" and list(sample.scores.values())[0].value == round(30 / 110, 4) and lab_ok
print("SMOKE OK" if ok else "SMOKE FAILED")
sys.exit(0 if ok else 1)
