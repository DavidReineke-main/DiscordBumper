import time
from datetime import datetime, timedelta
import random
import config

from handleVerification import handle_verification_code
from logger import log
from screenutil import switch_to_tab
from utils import capture_and_recognize_text, click_action, RECT_FARM_BUTTON


def farm():
    """Führt eine Farming-Runde aus. Gibt True zurück bei Erfolg, False bei Verify-Fail."""

    now = datetime.now()

    switch_to_tab(2)

    log(f"[INFO] Current Farmtime: {config.FARMTIME}s")
    click_action(RECT_FARM_BUTTON)

    # Zeitberechnung und Planung
    execution_time = (datetime.now() - now).total_seconds()
    remaining_time = max(config.FARMTIME - execution_time, 0) + random.uniform(0.1, 0.15)
    config.NEXT_FARMTIME = datetime.now() + timedelta(seconds=remaining_time)

    log(f"[INFO] NEXT_FARMTIME in {remaining_time:.2f} seconds at {config.NEXT_FARMTIME.strftime('%H:%M:%S')}")
    time.sleep(remaining_time)
    return True
