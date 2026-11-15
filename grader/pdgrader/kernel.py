"""Builds and drives the Java simulation kernel (kernel/src/pd/PdKernel.java)."""
import hashlib
import json
import os
import queue
import shutil
import subprocess
import tempfile
import threading
import time
from pathlib import Path

from . import nbt

ROOT = Path(__file__).resolve().parent.parent
CONFIG = ROOT / "config.json"
RUNTIME = ROOT / "runtime"
BUILD = ROOT / "kernel" / "build"
SOURCE = ROOT / "kernel" / "src" / "pd" / "PdKernel.java"
AGENT_SOURCE = ROOT / "kernel" / "agent" / "pd" / "PhysicsAgent.java"

# Changed-physics settings the agent understands, with their vanilla values. A Kernel started
# with physics={...} has those constants rewritten in Minecraft's classes as they load.
PHYSICS_DEFAULTS = {"repeater_unit": 2, "push_limit": 12, "observer_delay": 2, "observer_pulse": 2}

DATA_VERSION = 5023  # Minecraft Java 26.3
PACK_FORMAT = 121


class KernelError(RuntimeError):
    pass


def load_config():
    if not CONFIG.exists():
        raise KernelError("grader is not set up; run: python -m pdgrader setup --java-home <jdk25> --server-jar <server.jar>")
    return json.loads(CONFIG.read_text())


def _jars():
    jars = sorted(RUNTIME.glob("versions/*/server-*.jar")) + sorted(RUNTIME.glob("libraries/**/*.jar"))
    if not jars:
        raise KernelError("server libraries are not unpacked; run setup")
    return [str(j) for j in jars]


def _build_dir():
    """Compiled classes live in a folder named after the source's hash, so a changed source
    never overwrites classes that a running simulator is still loading from."""
    return BUILD / hashlib.sha256(SOURCE.read_bytes()).hexdigest()[:12]


def _compile(java_home):
    out = _build_dir()
    if out.exists():
        return out
    BUILD.mkdir(parents=True, exist_ok=True)
    tmp = Path(tempfile.mkdtemp(prefix="tmp-", dir=BUILD))
    subprocess.run([str(Path(java_home) / "bin" / "javac"), "-nowarn", "-d", str(tmp),
                    "-cp", os.pathsep.join(_jars()), str(SOURCE)], check=True)
    try:
        tmp.rename(out)  # atomic; if another process won the race, keep theirs
    except OSError:
        shutil.rmtree(tmp, ignore_errors=True)
    return out


def _agent_jar(java_home):
    """The changed-physics Java agent, built once per source hash like the kernel."""
    out = BUILD / ("agent-" + hashlib.sha256(AGENT_SOURCE.read_bytes()).hexdigest()[:12])
    jar = out / "pd-physics.jar"
    if jar.exists():
        return jar
    BUILD.mkdir(parents=True, exist_ok=True)
    tmp = Path(tempfile.mkdtemp(prefix="tmp-agent-", dir=BUILD))
    bin_ = Path(java_home) / "bin"
    subprocess.run([str(bin_ / "javac"), "-nowarn", "-d", str(tmp / "classes"), str(AGENT_SOURCE)], check=True)
    (tmp / "MANIFEST.MF").write_text("Premain-Class: pd.PhysicsAgent\n")
    subprocess.run([str(bin_ / "jar"), "cfm", str(tmp / "pd-physics.jar"), str(tmp / "MANIFEST.MF"), "-C", str(tmp / "classes"), "."], check=True)
    try:
        tmp.rename(out)
    except OSError:
        shutil.rmtree(tmp, ignore_errors=True)
    return jar


def physics_key(physics):
    """Only the settings that differ from vanilla, sorted; {} means vanilla."""
    physics = physics or {}
    unknown = set(physics) - set(PHYSICS_DEFAULTS)
    if unknown:
        raise KernelError(f"unknown physics settings: {sorted(unknown)}")
    return {k: int(v) for k, v in sorted(physics.items()) if int(v) != PHYSICS_DEFAULTS[k]}


def _classpath(java_home):
    return os.pathsep.join([str(_compile(java_home))] + _jars())


def setup(java_home, server_jar):
    """Unpack the server's bundled libraries, compile the kernel, and write config.json."""
    java_home, server_jar = Path(java_home).resolve(), Path(server_jar).resolve()
    java = java_home / "bin" / "java"
    RUNTIME.mkdir(exist_ok=True)
    # Mojang's bundler unpacks its libraries into the working directory on any launch.
    subprocess.run(
        [str(java), "-DbundlerMainClass=net.minecraft.gametest.Main", "-jar", str(server_jar), "--help"],
        cwd=RUNTIME, capture_output=True, check=True,
    )
    _compile(java_home)
    CONFIG.write_text(json.dumps({"java_home": str(java_home), "server_jar": str(server_jar)}, indent=2))


def _write_hold_pack(world_dir):
    """A test that never finishes, so the vanilla test server stays up for the kernel."""
    pack = world_dir / "datapacks" / "pdhold"
    (pack / "data" / "pd" / "structure").mkdir(parents=True)
    (pack / "data" / "pd" / "test_instance").mkdir(parents=True)
    (pack / "pack.mcmeta").write_text(
        json.dumps({"pack": {"description": "pdgrader hold", "min_format": PACK_FORMAT, "max_format": PACK_FORMAT}})
    )
    blocks = [
        {"pos": [0, 0, 0], "id": "minecraft:stone"},
        {
            "pos": [0, 1, 0],
            "id": "minecraft:test_block",
            "props": {"mode": "start"},
            "nbt": {"id": "minecraft:test_block", "mode": "start", "message": ""},
        },
    ]
    (pack / "data" / "pd" / "structure" / "hold.nbt").write_bytes(nbt.structure_bytes(blocks, DATA_VERSION, [1, 2, 1]))
    (pack / "data" / "pd" / "test_instance" / "hold.json").write_text(
        json.dumps(
            {
                "type": "minecraft:block_based",
                "environment": "minecraft:default",
                "structure": "pd:hold",
                "max_ticks": 2000000000,
                "setup_ticks": 0,
                "required": True,
            }
        )
    )


class Kernel:
    """One long-lived simulator process. Use as a context manager; call run_job() repeatedly."""

    def __init__(self, heap="2G", boot_timeout=120, physics=None):
        cfg = load_config()
        self.physics = physics_key(physics)
        agent = []
        if self.physics:
            args = ",".join(f"{k}={v}" for k, v in self.physics.items())
            agent = [f"-javaagent:{_agent_jar(cfg['java_home'])}={args}"]
        self.dir = Path(tempfile.mkdtemp(prefix="pdk-", dir=RUNTIME))
        _write_hold_pack(self.dir / "universe" / "gametestworld")
        self.log = []
        self._lines = queue.Queue()
        self._n = 0
        t0 = time.monotonic()
        self.proc = subprocess.Popen(
            [str(Path(cfg["java_home"]) / "bin" / "java"), f"-Xmx{heap}", *agent, "-cp", _classpath(cfg["java_home"]), "pd.PdKernel", "universe"],
            cwd=self.dir, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1,
        )
        threading.Thread(target=self._pump, daemon=True).start()
        self.version = self._wait("PDK_READY", boot_timeout)
        applied = {line.split()[1] for line in self.log if line.startswith("PDK_PHYSICS ")}
        if set(self.physics) - applied:
            self.close()
            raise KernelError(f"physics settings not applied: {sorted(set(self.physics) - applied)}; log tail: {self.log[-15:]}")
        self._job_lock = threading.Lock()   # one job at a time; several sessions may share a kernel
        self.boot_seconds = round(time.monotonic() - t0, 2)

    def _pump(self):
        for line in self.proc.stdout:
            line = line.rstrip("\n")
            self.log.append(line)
            if line.startswith("PDK_"):
                self._lines.put(line)
        self._lines.put("PDK_EOF")

    def _wait(self, prefix, timeout):
        deadline = time.monotonic() + timeout
        while True:
            try:
                line = self._lines.get(timeout=max(0.01, deadline - time.monotonic()))
            except queue.Empty:
                raise KernelError(f"kernel timed out waiting for {prefix}; log tail: {self.log[-15:]}")
            if line.startswith(prefix):
                return line[len(prefix):].strip()
            if line.startswith(("PDK_FATAL", "PDK_EOF")):
                raise KernelError(f"kernel died: {line}; log tail: {self.log[-15:]}")

    def run_job(self, job, timeout=600):
        with self._job_lock:
            return self._run_job(job, timeout)

    def _run_job(self, job, timeout):
        self._n += 1
        path = self.dir / f"job{self._n}.json"
        path.write_text(json.dumps(job))
        self.proc.stdin.write(str(path) + "\n")
        self.proc.stdin.flush()
        self._wait("PDK_DONE", timeout)
        result_path = Path(str(path) + ".result.json")
        result = json.loads(result_path.read_text())
        path.unlink()
        result_path.unlink()
        if not result.get("ok"):
            raise KernelError(f"kernel job failed: {result.get('error')}\n{result.get('trace', '')}")
        return result

    def close(self):
        try:
            if self.proc.poll() is None:
                self.proc.stdin.write("quit\n")
                self.proc.stdin.flush()
                self.proc.wait(timeout=20)
        except Exception:
            self.proc.kill()
        for pipe in (self.proc.stdin, self.proc.stdout):
            try:
                pipe.close()
            except Exception:
                pass
        shutil.rmtree(self.dir, ignore_errors=True)

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        self.close()
