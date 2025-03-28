import cv2
import mss
import numpy as np
from utils import RECT_FARM_BUTTON, RECT_VERIFY, RECT_CHATBAR, RECT_DISCARD

def draw_rectangles_on_screenshot(output_path="debug_ui_overlay.png"):
    with mss.mss() as sct:
        screenshot = sct.grab(sct.monitors[0])  # Ganzer Bildschirm
        img = np.array(screenshot)
        img_bgr = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)

    rectangles = [
        (RECT_FARM_BUTTON, (0, 0, 255)),    # Rot
        (RECT_VERIFY, (0, 255, 0)),         # Grün
        (RECT_CHATBAR, (255, 0, 0)),        # Blau
        (RECT_DISCARD, (100, 100, 0))        # Blau
    ]

    for rect, color in rectangles:
        top_left = (rect["x1"], rect["y1"])
        bottom_right = (rect["x1"] + rect["width"], rect["y1"] + rect["height"])
        cv2.rectangle(img_bgr, top_left, bottom_right, color, 3)

    cv2.imwrite(output_path, img_bgr)
    print(f"[DEBUG] Screenshot mit Rectangles gespeichert unter: {output_path}")


if __name__ == "__main__":
    draw_rectangles_on_screenshot()
