package pd;

import java.lang.classfile.ClassFile;
import java.lang.classfile.ClassModel;
import java.lang.classfile.ClassTransform;
import java.lang.classfile.CodeBuilder;
import java.lang.classfile.CodeElement;
import java.lang.classfile.CodeTransform;
import java.lang.classfile.instruction.ConstantInstruction;
import java.lang.classfile.instruction.InvokeInstruction;
import java.lang.instrument.ClassFileTransformer;
import java.lang.instrument.Instrumentation;
import java.security.ProtectionDomain;
import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

/**
 * Changed-physics variants for the piston-door benchmark.
 *
 * A Java agent that rewrites a few integer constants in Minecraft's own classes as they load,
 * so the server jar on disk is never modified. Arguments are comma-separated key=value pairs:
 *
 *   repeater_unit   game ticks per repeater delay step (vanilla 2: delays 1-4 are 2, 4, 6, 8 ticks)
 *   push_limit      most blocks a piston can move (vanilla 12)
 *   observer_delay  ticks from a watched change to the observer's output (vanilla 2)
 *   observer_pulse  ticks the observer's output stays on (vanilla 2)
 *
 * Every patch must find exactly the number of constants it expects, or the kernel refuses to
 * start (PDK_PHYSICS_ERROR). Each applied patch prints a PDK_PHYSICS line.
 */
public final class PhysicsAgent {

    record Patch(String key, String cls, String method, int from, int expect, String beforeInvoke) {}

    static final List<Patch> PATCHES = List.of(
        new Patch("repeater_unit", "net/minecraft/world/level/block/RepeaterBlock", "getDelay", 2, 1, null),
        new Patch("push_limit", "net/minecraft/world/level/block/piston/PistonStructureResolver", null, 12, 3, null),
        new Patch("observer_delay", "net/minecraft/world/level/block/ObserverBlock", "startSignal", 2, 1, "scheduleTick"),
        new Patch("observer_pulse", "net/minecraft/world/level/block/ObserverBlock", "tick", 2, 1, "scheduleTick"));

    public static void premain(String args, Instrumentation inst) {
        Map<String, Integer> values = new LinkedHashMap<>();
        for (String kv : (args == null ? "" : args).split(",")) {
            if (kv.isBlank()) continue;
            String[] p = kv.split("=");
            if (p.length != 2 || PATCHES.stream().noneMatch(x -> x.key().equals(p[0].trim())))
                throw new IllegalArgumentException("unknown physics setting: " + kv);
            values.put(p[0].trim(), Integer.parseInt(p[1].trim()));
        }
        inst.addTransformer(new ClassFileTransformer() {
            @Override
            public byte[] transform(Module module, ClassLoader loader, String name, Class<?> redefined, ProtectionDomain pd, byte[] bytes) {
                if (name == null) return null;
                List<Patch> mine = new ArrayList<>();
                for (Patch p : PATCHES) if (p.cls().equals(name) && values.containsKey(p.key())) mine.add(p);
                if (mine.isEmpty()) return null;
                try {
                    for (Patch p : mine) bytes = apply(bytes, p, values.get(p.key()));
                    return bytes;
                } catch (Throwable t) {
                    System.out.println("PDK_PHYSICS_ERROR " + name + " " + t);
                    System.out.flush();
                    Runtime.getRuntime().halt(3);
                    return null;
                }
            }
        });
        // Load (without initializing) every class to patch now, so all patches are applied and
        // reported before the kernel says it is ready, not lazily on first use.
        for (Patch p : PATCHES) {
            if (!values.containsKey(p.key())) continue;
            try {
                Class.forName(p.cls().replace('/', '.'), false, ClassLoader.getSystemClassLoader());
            } catch (ClassNotFoundException e) {
                System.out.println("PDK_PHYSICS_ERROR " + p.cls() + " not found");
                System.out.flush();
                Runtime.getRuntime().halt(3);
            }
        }
    }

    static byte[] apply(byte[] bytes, Patch p, int to) {
        int[] count = {0};
        ClassFile cf = ClassFile.of();
        ClassModel cm = cf.parse(bytes);
        byte[] out = cf.transformClass(cm, ClassTransform.transformingMethodBodies(
            m -> p.method() == null || m.methodName().equalsString(p.method()),
            new Swap(p, to, count)));
        if (count[0] != p.expect())
            throw new IllegalStateException(p.key() + ": expected " + p.expect() + " constant(s) " + p.from() + ", found " + count[0]);
        System.out.println("PDK_PHYSICS " + p.key() + " " + p.from() + "->" + to + " (" + count[0] + " site(s) in " + p.cls() + ")");
        System.out.flush();
        return out;
    }

    /** Replaces the integer constant `from`; with beforeInvoke set, only where the next instruction calls that method. */
    static final class Swap implements CodeTransform {
        final Patch p; final int to; final int[] count;
        ConstantInstruction pending;

        Swap(Patch p, int to, int[] count) { this.p = p; this.to = to; this.count = count; }

        static boolean matches(CodeElement e, int v) {
            return e instanceof ConstantInstruction ci && ci.constantValue() instanceof Integer i && i == v;
        }

        @Override
        public void accept(CodeBuilder b, CodeElement e) {
            if (p.beforeInvoke() == null) {
                if (matches(e, p.from())) { b.loadConstant(to); count[0]++; }
                else b.with(e);
                return;
            }
            if (pending != null) {
                if (e instanceof InvokeInstruction inv && inv.name().equalsString(p.beforeInvoke())) { b.loadConstant(to); count[0]++; }
                else b.with(pending);
                pending = null;
            }
            if (matches(e, p.from())) pending = (ConstantInstruction) e;
            else b.with(e);
        }

        @Override
        public void atEnd(CodeBuilder b) {
            if (pending != null) b.with(pending);
            pending = null;
        }
    }
}
