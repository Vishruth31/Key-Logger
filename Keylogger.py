import sys
import os
import time
import random
import string
import socket
import requests
from pynput import keyboard, mouse

# ------------------ CONSENT ------------------
print("This program collects user activity for educational/demo purposes.")
print("It logs keyboard and mouse events locally.")
consent = input("Do you consent to this? (yes/no): ").strip().lower()

if consent != "yes":
    print("Consent not given. Exiting program.")
    sys.exit()

# ------------------ GLOBALS ------------------
t = ""
start_time = time.time()
interval = 60

key_count = 0
mouse_count = 0

device_name = socket.gethostname()
pics_names = []

log_file = "Logfile.txt"

# ------------------ FILE SETUP ------------------
if not os.path.exists(log_file):
    open(log_file, "w").close()

# ------------------ SCREENSHOT ------------------
def ScreenShot():
    global pics_names
    try:
        import pyautogui
        name = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(7))
        filename = name + ".png"
        pyautogui.screenshot().save(filename)
        pics_names.append(filename)
        print(f"[INFO] Screenshot saved: {filename}")
    except Exception as e:
        print("[ERROR] Screenshot failed:", e)

# ------------------ SAVE LOG ------------------
def save_log(data):
    with open(log_file, "a") as f:
        f.write(data)

# ------------------ SEND DATA ------------------
def send_data():
    global key_count, mouse_count, start_time

    # ❗ Skip sending empty data
    if key_count == 0 and mouse_count == 0:
        start_time = time.time()
        return

    data = {
        "device": device_name,
        "keys": key_count,
        "clicks": mouse_count,
        "timestamp": time.ctime()
    }

    try:
        response = requests.post(
            "http://127.0.0.1:5000/api/log",
            json=data,
            timeout=5
        )
        print("🔥 Sent:", data, "| Status:", response.status_code)
    except Exception as e:
        print("[ERROR] Failed to send:", e)

    # reset counters AFTER sending
    key_count = 0
    mouse_count = 0
    start_time = time.time()

# ------------------ KEYBOARD EVENT ------------------
def on_press(key):
    global t, key_count

    key_count += 1

    try:
        data = f"\n[{time.ctime()}] Key: {key.char}"
    except AttributeError:
        data = f"\n[{time.ctime()}] Key: {key}"

    t += data

    if len(t) > 300:
        ScreenShot()

    if len(t) > 500:
        save_log(t)
        t = ""

# ------------------ MOUSE EVENT ------------------
def on_click(x, y, button, pressed):
    global t, mouse_count

    if pressed:
        mouse_count += 1
        data = f"\n[{time.ctime()}] Mouse: {button} at ({x},{y})"
        t += data

        if len(t) > 500:
            save_log(t)
            t = ""

# ------------------ START ------------------
print(f"✅ Logging started on device: {device_name}")
print("⏳ Sending data every 60 seconds... Press Ctrl+C to stop.\n")

keyboard_listener = keyboard.Listener(on_press=on_press)
mouse_listener = mouse.Listener(on_click=on_click)

keyboard_listener.start()
mouse_listener.start()

# ------------------ MAIN LOOP ------------------
try:
    while True:
        time.sleep(1)

        current_time = time.time()

        # ✅ Correct timing logic
        if current_time - start_time >= interval:
            send_data()

except KeyboardInterrupt:
    print("\n🛑 Stopping logging...")
    keyboard_listener.stop()
    mouse_listener.stop()