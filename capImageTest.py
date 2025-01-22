import mss
from PIL import Image

RECT_VERIFY = {
    "x1": -518,
    "y1": 1140,
    "width": 370,
    "height": 100,
}

def capture_with_mss():
    with mss.mss() as sct:
        monitor = {
            "top": RECT_VERIFY["y1"],
            "left": RECT_VERIFY["x1"],
            "width": RECT_VERIFY["width"],
            "height": RECT_VERIFY["height"],
        }
        screenshot = sct.grab(monitor)
        img = Image.frombytes("RGB", (screenshot.width, screenshot.height), screenshot.rgb)
        img.save("mss_capture.png")
        print("Saved MSS screenshot: mss_capture.png")
        return img

capture_with_mss()