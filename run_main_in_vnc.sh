#!/bin/bash
export DISPLAY=:99
export XDG_RUNTIME_DIR=/tmp/runtime-root

# Vorherige Instanz killen (optional: sleep dazwischen)
pkill -f "DiscordBumper/main.py"
sleep 1

# Starte Script
python3 /root/DiscordBumper/main.py
