from datetime import datetime
import os
import json
import config

from logger import log

STATE_FILE = "/root/DiscordBumper/state/settings_state.json"

def save_setting_state():
    os.makedirs(os.path.dirname(STATE_FILE), exist_ok=True)
    with open(STATE_FILE, "w") as f:
        json.dump({
            "FARMING": config.FARMING,
            "BUMPING": config.BUMPING,
            "CURRENTTAB": config.CURRENTTAB,
            "GREENHOUSE": config.GREENHOUSE,
            "NEXT_DAILY_RUN": config.NEXT_DAILY_RUN.isoformat(),
            "LAST_GREENHOUSE_RUN": config.LAST_GREENHOUSE_RUN.isoformat(),
            "LASTVERIFY": config.LASTVERIFY.isoformat(),
            "LASTBOOST": config.LASTBOOST.isoformat(),
            "DAILY": config.DAILY,
            "STOPPED": config.STOPPED,
            "BOOSTING": config.BOOSTING
        }, f)

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
            config.CURRENTTAB = data["CURRENTTAB"]
            config.GREENHOUSE = data["GREENHOUSE"]
            config.NEXT_DAILY_RUN = datetime.fromisoformat(data["NEXT_DAILY_RUN"])
            config.LAST_GREENHOUSE_RUN = datetime.fromisoformat(data["LAST_GREENHOUSE_RUN"])
            config.LASTVERIFY = datetime.fromisoformat(data["LASTVERIFY"])
            config.DAILY = data["DAILY"]
            config.STOPPED = data["STOPPED"]
            config.BOOSTING = data["BOOSTING"]
            config.LASTBOOST = datetime.fromisoformat(data["LASTBOOST"])

            return None
        except Exception as e:
            log(e, True)
            return None
