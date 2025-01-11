import time
import random
import pyautogui
from datetime import datetime, timedelta


def bump_action(execution_count):
    print(f"Execution {execution_count}: Typing '/bump' and pressing Enter...")
    for char in "/bump":
        pyautogui.typewrite(char)
        time.sleep(random.uniform(0.1, 0.5))
    pyautogui.press("enter")
    time.sleep(random.uniform(0.1, 0.5))
    pyautogui.press("enter")


execution_count = 0


time.sleep(5)

while True:

    bump_action(execution_count)
    execution_count = execution_count + 1


    wait_time = 2 * 60 * 60 + random.randint(0, 30)
    next_execution_time = datetime.now() + timedelta(seconds=wait_time)
    print(f"Waiting {wait_time} seconds until the next execution... Next execution at {next_execution_time.strftime('%Y-%m-%d %H:%M:%S')}")
    time.sleep(wait_time)


