
from logger import log
import config

def control_loop():
    while True:
        try:
            cmd = input("[INPUT] Befehl eingeben (f = Farming umschalten, b = Bumping umschalten, q = Beenden): ").strip().lower()
            if cmd == "f":
                config.FARMING = not config.FARMING
                state = "aktiviert" if config.FARMING else "deaktiviert"
                log(f"[TOGGLE] FARMING wurde {state}")
            elif cmd == "b":
                config.BUMPING = not config.BUMPING
                state = "aktiviert" if config.BUMPING else "deaktiviert"
                log(f"[TOGGLE] BUMPING wurde {state}")
            elif cmd == "q":
                log("[EXIT] Beende Script...")
                exit(0)
        except Exception as e:
            log(f"[ERROR] Input-Fehler: {e}")