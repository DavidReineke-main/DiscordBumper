import threading
import time
import random
import os
from datetime import datetime, timedelta
import pyautogui
import config

from bump import bump_action
from farm import farm
from keyBoardListenener import control_loop
from logger import log
from ui import draw_rectangles_on_screenshot


pyautogui.FAILSAFE = False
os.environ["DISPLAY"] = ":99"

execution_count = 0
BUMP_INTERVAL = 2 * 60 * 60  # alle 2 Stunden
next_bump = datetime.now() + timedelta(seconds=15)

config.FARMING = True
config.BUMPING = True


config.FARMTIME = 2.0
config.NEXT_FARMTIME = datetime.now()
config.VERIFICATION_STRIKES = 0

config.now = datetime.now()

# ----- Startup Pause -----
log("[INFO] Startup pause, waiting 5 Seconds to begin...")
time.sleep(5)

# ----- UI im separaten Thread starten -----
log("[INFO] Grabbing Debug Screenshot")
draw_rectangles_on_screenshot()

# ----- Listener Thread -----
log("[INFO] Starting Listener Thread")
listener_thread = threading.Thread(target=control_loop, daemon=True)
listener_thread.start()

# ----- Main Loop -----
log("[INFO] Starting Main Loop...")
time.sleep(2)


while True:
    config.now = datetime.now()

    #log(f'[DEBUG] START of execution')

    # ----- Bumping Logic -----
    if config.now >= next_bump and config.BUMPING:
        bump_action(execution_count)
        execution_count = execution_count + 1

        next_bump = config.now + timedelta(seconds=(BUMP_INTERVAL + random.randint(0, 30)))
        log(f"[INFO] Next Bump planned at {next_bump.strftime('%H:%M:%S')}")

    # ----- Security to do nothing else if the Bump is about to start or has started 10 seconds ago -----
    elif 0 <= (next_bump - config.now).total_seconds() <= 10:
        log(f'[DEBUG] SKIPPED execution: next Bump in {int((next_bump - config.now).total_seconds())}s')
        time.sleep(1)
        continue

    # ----- Farming Logic -----
    elif config.now >= config.NEXT_FARMTIME and config.FARMING:
        farm()

    #log(f'[DEBUG] END of execution')
    time.sleep(1)  # kleine Pause, damit CPU geschont wird