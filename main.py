import threading
import time
import random
import os
from datetime import datetime, timedelta
import pyautogui
import config
import pyperclip

from boost import boost
from daily import daily
from greenhouse import greenhouse
from handleVerification import handle_verification_code
from saveBumpState import load_last_bump_time
from saveSettingState import load_setting_state, save_setting_state
from bump import bump_action
from farm import farm
from keyBoardListenener import control_loop
from logger import log
from ui import draw_rectangles_on_screenshot
from screenutil import switch_to_tab, focus_chromium_window
from utils import click_action, RECT_GREENHOUSE, RECT_EMPTY_GREENHOUSE, RECT_BACK, RECT_DAILY, RECT_MENU, \
    capture_and_recognize_text, RECT_VERIFY, RECT_COMMAND, RECT_CHATBAR, capture_and_recognize_textCommand

# Setup
pyautogui.FAILSAFE = False
os.environ["DISPLAY"] = ":99"


#start_x, start_y = 765, 880
#end_x, end_y = 815, 880

#time.sleep(1)  # kleine Pause vor dem Start

# Maus bewegen und ziehen
#pyautogui.moveTo(start_x, start_y, duration=0.2)
#pyautogui.mouseDown()
#pyautogui.moveTo(end_x, end_y, duration=0.2)
#pyautogui.mouseUp()

#copied_text = pyperclip.paste()
#print("Kopierter Text:", copied_text)

# Kopieren
#time.sleep(0.1)
#pyautogui.hotkey("ctrl", "c")

BUMP_INTERVAL = 2 * 60 * 60  # 2 Stunden
execution_count = 0

# Initialwerte
config.FARMING = True
config.BUMPING = False
config.DAILY = True
config.GREENHOUSE = True
config.BOOSTING = True
config.FARMTIME = 2.0
config.VERIFICATION_STRIKES = 0
config.NEXT_FARMTIME = datetime.now()
config.NEXT_DAILY_RUN = datetime.now()
config.LAST_GREENHOUSE_RUN = datetime.now()
config.CURRENTTAB = 1
config.LASTVERIFY = datetime.now()
config.LASTBOOST = datetime.now()
config.STOPPED = False
duplicateText = 0
textBuffer = ''
farming = 0


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

# ----- MAIN LOOP -----
log("[INFO] Starte Hauptloop...")
while True:
    now = datetime.now()

    # ----- BUMP -----
    #if config.BUMPING and now >= next_bump:
    #    bump_action(execution_count)
    #    next_bump = now + timedelta(seconds=(BUMP_INTERVAL + random.randint(0, 30)))
    #    log(f"[BUMP] Next bump at {next_bump.strftime('%H:%M:%S')}")

    #elif 0 <= (next_bump - now).total_seconds() <= 10:
    #    log(f"[BUMP] Skipping actions, bump in {int((next_bump - now).total_seconds())}s")
    #    time.sleep(1)
    #    continue

    commandText = capture_and_recognize_textCommand()
    if handle_verification_code(commandText) is False:
        continue

    if config.STOPPED:
        time.sleep(2)
        continue

    gameText = capture_and_recognize_text()

    if gameText == textBuffer:
        duplicateText += 1
        log('Got the same text ' + str(duplicateText) + ' times', True)
        if duplicateText >= 10:
            log('MULTIPLE DUPLICATE TEXT DETECTED 10 TIMES IN A ROW, RESTARTING FARMING', True)

            click_action(RECT_CHATBAR)
            for char in "/play":
                pyautogui.typewrite(char)
                time.sleep(random.uniform(0.1, 0.5))

            pyautogui.press("enter")
            pyautogui.press("enter")
            duplicateText = 0

    textBuffer = gameText


    if config.BOOSTING and now >= config.LASTBOOST + timedelta(minutes=15 + random.uniform(0.5, 5)):
        boost()

    if handle_verification_code(gameText) is False:
        log("[ERROR] Verification fehlgeschlagen – beende FARMING-Zyklus", True)
        click_action(RECT_CHATBAR)

        pyautogui.typewrite('@')
        time.sleep(1)
        pyautogui.typewrite('@D')
        time.sleep(1)
        pyautogui.press("enter")
        time.sleep(1)

        for char in "Stopped Execution due to Failed Verification":
            pyautogui.typewrite(char)
            time.sleep(random.uniform(0.1, 0.5))

        pyautogui.press("enter")

        config.STOPPED = True
        save_setting_state()

    # ----- FARMING -----
    if config.FARMING and now >= config.NEXT_FARMTIME:
        farm()
        farming += 1
        if farming >= 20:
            config.FARMTIME = 1.0

    # ----- DAILY -----
    if config.DAILY and now >= config.NEXT_DAILY_RUN:
        if (now - config.LASTVERIFY) <= timedelta(seconds=60):
            log("[DAILY] Running DailyRewards", True)
            daily()
        else:
            log("[DAILY] Waiting for recent verification")

    # ----- GREENHOUSE -----
    if config.GREENHOUSE and now >= (config.LAST_GREENHOUSE_RUN + timedelta(minutes=39 + random.uniform(0.5, 3))):
        log("[GREENHOUSE] Running Greenhouse", True)
        greenhouse()

    time.sleep(0.1)
