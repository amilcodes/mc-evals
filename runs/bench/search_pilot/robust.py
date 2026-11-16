import sys, json, types, tempfile as _tf
sys.path.insert(0, "../../../grader"); sys.path.insert(0, ".")
import pdgrader.kernel as K
from pdgrader.grade import grade, translation_pass_rate, rotated_180
import census as C
K.tempfile = types.SimpleNamespace(mkdtemp=lambda prefix="", dir=None: _tf.mkdtemp(prefix=prefix, dir="/private/tmp/claude-501/census_k"))
seed = json.load(open("../w1/w1-fable-a/result.json"))["candidate"]
edits = {"observer": {"pos": [2,5,0], "to": ["observer", {"facing": "west"}]},
         "delay2": {"pos": [2,5,0], "to": ["repeater", {"facing": "west", "delay": "2"}]}}
out = {}
with K.Kernel(heap="1500M") as k:
    for name, e in edits.items():
        s = C.apply(seed, e)
        f = grade(k, s, 3, "seamless", "final")
        tr = translation_pass_rate(k, s, 3, "seamless", "final")
        rot = grade(k, rotated_180(s, 3), 3, "seamless", "final")
        out[name] = {"final": C.brief(f), "translations": tr["passed"], "translations_of": len(tr.get("results", tr.get("offsets", []))) or None, "rot180": C.brief(rot)}
        json.dump(s, open(f"fable70_{name}.json", "w"), indent=1)
    for p in ({"repeater_unit": 3}, {"observer_delay": 3}):
        pass
print(json.dumps(out, indent=1))
json.dump(out, open("robust_fable70.json", "w"), indent=1)
