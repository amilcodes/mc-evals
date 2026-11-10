"""Client for daemon.py: call(tool, **args) -> text."""
import json, urllib.request

def call(tool, **args):
    req = urllib.request.Request("http://127.0.0.1:8877", data=json.dumps({"tool": tool, "args": args}).encode())
    with urllib.request.urlopen(req, timeout=900) as r:
        return json.loads(r.read())["text"]
