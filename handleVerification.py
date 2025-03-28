import time
import random

import config
import pyautogui
from logger import log
from utils import click_chatbar_action, click_action, RECT_DISCARD


def handle_verification_code(text):
    """Prüft den Text auf Verifizierungscodes und gibt sie ein."""

    if "Antibot Verification" in text and "Use /verify" in text:
        log("[INFO] Verification text detected!")
        config.VERIFICATION_STRIKES += 1
        log(f"[SECURITY] Verification strikes: {config.VERIFICATION_STRIKES}")

        if config.VERIFICATION_STRIKES >= 3:
            config.FARMING = False
            log("[SECURITY] Deaktiviere FARMING wegen 3x Verifizierung")

        try:
            code = text.split("code to continue playing:")[1].split(".")[0].strip()
            click_chatbar_action()
            time.sleep(random.uniform(0.1, 0.5))

            for char in "/verify " + code:
                pyautogui.typewrite(char)
                time.sleep(random.uniform(0.1, 0.5))

            pyautogui.press("enter")
            pyautogui.press("enter")

            time.sleep(2)
            click_action(RECT_DISCARD)
            log(f"[INFO] Entered verification code: /verify {code}")

        except IndexError:
            log("[ERROR] Failed to extract verification code")

    elif "You must wait" in text:
        new_time = float(text.split(":")[1].split(" ")[1].strip())
        log(f"[INFO] Adjusted FARMTIME to {new_time}s")
        config.FARMTIME = new_time

        # Kein Verifizierungsfehler → Strike reset
        config.VERIFICATION_STRIKES = 0

    else:
        # Kein Verifizierungstext → Strike reset
        config.VERIFICATION_STRIKES = 0
