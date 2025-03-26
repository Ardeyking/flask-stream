from flask import Flask, Response, request
import time

app = Flask(__name__)
latest_frame = None

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
            if latest_frame:
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + latest_frame + b'\r\n')
            else:
                # Wait briefly to prevent tight loop and keep Gunicorn happy
                time.sleep(0.1)
    return Response(generate(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/')
def home():
    return "<h2>Livestream</h2><img src='/video_feed' width='640'>"
