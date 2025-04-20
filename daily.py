import time
from datetime import datetime, timedelta

import config

from logger import log
from screenutil import focus_chromium_window, switch_to_tab
from utils import click_action, RECT_BACK, RECT_DAILY


def daily():
    log("[DAILY] Claiming daily reward...")
    focus_chromium_window()
    switch_to_tab(3)
    time.sleep(1)
    click_action(RECT_DAILY)
    time.sleep(2)
    click_action(RECT_BACK)
    config.NEXT_DAILY_RUN = datetime.now() + timedelta(days=1)