#!/bin/zsh
export RSG_LIVE_IN_TERMINAL=1
export PYTHONUNBUFFERED=1
export RSG__CLIENT__GUI_SCALE=3
export RSG__CLIENT__WINDOW_WIDTH=2992
export RSG__CLIENT__WINDOW_HEIGHT=1800
export RSG__CLIENT__GAMMA=5.0
export RSG__CLIENT__FOV_NORMAL=110
export RSG__CLIENT__RENDER_DISTANCE=12
export RSG__CLIENT__MOUSE_SENSITIVITY=0.5
export RSG__CLIENT__PAUSE_ON_LOST_FOCUS=false
export RSG__RUN__PREFERRED_PAUSE_VARIANT=f3_esc
export RSG__PATHS__CLIENT_JAR_PATH='/Users/AmilAgrawal/Library/Application Support/minecraft/versions/1.16.1/1.16.1.jar'
cd '/Users/AmilAgrawal/Library/Application Support/Claude/scratch-workspaces/d9080dc0-6400-4a71-ba8b-e896651c820d/d48e81fa-2e2e-421b-9196-f7a0199ec441/scratch-2026-10-02-00aea5/rsg-agent'
echo $$ > '/Users/AmilAgrawal/Library/Application Support/Claude/scratch-workspaces/d9080dc0-6400-4a71-ba8b-e896651c820d/d48e81fa-2e2e-421b-9196-f7a0199ec441/scratch-2026-11-09-4800c6/runs/bench/video/mc/jobs/20261115211514036/pid'
'/Users/AmilAgrawal/Library/Application Support/Claude/scratch-workspaces/d9080dc0-6400-4a71-ba8b-e896651c820d/d48e81fa-2e2e-421b-9196-f7a0199ec441/scratch-2026-11-09-4800c6/runs/bench/video/mc/WindowRecorder' 58506 52 '/Users/AmilAgrawal/Library/Application Support/Claude/scratch-workspaces/d9080dc0-6400-4a71-ba8b-e896651c820d/d48e81fa-2e2e-421b-9196-f7a0199ec441/scratch-2026-11-09-4800c6/runs/bench/video/mc/take_glass_raw.mp4' 60 > '/Users/AmilAgrawal/Library/Application Support/Claude/scratch-workspaces/d9080dc0-6400-4a71-ba8b-e896651c820d/d48e81fa-2e2e-421b-9196-f7a0199ec441/scratch-2026-11-09-4800c6/runs/bench/video/mc/jobs/20261115211514036/stdout' 2> '/Users/AmilAgrawal/Library/Application Support/Claude/scratch-workspaces/d9080dc0-6400-4a71-ba8b-e896651c820d/d48e81fa-2e2e-421b-9196-f7a0199ec441/scratch-2026-11-09-4800c6/runs/bench/video/mc/jobs/20261115211514036/stderr'
rc=$?
echo $rc > '/Users/AmilAgrawal/Library/Application Support/Claude/scratch-workspaces/d9080dc0-6400-4a71-ba8b-e896651c820d/d48e81fa-2e2e-421b-9196-f7a0199ec441/scratch-2026-11-09-4800c6/runs/bench/video/mc/jobs/20261115211514036/rc.tmp' && mv '/Users/AmilAgrawal/Library/Application Support/Claude/scratch-workspaces/d9080dc0-6400-4a71-ba8b-e896651c820d/d48e81fa-2e2e-421b-9196-f7a0199ec441/scratch-2026-11-09-4800c6/runs/bench/video/mc/jobs/20261115211514036/rc.tmp' '/Users/AmilAgrawal/Library/Application Support/Claude/scratch-workspaces/d9080dc0-6400-4a71-ba8b-e896651c820d/d48e81fa-2e2e-421b-9196-f7a0199ec441/scratch-2026-11-09-4800c6/runs/bench/video/mc/jobs/20261115211514036/rc'
(sleep 0.3; osascript -e 'tell application "Terminal" to close (every window whose name contains "job_20261115211514036")') >/dev/null 2>&1 &!
exit 0
