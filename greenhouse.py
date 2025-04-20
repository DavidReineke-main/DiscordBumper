from datetime import datetime, timedelta
import time

import config

from logger import log
from screenutil import focus_chromium_window, switch_to_tab
from utils import click_action, RECT_EMPTY_GREENHOUSE, RECT_GREENHOUSE, RECT_BACK


def greenhouse():
    log("[GREENHOUSE] Starting greenhouse action")
    focus_chromium_window()
    switch_to_tab(4)
    time.sleep(1)
    click_action(RECT_GREENHOUSE)
    time.sleep(2)
    click_action(RECT_EMPTY_GREENHOUSE)
    time.sleep(2)
    click_action(RECT_BACK)
    config.NEXT_GREENHOUSE_RUN = datetime.now() + timedelta(minutes=30)
    log(f"[GREENHOUSE] Next run at {config.NEXT_GREENHOUSE_RUN.strftime('%H:%M:%S')}")