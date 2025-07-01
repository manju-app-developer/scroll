from flask import Flask, render_template, jsonify
from flask_cors import CORS
import gesture_scroll

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    gesture_scroll.start_loop()
    return render_template('index.html')

@app.route('/toggle', methods=['POST'])
def toggle():
    state = gesture_scroll.toggle_enabled()
    return jsonify({'enabled': state})

@app.route('/status', methods=['GET'])
def status():
    return jsonify({'enabled': gesture_scroll.enabled})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
