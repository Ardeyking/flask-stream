from flask import Flask, Response, request
import time
import cv2
import numpy as np

app = Flask(__name__)
latest_frame = None

def generate_blank_frame():
    # Create a black 640x480 frame
    frame = np.zeros((480, 640, 3), dtype=np.uint8)
    _, jpeg = cv2.imencode('.jpg', frame)
    return jpeg.tobytes()

@app.route('/upload_frame', methods=['POST'])
def upload_frame():
    global latest_frame
    latest_frame = request.data
    return 'Frame received', 200

@app.route('/video_feed')
def video_feed():
    def generate():
        global latest_frame
        while True:
            frame = latest_frame if latest_frame else generate_blank_frame()

            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

            time.sleep(0.1)

    return Response(generate(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/')
def home():
    return "<h2>Livestream</h2><img src='/video_feed' width='640'>"
