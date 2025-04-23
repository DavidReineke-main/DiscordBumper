from datetime import datetime, timedelta
import time
import random

import config
import pyautogui

from logger import log
from screenutil import focus_chromium_window, switch_to_tab
from utils import click_action, RECT_EMPTY_GREENHOUSE, RECT_GREENHOUSE, RECT_BACK, RECT_FARM_BUTTON, RECT_MENU


def greenhouse():
    log("[GREENHOUSE] Starting greenhouse action")
    focus_chromium_window()
    switch_to_tab(4)

    for char in "/play":
        pyautogui.typewrite(char)
        time.sleep(random.uniform(0.1, 0.5))

    pyautogui.press("enter")
    pyautogui.press("enter")

    time.sleep(2)
    click_action(RECT_MENU)
    time.sleep(4)
    click_action(RECT_GREENHOUSE)
    time.sleep(4)
    click_action(RECT_EMPTY_GREENHOUSE)
    config.LAST_GREENHOUSE_RUN = datetime.now()
    log(f"[GREENHOUSE] Next run at {(config.LAST_GREENHOUSE_RUN + timedelta(minutes=39)).strftime('%H:%M:%S')}")