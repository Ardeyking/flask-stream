from flask import Flask, Response, request, render_template
import time

app = Flask(__name__)
latest_frame = b''  # Stores the most recent uploaded JPEG

@app.route('/')
def home():
    return render_template('index.html')  # Page with <img src="/video_feed">

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
            # If no frame yet, send a tiny blank JPEG
            frame = latest_frame if latest_frame else b'\xff\xd8\xff\xd9'

            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

            time.sleep(0.05)  # ~20 FPS

    return Response(generate(), mimetype='multipart/x-mixed-replace; boundary=frame')
