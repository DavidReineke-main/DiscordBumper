
from logger import log
import config

from saveSettingState import save_setting_state


def control_loop():
    while True:
        try:
            cmd = input("[INPUT] Befehl eingeben (f = Farming umschalten, b = Bumping umschalten, q = Beenden): ").strip().lower()
            if cmd == "f":
                config.FARMING = not config.FARMING
                config.DAILY = not config.DAILY
                config.GREENHOUSE = not config.GREENHOUSE
                config.BOOSTING = not config.BOOSTING
                state = "aktiviert" if config.FARMING else "deaktiviert"
                save_setting_state()
                log(f"[TOGGLE] FARMING wurde {state}")
            elif cmd == "b":
                config.BUMPING = not config.BUMPING
                state = "aktiviert" if config.BUMPING else "deaktiviert"
                log(f"[TOGGLE] BUMPING wurde {state}")
                save_setting_state()
            elif cmd == "q":
                save_setting_state()
                log("[EXIT] Beende Script...")
                exit(0)
        except Exception as e:
            log(f"[ERROR] Input-Fehler: {e}")