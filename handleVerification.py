from datetime import datetime
import time
import random

import config
import pyautogui
from logger import log
from saveSettingState import save_setting_state
from utils import click_action, RECT_DISCARD, RECT_CHATBAR


def handle_verification_code(text):
    """Prüft den Text auf Verifizierungscodes und gibt sie ein. Gibt True bei Erfolg, False bei Fail."""

    if "Antibot Verification" in text and "Use /verify" in text:
        log("[INFO] Verification text detected!", True)
        config.VERIFICATION_STRIKES += 1
        log(f"[SECURITY] Verification strikes: {config.VERIFICATION_STRIKES}", True)

        if config.VERIFICATION_STRIKES >= 3:
            config.FARMING = False
            config.DAILY = False
            config.GREENHOUSE = False
            config.BOOSTING = False
            save_setting_state()
            log("[SECURITY] Deaktiviere alle Features wegen 3x Verify-Fail", True)
            return False  # <<< Abbrechen hier

        try:
            code = text.split("code to continue playing:")[1].split(".")[0].strip()
            click_action(RECT_CHATBAR)
            time.sleep(random.uniform(0.1, 0.5))

            for char in "/verify " + code:
                pyautogui.typewrite(char)
                time.sleep(random.uniform(0.1, 0.5))

            pyautogui.press("enter")
            pyautogui.press("enter")

            time.sleep(2)
            click_action(RECT_DISCARD)
            log(f"[INFO] Entered verification code: /verify {code}", True)

            for char in "/play":
                pyautogui.typewrite(char)
                time.sleep(random.uniform(0.1, 0.5))

            pyautogui.press("enter")
            pyautogui.press("enter")

            return True  # <<< Erfolg

        except IndexError:
            log("[ERROR] Failed to extract verification code")
            return

    elif "return" in text and config.STOPPED:

        log(f"[COMMAND] Resumed Execution by Command", True)
        config.STOPPED = False
        config.FARMING = True
        config.GREENHOUSE = True
        config.DAILY = True
        config.BOOSTING = True

        click_action(RECT_CHATBAR)
        for char in "/play":
            pyautogui.typewrite(char)
            time.sleep(random.uniform(0.1, 0.5))

        pyautogui.press("enter")
        pyautogui.press("enter")
        save_setting_state()
        time.sleep(3)
        return True

    elif "stop" in text and not config.STOPPED:

        log(f"[COMMAND] Stopped Execution by Command", True)
        config.STOPPED = True
        config.FARMING = False
        config.GREENHOUSE = False
        config.DAILY = False
        config.BOOSTING = False

        save_setting_state()
        return True

    elif "You must wait" in text:
        try:
            new_time = float(text.split(":")[1].split(" ")[1].strip())
            log(f"[INFO] Adjusted FARMTIME to {new_time}s")
            config.FARMTIME = new_time
            config.LASTVERIFY = datetime.now()
            config.VERIFICATION_STRIKES = 0
        except Exception as e:
            log(f"[ERROR] Could not parse wait time: {e}")
        return True



    return True

