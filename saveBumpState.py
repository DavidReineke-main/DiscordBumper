import os
import json
from datetime import datetime


STATE_FILE = "/root/DiscordBumper/state/bump_state.json"

def save_last_bump_time(dt: datetime):
    os.makedirs(os.path.dirname(STATE_FILE), exist_ok=True)
    with open(STATE_FILE, "w") as f:
        json.dump({"last_bump": dt.isoformat()}, f)

def load_last_bump_time():
    if not os.path.exists(STATE_FILE):
        return None
    with open(STATE_FILE, "r") as f:
        try:
            data = json.load(f)
            return datetime.fromisoformat(data["last_bump"])
        except Exception:
            return None
