import os
import time

from logger import log


def focus_chromium_window():
    """
    Aktiviert das Chromium-Discord-Fenster anhand der Fensterklasse.
    """
    result = os.system("xdotool search --onlyvisible --class chromium windowactivate")
    if result != 0:
        log("[WARN] Discord-Fenster (Chromium) nicht gefunden.")
    else:
        log("[INFO] Fokus auf Discord (Chromium) gesetzt.")


def switch_to_tab(tab_index):
    focus_chromium_window()
    time.sleep(0.1)
    if 1 <= tab_index <= 8:
        os.system(f"xdotool key ctrl+{tab_index}")
        log(f"[INFO] Tabwechsel: Chromium → Tab {tab_index}")
        time.sleep(0.3)
    else:
        log(f"[WARN] Ungültiger Tab-Index: {tab_index}")