from datetime import datetime, timezone, timedelta

LOGFILE_PATH = "/root/DiscordBumper/bot.log"  # Passe den Pfad ggf. an
LOG_TIMEZONE = timezone(timedelta(hours=1))   # GMT+1

def log(message, *, to_console=True):
    now = datetime.now(LOG_TIMEZONE).strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{now}] {message}"

    # Log in Datei schreiben
    with open(LOGFILE_PATH, "a") as logfile:
        logfile.write(line + "\n")

    # Optional auch ausgeben
    if to_console:
        print(line)