"""Re-checks every task file: the start build must fail and the reference solution must pass under the
task's physics. One kernel per physics setting, booted one at a time. Also refreshes refs/ and runs
the selftest in the vanilla session. Writes verify_all.json."""
import json
import os

import build_tasks as BT
import check as C
import selftest

groups = {}
for f in sorted(BT.TASKS.glob("*.json")):
    t = json.loads(f.read_text())
    groups.setdefault(json.dumps(t["physics"], sort_keys=True), []).append(t)
groups.setdefault("{}", [])
rows, extra = [], {}
for phys, tasks in sorted(groups.items()):
    st = os.statvfs("/private/tmp")
    if st.f_bavail * st.f_frsize < 300e6:
        raise SystemExit("low disk")
    with C.kernel_for(json.loads(phys)) as k:
        if phys == "{}":
            extra["refs"] = BT.refs(k)
            extra["selftest_ok"] = all(r["ok"] for r in selftest.run(k))
        for t in tasks:
            s, r = C.check(k, t["spec"], t["start_build"]), C.check(k, t["spec"], t["reference_solution"])
            rows.append({"id": t["id"], "physics": t["physics"], "start_fails": not s["pass"], "start_fail": C.brief(s)["fail"],
                         "reference_passes": r["pass"], "ok": (not s["pass"]) and r["pass"]})
            print(rows[-1], flush=True)
out = {"tasks": len(rows), "all_ok": all(r["ok"] for r in rows), **extra, "rows": rows}
(BT.HERE / "verify_all.json").write_text(json.dumps(out, indent=1))
BT.write_index()
print("ALL OK" if out["all_ok"] else "FAILURES", extra)
