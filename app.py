from flask import Flask, render_template, request, redirect, jsonify
import json
import os

app = Flask(__name__)

# Path to store feedback
FEEDBACK_FILE = os.path.join('data', 'feedback.json')

# Load feedback from file
def load_feedback():
    if os.path.exists(FEEDBACK_FILE):
        with open(FEEDBACK_FILE, 'r') as f:
            return json.load(f)
    return []

# Save feedback to file
def save_feedback(feedback):
    with open(FEEDBACK_FILE, 'w') as f:
        json.dump(feedback, f, indent=4)

@app.route('/')
def index():
    feedback = load_feedback()
    return render_template('index.html', feedback=feedback)

@app.route('/add_feedback', methods=['POST'])
def add_feedback():
    feedback = load_feedback()
    new_feedback = {
        "name": request.form['name'],
        "message": request.form['message']
    }
    feedback.append(new_feedback)
    save_feedback(feedback)
    return redirect('/')

@app.route('/api/feedback', methods=['GET'])
def get_feedback():
    feedback = load_feedback()
    return jsonify(feedback)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

