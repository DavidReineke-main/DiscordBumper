import os
import json
import config

from logger import log

STATE_FILE = "/root/DiscordBumper/state/settings_state.json"

def save_setting_state(FARMING, BUMPING):
    os.makedirs(os.path.dirname(STATE_FILE), exist_ok=True)
    with open(STATE_FILE, "w") as f:
        json.dump({"FARMING": FARMING, "BUMPING": BUMPING}, f)

def load_setting_state():

    log('Loading settings File', True)
    if not os.path.exists(STATE_FILE):
        log('No Settings File found', True)
        return None
    with open(STATE_FILE, "r") as f:
        try:
            log('Found Settings file, assigning')
            data = json.load(f)
            config.FARMING = data["FARMING"]
            config.BUMPING = data["BUMPING"]
            return None
        except Exception as e:
            log(e, True)
            return None
