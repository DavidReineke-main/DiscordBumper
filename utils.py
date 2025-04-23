import pyautogui
import mss
from PIL import Image
import pytesseract

# Konfiguration der Bildschirmbereiche
RECT_FARM_BUTTON = {"x1": 450, "y1": 915, "width": 67, "height": 35}
RECT_VERIFY = {"x1": 450, "y1": 820, "width": 370, "height": 100}
RECT_COMMAND = {"x1": 440, "y1": 900, "width": 370, "height": 80}
RECT_CHATBAR = {"x1": 470, "y1": 995, "width": 100, "height": 30}
RECT_DISCARD = {"x1": 710, "y1": 952, "width": 60, "height": 10}
RECT_BACK = {"x1": 520, "y1": 915, "width": 67, "height": 35}
RECT_DAILY = {"x1": 550, "y1":880, "width": 67, "height": 35}
RECT_GREENHOUSE = {"x1": 450, "y1": 845, "width": 67, "height": 35}
RECT_EMPTY_GREENHOUSE = {"x1": 480, "y1": 880, "width": 67, "height": 35}
RECT_VERIFY_CODE = {"x1": 765, "y1": 875, "width": 50, "height": 35}
RECT_MENU = {"x1": 700, "y1": 915, "width": 50, "height": 35}

pytesseract.pytesseract.tesseract_cmd = "/usr/bin/tesseract"

def click_action(rect):
    x = rect["x1"] + rect["width"] // 2
    y = rect["y1"] + rect["height"] // 2
    pyautogui.click(x, y)

def capture_and_recognize_text():
    with mss.mss() as sct:
        monitor = {"top": RECT_VERIFY["y1"], "left": RECT_VERIFY["x1"], "width": RECT_VERIFY["width"], "height": RECT_VERIFY["height"]}
        screenshot = sct.grab(monitor)
        img = Image.frombytes("RGB", (screenshot.width, screenshot.height), screenshot.rgb)
        return pytesseract.image_to_string(img).strip()

def capture_and_recognize_textCommand():
    with mss.mss() as sct:
        monitor = {"top": RECT_COMMAND["y1"], "left": RECT_COMMAND["x1"], "width": RECT_COMMAND["width"], "height": RECT_COMMAND["height"]}
        screenshot = sct.grab(monitor)
        img = Image.frombytes("RGB", (screenshot.width, screenshot.height), screenshot.rgb)
        return pytesseract.image_to_string(img).strip()
