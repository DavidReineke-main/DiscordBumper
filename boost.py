import time
from datetime import datetime
import config

from screenutil import focus_chromium_window, switch_to_tab
from utils import click_action, RECT_BACK_BOOST, RECT_BOOST1, RECT_BOOST, RECT_BOOST2, RECT_BOOST3


def boost():
    focus_chromium_window()
    switch_to_tab(5)
    click_action(RECT_BOOST)
    time.sleep(2)

    click_action(RECT_BOOST1)
    time.sleep(2)
    click_action(RECT_BOOST2)
    time.sleep(2)
    click_action(RECT_BOOST3)
    time.sleep(2)
    click_action(RECT_BACK_BOOST)
    time.sleep(2)

    config.LASTBOOST = datetime.now()
    config.FARMTIME = 1.0
    return

