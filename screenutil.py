import os
import time
import config
from logger import log
from saveSettingState import save_setting_state

def focus_chromium_window():
    """
    Aktiviert das Chromium-Discord-Fenster anhand der Fensterklasse.
    """
    try:
        result = os.system("xdotool search --onlyvisible --class chromium windowactivate")
        if result != 0:
            log("[WARN] Discord-Fenster (Chromium) nicht gefunden.", True)
        else:
            log("[INFO] Fokus auf Discord (Chromium) gesetzt.", True)
    except Exception as e:
        log(f"[ERROR] Fehler beim Setzen des Fokus auf Chromium: {e}", True)

def switch_to_tab(tab_index):
    """
    Wechselt auf einen Tab im aktiven Chromium-Fenster via Tastenkombination.
    """
    try:
        if config.CURRENTTAB == tab_index:
            return

        focus_chromium_window()
        time.sleep(0.1)

        if 1 <= tab_index <= 8:
            result = os.system(f"xdotool key ctrl+{tab_index}")
            if result != 0:
                log(f"[ERROR] Fehler beim Tabwechsel zu Tab {tab_index} via xdotool.", True)
            else:
                log(f"[INFO] Tabwechsel: Chromium → Tab {tab_index}", True)
                config.CURRENTTAB = tab_index
                save_setting_state()
                time.sleep(0.3)
        else:
            log(f"[WARN] Ungültiger Tab-Index: {tab_index}", True)

    except Exception as e:
        log(f"[ERROR] Fehler beim Wechseln des Tabs: {e}", True)
