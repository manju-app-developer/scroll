from flask import Flask, render_template, jsonify
from flask_cors import CORS
import gesture_scroll

app = Flask(__name__)
CORS(app)  # ✅ Enables CORS for all routes

@app.route('/')
def index():
    gesture_scroll.start_loop()  # Starts gesture detection thread if not already running
    return render_template('index.html', status=gesture_scroll.enabled)

@app.route('/toggle', methods=['POST'])
def toggle():
    state = gesture_scroll.toggle_enabled()
    print(f"Gesture control toggled → {'ON' if state else 'OFF'}")
    return jsonify({'enabled': state})

@app.route('/status', methods=['GET'])
def get_status():
    return jsonify({'enabled': gesture_scroll.enabled})

if __name__ == '__main__':
    print("🚀 Flask server running on http://127.0.0.1:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)
