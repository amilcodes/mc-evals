package pd;

import com.google.gson.Gson;
import com.google.gson.JsonArray;
import com.google.gson.JsonElement;
import com.google.gson.JsonObject;
import com.google.gson.JsonParser;
import java.io.BufferedReader;
import java.io.FileDescriptor;
import java.io.FileOutputStream;
import java.io.InputStreamReader;
import java.io.PrintStream;
import java.io.PrintWriter;
import java.io.StringWriter;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.nio.file.StandardCopyOption;
import java.util.ArrayList;
import java.util.BitSet;
import java.util.Comparator;
import java.util.IdentityHashMap;
import java.util.List;
import java.util.Map;
import java.util.Optional;
import java.util.TreeSet;
import net.minecraft.SharedConstants;
import net.minecraft.commands.arguments.blocks.BlockStateParser;
import net.minecraft.core.BlockPos;
import net.minecraft.core.HolderLookup;
import net.minecraft.core.registries.Registries;
import net.minecraft.gametest.framework.GameTestServer;
import net.minecraft.server.Bootstrap;
import net.minecraft.server.MinecraftServer;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.server.packs.repository.PackRepository;
import net.minecraft.server.packs.repository.ServerPacksSource;
import net.minecraft.util.Util;
import net.minecraft.world.entity.Entity;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.level.ChunkPos;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.Blocks;
import net.minecraft.world.level.block.LeverBlock;
import net.minecraft.world.level.block.ObserverBlock;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.world.level.levelgen.structure.BoundingBox;
import net.minecraft.world.level.storage.LevelStorageSource;
import net.minecraft.world.phys.AABB;

/**
 * In-process simulation kernel for the piston-door grader.
 *
 * It starts Mojang's own headless test server (the same class the vanilla
 * {@code net.minecraft.gametest.Main} launcher uses), then takes over the server thread and
 * advances the world itself with {@link ServerLevel#tick}. Nothing in the game is patched.
 *
 * Protocol: one job per line on stdin (a path to a JSON job file). A job with
 * {@code "resume": true} continues the previous job's world without ticking. The result is written to
 * {@code <job>.result.json} and {@code PDK_DONE <job>} is printed. {@code quit} exits.
 * The kernel knows nothing about scoring rules; it places blocks, steps ticks and reports.
 */
public final class PdKernel {
    private static final int MARGIN = 2;          // cells scanned beyond the declared region
    private static final int ACTIVE_PAD = 4;      // per-tick scan pad around everything seen so far
    private static final int MAX_CHANGES = 600;   // change-log cap per run step
    private static final int SILENT = Block.UPDATE_CLIENTS | Block.UPDATE_SKIP_ALL_SIDEEFFECTS;

    private static final Gson GSON = new com.google.gson.GsonBuilder().serializeNulls().create();
    private static PrintStream out;

    private final MinecraftServer server;
    private final ServerLevel level;
    private final BufferedReader in;
    private final HolderLookup<Block> blocks;
    private final Map<BlockState, String> names = new IdentityHashMap<>();
    private final BlockState air = Blocks.AIR.defaultBlockState();

    // Per-job state. Scan box is the declared region grown by MARGIN, in world coordinates.
    private int ox, oy, oz;
    private int x0, y0, z0, x1, y1, z1;
    private int rx0, ry0, rz0, rx1, ry1, rz1;
    private int dx, dy, dz;
    private BlockState[] prev;
    private BitSet ignore, ever;
    private int[] swept;
    private boolean escaped;
    private int moving;
    private int n, w, h;  // door width (x) and height (y); n is kept for older jobs
    private Block doorBlock;
    private final List<int[]> frozenPos = new ArrayList<>();
    private final List<Block> frozenBlock = new ArrayList<>();
    private JsonObject frozenViolation;
    private JsonObject entitySeen;
    private long jobTick;
    private int changeCap = MAX_CHANGES;

    private PdKernel(MinecraftServer server, BufferedReader in) {
        this.server = server;
        this.level = server.overworld();
        this.in = in;
        this.blocks = level.registryAccess().lookupOrThrow(Registries.BLOCK);
    }

    public static void main(String[] args) throws Exception {
        // Bootstrap redirects System.out into the logger; keep the raw stream for the protocol.
        out = new PrintStream(new FileOutputStream(FileDescriptor.out), true, StandardCharsets.UTF_8);
        BufferedReader in = new BufferedReader(new InputStreamReader(System.in, StandardCharsets.UTF_8));
        Path universe = Paths.get(args[0]);

        SharedConstants.tryDetectVersion();
        Bootstrap.bootStrap();
        Util.startTimerHackThread();
        LevelStorageSource.LevelStorageAccess access =
            LevelStorageSource.createDefault(universe).createAccess("gametestworld");
        PackRepository packs = ServerPacksSource.createPackRepository(access);
        // "pd:hold" is a test that never finishes; it keeps the test server from shutting down.
        MinecraftServer server = MinecraftServer.spin(
            thread -> GameTestServer.create(thread, access, packs, Optional.of("pd:hold"), false, 1));
        while (!server.isReady()) {
            if (!server.isRunning()) {
                out.println("PDK_FATAL server stopped during start-up");
                Runtime.getRuntime().halt(2);
            }
            Thread.sleep(20);
        }
        // From here on the server thread belongs to the kernel and the server's own loop never
        // ticks again. Every tick is one explicit ServerLevel.tick call below.
        server.execute(() -> new PdKernel(server, in).loop());
    }

    private void loop() {
        try {
            out.println("PDK_READY " + SharedConstants.getCurrentVersion().name());
            String line;
            while ((line = in.readLine()) != null) {
                line = line.trim();
                if (line.isEmpty()) continue;
                if (line.equals("quit")) break;
                Path job = Paths.get(line);
                JsonObject res;
                try {
                    res = runJob(JsonParser.parseString(Files.readString(job)).getAsJsonObject());
                    res.addProperty("ok", true);
                } catch (Throwable t) {
                    StringWriter sw = new StringWriter();
                    t.printStackTrace(new PrintWriter(sw));
                    res = new JsonObject();
                    res.addProperty("ok", false);
                    res.addProperty("error", String.valueOf(t.getMessage()));
                    res.addProperty("trace", sw.toString());
                }
                Path tmp = Paths.get(line + ".result.tmp");
                Files.writeString(tmp, GSON.toJson(res));
                Files.move(tmp, Paths.get(line + ".result.json"), StandardCopyOption.REPLACE_EXISTING);
                out.println("PDK_DONE " + line);
            }
        } catch (Throwable t) {
            out.println("PDK_FATAL " + t);
        }
        Runtime.getRuntime().halt(0);
    }

    // ---------------------------------------------------------------- job

    private JsonObject runJob(JsonObject job) throws Exception {
        // A resumed job carries on in the world exactly as the previous job left it: same
        // region, same tracking, and not a single tick in between. Only its steps are read.
        boolean resume = job.has("resume") && job.get("resume").getAsBoolean();
        if (resume) {
            if (prev == null) throw new IllegalStateException("no earlier job to resume");
        } else {
            startJob(job);
        }

        JsonArray results = new JsonArray();
        for (JsonElement e : job.getAsJsonArray("steps")) {
            JsonObject step = e.getAsJsonObject();
            String op = step.get("op").getAsString();
            JsonObject r;
            switch (op) {
                case "clear" -> r = clear();
                case "place" -> r = place(step);
                case "lever" -> r = lever(step);
                case "run" -> r = run(step);
                case "snapshot" -> r = snapshot();
                default -> throw new IllegalArgumentException("unknown op " + op);
            }
            r.addProperty("op", op);
            if (step.has("label")) r.addProperty("label", step.get("label").getAsString());
            r.addProperty("game_time", level.getGameTime());
            results.add(r);
        }

        JsonObject res = new JsonObject();
        res.add("steps", results);
        res.add("swept", sweptJson());
        res.addProperty("swept_cells", ever.cardinality());
        res.addProperty("escaped", escaped);
        res.add("frozen_violation", frozenViolation);
        res.add("entity_seen", entitySeen);
        return res;
    }

    private void startJob(JsonObject job) throws Exception {
        int[] o = ints(job.getAsJsonArray("origin"));
        ox = o[0]; oy = o[1]; oz = o[2];
        int[] rmin = ints(job.getAsJsonObject("region").getAsJsonArray("min"));
        int[] rmax = ints(job.getAsJsonObject("region").getAsJsonArray("max"));
        rx0 = ox + rmin[0]; ry0 = oy + rmin[1]; rz0 = oz + rmin[2];
        rx1 = ox + rmax[0]; ry1 = oy + rmax[1]; rz1 = oz + rmax[2];
        x0 = rx0 - MARGIN; y0 = ry0 - MARGIN; z0 = rz0 - MARGIN;
        x1 = rx1 + MARGIN; y1 = ry1 + MARGIN; z1 = rz1 + MARGIN;
        if (y0 < level.getMinY() || y1 > level.getMaxY()) throw new IllegalArgumentException("region outside world height");
        dx = x1 - x0 + 1; dy = y1 - y0 + 1; dz = z1 - z0 + 1;
        if ((long) dx * dy * dz > 4_000_000L) throw new IllegalArgumentException("region too large");
        n = job.get("n").getAsInt();
        w = job.has("w") ? job.get("w").getAsInt() : n;
        h = job.has("h") ? job.get("h").getAsInt() : n;
        doorBlock = parse(job.get("door_block").getAsString()).getBlock();

        ensureChunks();
        resetTracking();

        ignore = new BitSet(dx * dy * dz);
        if (job.has("ignore")) {
            for (JsonElement e : job.getAsJsonArray("ignore")) {
                int[] p = ints(e.getAsJsonArray());
                ignore.set(idx(ox + p[0], oy + p[1], oz + p[2]));
            }
        }
        frozenPos.clear();
        frozenBlock.clear();
        if (job.has("frozen")) {
            for (JsonElement e : job.getAsJsonArray("frozen")) {
                JsonArray a = e.getAsJsonArray();
                int[] p = {ox + a.get(0).getAsInt(), oy + a.get(1).getAsInt(), oz + a.get(2).getAsInt()};
                frozenPos.add(p);
                frozenBlock.add(parse(a.get(3).getAsString()).getBlock());
                ignore.set(idx(p[0], p[1], p[2]));
            }
        }
    }

    private void resetTracking() {
        prev = new BlockState[dx * dy * dz];
        java.util.Arrays.fill(prev, air);
        ever = new BitSet(dx * dy * dz);
        swept = null;
        escaped = false;
        frozenViolation = null;
        entitySeen = null;
        jobTick = 0;
    }

    /**
     * Forces the chunks under the scan box (plus one ring) and waits until each is fully
     * ticking. A chunk only ticks its block entities, moving pistons included, once its
     * entity storage has finished loading on a background thread, so this waits in real time.
     */
    private void ensureChunks() throws InterruptedException {
        int cx0 = x0 >> 4, cx1 = x1 >> 4, cz0 = z0 >> 4, cz1 = z1 >> 4;
        for (int cx = cx0 - 1; cx <= cx1 + 1; cx++)
            for (int cz = cz0 - 1; cz <= cz1 + 1; cz++) {
                level.setChunkForced(cx, cz, true);
                level.getChunk(cx, cz);
            }
        // Chunk and entity-storage loading finish as tasks on the server thread, which this
        // kernel occupies, so hand the thread back for a moment on each pass.
        String waiting = "";
        for (int i = 0; i < 3000; i++) {
            long until = System.nanoTime() + 2_000_000L;
            server.managedBlock(() -> System.nanoTime() > until);
            level.tick(() -> true);
            waiting = "";
            for (int cx = cx0; cx <= cx1 && waiting.isEmpty(); cx++)
                for (int cz = cz0; cz <= cz1 && waiting.isEmpty(); cz++) {
                    long c = ChunkPos.pack(cx, cz);
                    if (!level.shouldTickBlocksAt(c)) waiting = "chunk " + cx + "," + cz + " not block-ticking";
                    else if (!level.areEntitiesLoaded(c)) waiting = "chunk " + cx + "," + cz + " entities not loaded";
                }
            if (waiting.isEmpty()) return;
        }
        throw new IllegalStateException("chunks never became fully ticking: " + waiting);
    }

    // ---------------------------------------------------------------- ops

    /** Empties the scan box and lets every leftover scheduled tick and block event drain. */
    private JsonObject clear() {
        BlockPos.MutableBlockPos p = new BlockPos.MutableBlockPos();
        for (int x = x0; x <= x1; x++)
            for (int y = y0; y <= y1; y++)
                for (int z = z0; z <= z1; z++) {
                    p.set(x, y, z);
                    if (!level.getBlockState(p).isAir()) level.setBlock(p, air, SILENT);
                }
        level.getBlockTicks().clearArea(new BoundingBox(x0, y0, z0, x1, y1, z1));
        for (Entity e : level.getEntitiesOfClass(Entity.class, box())) e.discard();
        for (int i = 0; i < 100; i++) level.tick(() -> true);
        for (Entity e : level.getEntitiesOfClass(Entity.class, box())) e.discard();
        int left = 0;
        for (int x = x0; x <= x1; x++)
            for (int y = y0; y <= y1; y++)
                for (int z = z0; z <= z1; z++)
                    if (!level.getBlockState(p.set(x, y, z)).isAir()) left++;
        resetTracking();
        JsonObject r = new JsonObject();
        r.addProperty("non_air_after_clear", left);
        return r;
    }

    /**
     * Places blocks in two passes, like a schematic paste followed by one round of updates:
     * first every block silently, then shape updates and neighbour updates in (x, y, z) order.
     */
    private JsonObject place(JsonObject step) throws Exception {
        TreeSet<BlockPos> placed = new TreeSet<>(
            Comparator.<BlockPos>comparingInt(q -> q.getX()).thenComparingInt(q -> q.getY()).thenComparingInt(q -> q.getZ()));
        for (JsonElement e : step.getAsJsonArray("blocks")) {
            JsonArray a = e.getAsJsonArray();
            BlockPos pos = new BlockPos(ox + a.get(0).getAsInt(), oy + a.get(1).getAsInt(), oz + a.get(2).getAsInt());
            if (pos.getX() < rx0 || pos.getX() > rx1 || pos.getY() < ry0 || pos.getY() > ry1
                || pos.getZ() < rz0 || pos.getZ() > rz1)
                throw new IllegalArgumentException("block outside region: " + a);
            level.setBlock(pos, parse(a.get(3).getAsString()), SILENT);
            placed.add(pos);
        }
        // An observer's own shape update would make it fire just for having been placed, which
        // a hand-built observer in Java Edition does not do. Rulebook 0.3 skips it; older runs set the flag.
        boolean observersFire = step.has("observers_fire_on_place") && step.get("observers_fire_on_place").getAsBoolean();
        for (BlockPos pos : placed) {
            BlockState s = level.getBlockState(pos);
            if (!observersFire && s.getBlock() instanceof ObserverBlock) continue;
            BlockState fixed = Block.updateFromNeighbourShapes(s, level, pos);
            if (fixed != s) level.setBlock(pos, fixed, Block.UPDATE_CLIENTS | Block.UPDATE_KNOWN_SHAPE);
        }
        for (BlockPos pos : placed) level.updateNeighborsAt(pos, level.getBlockState(pos).getBlock(), null);
        scan(true, null, 0);
        JsonObject r = new JsonObject();
        r.addProperty("placed", placed.size());
        return r;
    }

    private JsonObject lever(JsonObject step) {
        int[] l = ints(step.getAsJsonArray("pos"));
        BlockPos pos = new BlockPos(ox + l[0], oy + l[1], oz + l[2]);
        BlockState s = level.getBlockState(pos);
        JsonObject r = new JsonObject();
        if (!(s.getBlock() instanceof LeverBlock lever)) {
            r.addProperty("error", "no lever at " + pos.subtract(new BlockPos(ox, oy, oz)).toShortString() + ", found " + name(s));
            return r;
        }
        lever.pull(s, level, pos, null);
        r.addProperty("powered", level.getBlockState(pos).getValue(LeverBlock.POWERED));
        // Dust and other instant components change during the flip itself, before any tick.
        JsonArray instant = new JsonArray();
        scan(false, instant, 0);
        r.add("changes", instant);
        r.add("pos", step.getAsJsonArray("pos"));
        return r;
    }

    /** Ticks until nothing has changed for `quiet` ticks (and at least `min_ticks`), or `max_ticks`. */
    private JsonObject run(JsonObject step) {
        int maxTicks = step.get("max_ticks").getAsInt();
        int quiet = step.has("quiet") ? step.get("quiet").getAsInt() : Integer.MAX_VALUE;
        int minTicks = step.has("min_ticks") ? step.get("min_ticks").getAsInt() : 0;
        changeCap = step.has("max_changes") ? step.get("max_changes").getAsInt() : MAX_CHANGES;
        JsonArray door = new JsonArray();
        JsonArray changes = new JsonArray();
        int total = 0, ticks = 0, lastChange = 0, sinceChange = 0;
        boolean quiescent = false;
        door.add(doorString());
        while (ticks < maxTicks) {
            level.tick(() -> true);
            ticks++;
            jobTick++;
            int changed = scan(false, changes, ticks);
            total += changed;
            door.add(doorString());
            checkFrozen();
            checkEntities();
            if (changed > 0 || moving > 0) {
                lastChange = ticks;
                sinceChange = 0;
            } else {
                sinceChange++;
            }
            if (ticks >= minTicks && sinceChange >= quiet) {
                quiescent = true;
                break;
            }
        }
        changeCap = MAX_CHANGES;
        scan(true, null, 0);
        JsonObject r = new JsonObject();
        r.addProperty("ticks", ticks);
        r.addProperty("last_change_tick", lastChange);
        r.addProperty("quiescent", quiescent);
        r.addProperty("changes_total", total);
        r.addProperty("moving_at_end", moving);
        r.add("door", door);
        r.add("changes", changes);
        r.add("swept", sweptJson());
        return r;
    }

    private JsonObject snapshot() {
        scan(true, null, 0);
        JsonArray cells = new JsonArray();
        for (int x = x0; x <= x1; x++)
            for (int y = y0; y <= y1; y++)
                for (int z = z0; z <= z1; z++) {
                    BlockState s = prev[idx(x, y, z)];
                    if (s.isAir()) continue;
                    JsonArray c = new JsonArray();
                    c.add(x - ox); c.add(y - oy); c.add(z - oz); c.add(name(s));
                    cells.add(c);
                }
        JsonObject r = new JsonObject();
        r.add("cells", cells);
        return r;
    }

    // ---------------------------------------------------------------- tracking

    /**
     * Reads block states, logs differences from the last scan, and grows the swept box.
     * A full scan covers the whole scan box; otherwise only the box around everything seen so far.
     */
    private int scan(boolean full, JsonArray changes, int tick) {
        int ax0 = x0, ay0 = y0, az0 = z0, ax1 = x1, ay1 = y1, az1 = z1;
        if (!full) {
            if (swept == null) { moving = 0; return 0; }
            ax0 = Math.max(x0, swept[0] - ACTIVE_PAD); ay0 = Math.max(y0, swept[1] - ACTIVE_PAD);
            az0 = Math.max(z0, swept[2] - ACTIVE_PAD); ax1 = Math.min(x1, swept[3] + ACTIVE_PAD);
            ay1 = Math.min(y1, swept[4] + ACTIVE_PAD); az1 = Math.min(z1, swept[5] + ACTIVE_PAD);
        }
        int changed = 0;
        moving = 0;
        BlockPos.MutableBlockPos p = new BlockPos.MutableBlockPos();
        for (int x = ax0; x <= ax1; x++)
            for (int y = ay0; y <= ay1; y++)
                for (int z = az0; z <= az1; z++) {
                    BlockState cur = level.getBlockState(p.set(x, y, z));
                    int i = idx(x, y, z);
                    if (cur != prev[i]) {
                        changed++;
                        if (changes != null && changes.size() < changeCap) {
                            JsonArray c = new JsonArray();
                            c.add(tick); c.add(x - ox); c.add(y - oy); c.add(z - oz);
                            c.add(name(prev[i])); c.add(name(cur));
                            changes.add(c);
                        }
                        prev[i] = cur;
                    }
                    if (cur.isAir()) continue;
                    if (cur.is(Blocks.MOVING_PISTON)) moving++;
                    if (ignore != null && ignore.get(i)) continue;
                    ever.set(i);
                    if (swept == null) swept = new int[] {x, y, z, x, y, z};
                    else {
                        swept[0] = Math.min(swept[0], x); swept[1] = Math.min(swept[1], y); swept[2] = Math.min(swept[2], z);
                        swept[3] = Math.max(swept[3], x); swept[4] = Math.max(swept[4], y); swept[5] = Math.max(swept[5], z);
                    }
                    if (x < rx0 || x > rx1 || y < ry0 || y > ry1 || z < rz0 || z > rz1) escaped = true;
                }
        return changed;
    }

    private String doorString() {
        StringBuilder sb = new StringBuilder(w * h);
        BlockPos.MutableBlockPos p = new BlockPos.MutableBlockPos();
        for (int y = 0; y < h; y++)
            for (int x = 0; x < w; x++) {
                BlockState s = level.getBlockState(p.set(ox + x, oy + y, oz));
                sb.append(s.isAir() ? '.' : s.is(doorBlock) ? '#' : s.is(Blocks.MOVING_PISTON) ? 'm' : '?');
            }
        return sb.toString();
    }

    private void checkFrozen() {
        if (frozenViolation != null) return;
        BlockPos.MutableBlockPos p = new BlockPos.MutableBlockPos();
        for (int i = 0; i < frozenPos.size(); i++) {
            int[] f = frozenPos.get(i);
            BlockState s = level.getBlockState(p.set(f[0], f[1], f[2]));
            if (!s.is(frozenBlock.get(i))) {
                frozenViolation = new JsonObject();
                frozenViolation.addProperty("job_tick", jobTick);
                JsonArray pos = new JsonArray();
                pos.add(f[0] - ox); pos.add(f[1] - oy); pos.add(f[2] - oz);
                frozenViolation.add("pos", pos);
                frozenViolation.addProperty("found", name(s));
                return;
            }
        }
    }

    private void checkEntities() {
        if (entitySeen != null) return;
        List<Entity> es = level.getEntitiesOfClass(Entity.class, box());
        if (es.isEmpty()) return;
        entitySeen = new JsonObject();
        entitySeen.addProperty("job_tick", jobTick);
        entitySeen.addProperty("count", es.size());
        entitySeen.addProperty("type", EntityType.getKey(es.get(0).getType()).toString());
    }

    // ---------------------------------------------------------------- helpers

    private AABB box() {
        return new AABB(x0, y0, z0, x1 + 1, y1 + 1, z1 + 1);
    }

    private int idx(int x, int y, int z) {
        if (x < x0 || x > x1 || y < y0 || y > y1 || z < z0 || z > z1)
            throw new IllegalArgumentException("position outside scan box");
        return ((x - x0) * dy + (y - y0)) * dz + (z - z0);
    }

    private JsonElement sweptJson() {
        if (swept == null) return com.google.gson.JsonNull.INSTANCE;
        JsonObject s = new JsonObject();
        JsonArray mn = new JsonArray(), mx = new JsonArray();
        mn.add(swept[0] - ox); mn.add(swept[1] - oy); mn.add(swept[2] - oz);
        mx.add(swept[3] - ox); mx.add(swept[4] - oy); mx.add(swept[5] - oz);
        s.add("min", mn);
        s.add("max", mx);
        return s;
    }

    private BlockState parse(String s) throws Exception {
        return BlockStateParser.parseForBlock(blocks, s, false).blockState();
    }

    private String name(BlockState s) {
        return names.computeIfAbsent(s, BlockStateParser::serialize);
    }

    private static int[] ints(JsonArray a) {
        int[] r = new int[a.size()];
        for (int i = 0; i < r.length; i++) r[i] = a.get(i).getAsInt();
        return r;
    }
}
