import threading
import time
import random
import os
from datetime import datetime, timedelta
import pyautogui
import config

from daily import daily
from greenhouse import greenhouse
from saveBumpState import load_last_bump_time
from saveSettingState import load_setting_state, save_setting_state
from bump import bump_action
from farm import farm
from keyBoardListenener import control_loop
from logger import log
from ui import draw_rectangles_on_screenshot
from screenutil import switch_to_tab, focus_chromium_window
from utils import click_action, RECT_GREENHOUSE, RECT_EMPTY_GREENHOUSE, RECT_BACK, RECT_DAILY

# Setup
pyautogui.FAILSAFE = False
os.environ["DISPLAY"] = ":99"

BUMP_INTERVAL = 2 * 60 * 60  # 2 Stunden
execution_count = 0

# Initialwerte
config.FARMING = True
config.BUMPING = True
config.DAILY = True
config.GREENHOUSE = True
config.FARMTIME = 2.0
config.VERIFICATION_STRIKES = 0
config.NEXT_FARMTIME = datetime.now()
config.NEXT_DAILY_RUN = datetime.now()
config.NEXT_GREENHOUSE_RUN = datetime.now()
config.CURRENTTAB = 1
config.LASTVERIFY = datetime.now()

# Lade gespeicherte Zustände
draw_rectangles_on_screenshot()
load_setting_state()
log(f'FARMING set to {config.FARMING}')
log(f'BUMPING set to {config.BUMPING}')
log(f'DAILY set to {config.DAILY}')
log(f'GREENHOUSE set to {config.GREENHOUSE}')
log(f'LASTVERIFY: {config.LASTVERIFY.strftime("%H:%M:%S")}')

switch_to_tab(config.CURRENTTAB, True)

# Bump Initialisierung
log("[INFO] Lade letzte Bump-Zeit...")
last_bump = load_last_bump_time()
if last_bump is None:
    next_bump = datetime.now() + timedelta(seconds=10)
else:
    elapsed = (datetime.now() - last_bump).total_seconds()
    if elapsed >= BUMP_INTERVAL:
        next_bump = datetime.now()
    else:
        next_bump = datetime.now() + timedelta(seconds=(BUMP_INTERVAL - elapsed))

# Keyboard Listener starten
thread = threading.Thread(target=control_loop, daemon=True)
thread.start()
log("[INFO] Startup pause – 5 Sekunden")
time.sleep(0)

# ----- MAIN LOOP -----
log("[INFO] Starte Hauptloop...")
while True:
    now = datetime.now()

    # ----- BUMP -----
    if config.BUMPING and now >= next_bump:
        bump_action(execution_count)
        next_bump = now + timedelta(seconds=(BUMP_INTERVAL + random.randint(0, 30)))
        log(f"[BUMP] Next bump at {next_bump.strftime('%H:%M:%S')}")

    elif 0 <= (next_bump - now).total_seconds() <= 10:
        log(f"[BUMP] Skipping actions, bump in {int((next_bump - now).total_seconds())}s")
        time.sleep(1)
        continue

    # ----- FARMING -----
    if config.FARMING and now >= config.NEXT_FARMTIME:
        farm()

    # ----- DAILY -----
    if config.DAILY and now >= config.NEXT_DAILY_RUN:
        if (now - config.LASTVERIFY) <= timedelta(seconds=60):
            daily()
        else:
            log("[DAILY] Waiting for recent verification")

    # ----- GREENHOUSE -----
    if config.GREENHOUSE and now >= config.NEXT_GREENHOUSE_RUN:
        if (now - config.LASTVERIFY) <= timedelta(seconds=60):
            greenhouse()
        else:
            log("[GREENHOUSE] Skipped due to missing recent verification")

    time.sleep(1)
