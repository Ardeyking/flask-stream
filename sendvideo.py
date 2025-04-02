import subprocess
import requests
import time
import os

RENDER_URL = "https://flask-stream-oo4j.onrender.com"

while True:
    try:
        # Delete the old frame to force a fresh capture
        if os.path.exists("frame.jpg"):
            os.remove("frame.jpg")
        print("Looping... Capturing new frame")
        # Capture a new frame
        result = subprocess.run([
            "libcamera-jpeg",
            "-o", "frame.jpg",
            "--width", "640",
            "--height", "480",
            "--nopreview",
            "-t", "1"
        ], capture_output=True, text=True)

        if result.returncode != 0:
            print("Capture failed:", result.stderr)
            time.sleep(1)
            continue

        time.sleep(0.1)  # Give camera time to reset before upload

        # Upload frame
        with open("frame.jpg", "rb") as f:
            res = requests.post(RENDER_URL, data=f.read(), timeout=5)
            print("Frame sent:", res.status_code)

        time.sleep(0.3)  # ~3 FPS for stability

    except Exception as e:
        print("Error:", e)
        time.sleep(1)
