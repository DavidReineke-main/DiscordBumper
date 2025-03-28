import pyautogui
import mss
from PIL import Image
import pytesseract

# Konfiguration der Bildschirmbereiche
RECT_FARM_BUTTON = {"x1": 1458, "y1": 948, "width": 67, "height": 35}
RECT_VERIFY = {"x1": 1458, "y1": 840, "width": 370, "height": 100}
RECT_CHATBAR = {"x1": 1470, "y1": 1010, "width": 100, "height": 30}

pytesseract.pytesseract.tesseract_cmd = "/usr/bin/tesseract"

def click_action():
    x = RECT_FARM_BUTTON["x1"] + RECT_FARM_BUTTON["width"] // 2
    y = RECT_FARM_BUTTON["y1"] + RECT_FARM_BUTTON["height"] // 2
    pyautogui.click(x, y)

def click_chatbar_action():
    x = RECT_CHATBAR["x1"] + RECT_CHATBAR["width"] // 2
    y = RECT_CHATBAR["y1"] + RECT_CHATBAR["height"] // 2
    pyautogui.click(x, y)

def capture_and_recognize_text():
    with mss.mss() as sct:
        monitor = {"top": RECT_VERIFY["y1"], "left": RECT_VERIFY["x1"], "width": RECT_VERIFY["width"], "height": RECT_VERIFY["height"]}
        screenshot = sct.grab(monitor)
        img = Image.frombytes("RGB", (screenshot.width, screenshot.height), screenshot.rgb)
        return pytesseract.image_to_string(img).strip()
