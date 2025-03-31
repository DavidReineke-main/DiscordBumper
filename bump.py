from datetime import datetime
import random
import time

import pyautogui

from logger import log
from saveBumpState import save_last_bump_time
from screenutil import focus_chromium_window, switch_to_tab


def bump_action(execution_count):
    log(f"Execution {execution_count}: Typing '/bump' and pressing Enter...")

    focus_chromium_window()
    switch_to_tab(1)
    pyautogui.typewrite("/")
    for char in "bump":
        pyautogui.typewrite(char)
        time.sleep(random.uniform(0.1, 0.5))
    pyautogui.press("enter")
    time.sleep(random.uniform(0.1, 0.5))
    pyautogui.press("enter")

    save_last_bump_time(datetime.now())
    log("[INFO] Letzter Bump gespeichert.")
