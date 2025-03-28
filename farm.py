from datetime import datetime, timedelta
import random
import config

from handleVerification import handle_verification_code
from logger import log
from screenutil import switch_to_tab, focus_chromium_window
from utils import capture_and_recognize_text, click_action, RECT_FARM_BUTTON


def farm():
    """Führt eine Farming-Runde aus."""

    switch_to_tab(2)

    log(f"[INFO] Current Farmtime: {config.FARMTIME}s")
    click_action(RECT_FARM_BUTTON)

    detected_text = capture_and_recognize_text()
    handle_verification_code(detected_text)

    # Wie lange hat der Vorgang gedauert?
    execution_time = (datetime.now() - config.now).total_seconds()

    # Restzeit berechnen
    remaining_time = max(config.FARMTIME - execution_time, 0) + random.uniform(0.1, 0.15)
    config.NEXT_FARMTIME = datetime.now() + timedelta(seconds=remaining_time)

    log(f"[INFO] NEXT_FARMTIME in {remaining_time:.2f} seconds at {config.NEXT_FARMTIME.strftime('%H:%M:%S')}")
