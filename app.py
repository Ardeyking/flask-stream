from flask import Flask, Response, request, render_template
import time

app = Flask(__name__)
latest_frame = b''  # Stores the most recent uploaded frame

@app.route('/')
def home():
    return render_template('index.html')  # This should load your live viewer page

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
            time.sleep(0.05)  # Stream at ~20 FPS max

    return Response(generate(), mimetype='multipart/x-mixed-replace; boundary=frame')
