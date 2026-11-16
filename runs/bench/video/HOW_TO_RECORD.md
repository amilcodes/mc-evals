# Recording the Opus 5,236 door in real Minecraft

Needs Minecraft Java Edition 26.3, the version the benchmark ran on.

1. Create a new world: Creative, Superflat, cheats on. On the world-creation screen open
   **Data Packs** and drag `pdbench_opus_door_datapack.zip` in, or later copy the zip into
   `saves/<world>/datapacks/` and run `/reload`.
2. Place the door with its corner at (0, 100, 0):

   ```
   /place template pdbench:opus_5236_4x4 0 100 0
   ```

3. Flip the lever on and then off once:

   ```
   /setblock 0 109 11 minecraft:lever[face=wall,facing=west,powered=true]
   /setblock 0 109 11 minecraft:lever[face=wall,facing=west,powered=false]
   ```

   The benchmark's grader places blocks without observers firing, and normal Minecraft may let
   them fire. If they do, the door starts with four stray blocks in its doorway. The first close
   fills the doorway, and from then on it opens and closes correctly. This was checked over eight
   flips in the same game engine.
4. Stand in the hallway facing the door (the doorway is x 16 to 19, y 103 to 106, at z = 9):

   ```
   /tp @s 18 103 3 0 0
   ```

5. Start recording (OBS, or macOS Cmd-Shift-5) and flip the lever with the two commands above,
   waiting about 5 seconds between them. Closing takes 63 game ticks (just over 3 seconds) and
   opening 86 ticks (about 4.3 seconds). Do not change the game's tick rate.

For an overview shot, `/tp @s -6 115 -10 -35 30` looks down on the whole build from the front left.
