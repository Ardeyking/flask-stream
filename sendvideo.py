import subprocess
import requests
import time
import os

# Replace with your actual Render livestream endpoint
RENDER_URL = "https://your-app-name.onrender.com/upload_frame"

while True:
    try:
        # Remove old frame if it exists
        if os.path.exists("frame.jpg"):
            os.remove("frame.jpg")

        # Capture JPEG using libcamera
        subprocess.run([
            "libcamera-jpeg",
            "-o", "frame.jpg",
            "--width", "640",
            "--height", "480",
            "--nopreview",
            "-t", "1"
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

        # Upload the frame to Render
        with open("frame.jpg", "rb") as f:
            res = requests.post(RENDER_URL, data=f.read(), timeout=5)
            print("Sent:", res.status_code)

        # Wait a bit before sending the next frame
        time.sleep(0.2)  # ~5 FPS

    except Exception as e:
        print("Error sending frame:", e)
        time.sleep(1)
