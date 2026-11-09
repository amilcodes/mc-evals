import java.lang.reflect.Field;
import java.lang.reflect.Method;

/** Prints which feature flags the vanilla GameTestServer enables. Reflection only, so it
 *  compiles without Minecraft on the classpath. */
public class Flags {
    public static void main(String[] a) throws Exception {
        try {
            Class.forName("net.minecraft.SharedConstants").getMethod("tryDetectVersion").invoke(null);
            Class.forName("net.minecraft.server.Bootstrap").getMethod("bootStrap").invoke(null);
        } catch (Throwable t) {
            System.out.println("bootstrap skipped: " + t);
        }
        Class<?> ff = Class.forName("net.minecraft.world.flag.FeatureFlags");
        Object reg = ff.getField("REGISTRY").get(null);
        Class<?> gts = Class.forName("net.minecraft.gametest.framework.GameTestServer");
        Field f = gts.getDeclaredField("ENABLED_FEATURES");
        f.setAccessible(true);
        Object set = f.get(null);
        Method toNames = reg.getClass().getMethod("toNames", set.getClass());
        System.out.println("RESULT all flags            = " + toNames.invoke(reg, reg.getClass().getMethod("allFlags").invoke(reg)));
        System.out.println("RESULT default flags        = " + toNames.invoke(reg, ff.getField("DEFAULT_FLAGS").get(null)));
        System.out.println("RESULT gametest server flags = " + toNames.invoke(reg, set));
    }
}
