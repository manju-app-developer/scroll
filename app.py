from flask import Flask, render_template, jsonify
import gesture_scroll

app = Flask(__name__)

@app.route('/')
def index():
    gesture_scroll.start_loop()  # Starts the gesture thread if not already running
    return render_template('index.html', status=gesture_scroll.enabled)

@app.route('/toggle', methods=['POST'])
def toggle():
    state = gesture_scroll.toggle_enabled()
    print(f"Gesture control toggled → {'ON' if state else 'OFF'}")
    return jsonify({'enabled': state})

if __name__ == '__main__':
    print("🚀 Flask server starting at http://127.0.0.1:5000")
    app.run(debug=True)
