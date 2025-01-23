import time
import random
import pyautogui
import tkinter as tk
from PIL import Image
import pytesseract
import mss
import threading

# Configure Tesseract-OCR path (adjust for your installation)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Rectangle coordinates and sizes
RECT_FARM_BUTTON = {
    "x1": -518,  # Adjust these values as necessary
    "y1": 1245,
    "width": 67,
    "height": 35,
}

RECT_VERIFY = {
    "x1": -518,  # Adjust these values as necessary
    "y1": 1140,
    "width": 370,
    "height": 100,
}

RECT_CHATBAR = {
    "x1": -500,  # Adjust these values as necessary
    "y1": 1310,
    "width": 100,
    "height": 30,
}

RECT_DISCARD = {
    "x1": -310,  # Adjust these values as necessary
    "y1": 1262,
    "width": 120,
    "height": 15,
}

FARMTIME = 2.5

def draw_transparent_rectangles():
    root = tk.Tk()
    root.title("Transparent Rectangles")
    root.attributes("-topmost", True)
    root.overrideredirect(True)
    root.wm_attributes("-transparentcolor", "black")

    # Calculate window dimensions
    x_min = min(RECT_FARM_BUTTON["x1"], RECT_VERIFY["x1"], RECT_CHATBAR["x1"])
    y_min = min(RECT_FARM_BUTTON["y1"], RECT_VERIFY["y1"], RECT_CHATBAR["y1"])
    x_max = max(
        RECT_FARM_BUTTON["x1"] + RECT_FARM_BUTTON["width"],
        RECT_VERIFY["x1"] + RECT_VERIFY["width"],
        RECT_CHATBAR["x1"] + RECT_CHATBAR["width"],
    )
    y_max = max(
        RECT_FARM_BUTTON["y1"] + RECT_FARM_BUTTON["height"],
        RECT_VERIFY["y1"] + RECT_VERIFY["height"],
        RECT_CHATBAR["y1"] + RECT_CHATBAR["height"],
    )

    window_width = x_max - x_min
    window_height = y_max - y_min

    root.geometry(f"{window_width}x{window_height}+{x_min}+{y_min}")

    # Create canvas
    canvas = tk.Canvas(root, width=window_width, height=window_height, bg="black", highlightthickness=0)
    canvas.pack()

    # Draw the red rectangle (Farm Button)
    canvas.create_rectangle(
        RECT_FARM_BUTTON["x1"] - x_min,
        RECT_FARM_BUTTON["y1"] - y_min,
        RECT_FARM_BUTTON["x1"] - x_min + RECT_FARM_BUTTON["width"],
        RECT_FARM_BUTTON["y1"] - y_min + RECT_FARM_BUTTON["height"],
        outline="red",
        width=5,
    )

    # Draw the green rectangle (Verify)
    canvas.create_rectangle(
        RECT_VERIFY["x1"] - x_min,
        RECT_VERIFY["y1"] - y_min,
        RECT_VERIFY["x1"] - x_min + RECT_VERIFY["width"],
        RECT_VERIFY["y1"] - y_min + RECT_VERIFY["height"],
        outline="green",
        width=5,
    )

    # Draw the blue rectangle (Chatbar)
    canvas.create_rectangle(
        RECT_CHATBAR["x1"] - x_min,
        RECT_CHATBAR["y1"] - y_min,
        RECT_CHATBAR["x1"] - x_min + RECT_CHATBAR["width"],
        RECT_CHATBAR["y1"] - y_min + RECT_CHATBAR["height"],
        outline="blue",
        width=5,
    )

    # Draw the blue rectangle (Chatbar)
    canvas.create_rectangle(
        RECT_DISCARD["x1"] - x_min,
        RECT_DISCARD["y1"] - y_min,
        RECT_DISCARD["x1"] - x_min + RECT_DISCARD["width"],
        RECT_DISCARD["y1"] - y_min + RECT_DISCARD["height"],
        outline="yellow",
        width=5,
    )

    print("Transparent rectangles displayed. Close window with ALT+F4.")
    root.mainloop()

# Function: Click within the red rectangle (Farm Button)
def click_action():
    x = RECT_FARM_BUTTON["x1"] + RECT_FARM_BUTTON["width"] // 2
    y = RECT_FARM_BUTTON["y1"] + RECT_FARM_BUTTON["height"] // 2
    pyautogui.click(x, y)
    print(f"Clicked at ({x}, {y})")

# Function: Click within the red rectangle (Farm Button)
def click_chatbar_action():
    x = RECT_CHATBAR["x1"] + RECT_CHATBAR["width"] // 2
    y = RECT_CHATBAR["y1"] + RECT_CHATBAR["height"] // 2
    pyautogui.click(x, y)
    print(f"Clicked at ({x}, {y})")

# Function: Click within the red rectangle (Farm Button)
def click_discard_action():
    x = RECT_DISCARD["x1"] + RECT_DISCARD["width"] // 2
    y = RECT_DISCARD["y1"] + RECT_CHATBAR["height"] // 2
    pyautogui.click(x, y)
    print(f"Clicked at ({x}, {y})")

# Function: Capture the Verify rectangle using mss and recognize text
def capture_and_recognize_text():
    with mss.mss() as sct:
        monitor = {
            "top": RECT_VERIFY["y1"],
            "left": RECT_VERIFY["x1"],
            "width": RECT_VERIFY["width"],
            "height": RECT_VERIFY["height"],
        }
        screenshot = sct.grab(monitor)
        img = Image.frombytes("RGB", (screenshot.width, screenshot.height), screenshot.rgb)
        img.save("debug_verify_capture.png")  # Save the debug image for verification
        print("Saved debug screenshot: debug_verify_capture.png")
        text = pytesseract.image_to_string(img)
        print(text)
        return text.strip()

# Function: Handle verification code
def handle_verification_code(text):
    global FARMTIME
    print("Checking for verification text...")
    if "Antibot Verification" in text and "Use /verify" in text:
        print("Verification text detected!")
        try:
            # Extract the code (e.g., 3fY4)
            code = text.split("code to continue playing:")[1].split(".")[0].strip()
            click_chatbar_action()
            time.sleep(random.uniform(0.1, 0.5))
            pyautogui.press("enter")
            time.sleep(random.uniform(0.1, 0.5))
            for char in "/verify " +  code:
                pyautogui.typewrite(char)
                time.sleep(random.uniform(0.1, 0.5))
            pyautogui.press("enter")
            time.sleep(random.uniform(0.1, 0.5))
            pyautogui.press("enter")
            time.sleep(random.uniform(0.5, 1))
            click_chatbar_action()

            pyautogui.press("enter")
            for char in "/farm":
                pyautogui.typewrite(char)
                time.sleep(random.uniform(0.1, 0.5))
            pyautogui.press("enter")
            time.sleep(random.uniform(0.1, 0.5))
            pyautogui.press("enter")
            time.sleep(random.uniform(0.5, 1))
            print(f"Entered verification code: /verify {code}")
        except IndexError:
            print("Error extracting the code. Text:", text)
    elif "You must wait" in text:
        print("Detected Timing issue")
        newTime = text.split(":")[1].split(" ")[1].strip()
        print("NewTime: ", newTime)
        FARMTIME = float(newTime)

    else:
        print("No verification text detected.")

# Main Program

rectangle_thread = threading.Thread(target=draw_transparent_rectangles, daemon=True)
rectangle_thread.start()


while True:
    print("Current Farmtime: ", FARMTIME)
    click_action()

    # Starte die Zeitmessung
    start_time = time.time()

    # Capture and process verification text
    detected_text = capture_and_recognize_text()
    print("Detected Text:", detected_text)
    handle_verification_code(detected_text)

    # Ende der Zeitmessung
    execution_time = time.time() - start_time
    print(f"Execution time for detection and handling: {execution_time:.2f} seconds")

    # Berechne verbleibende Zeit bis zur nächsten Aktion
    remaining_time = max(FARMTIME - execution_time, 0) + random.uniform(0.08, 0.15)
    print(f"Remaining sleep time: {remaining_time:.2f} seconds")
    print('------------------------------------------------------')
    # Warte die verbleibende Zeit
    time.sleep(remaining_time)