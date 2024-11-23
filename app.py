from flask import Flask, request, jsonify, render_template

# Initialize Flask app
app = Flask(__name__)

# Store feedback in memory (temporary)
feedbacks = []

@app.route('/')
def home():
    """Render the homepage with feedbacks."""
    return render_template('index.html', feedbacks=feedbacks)

@app.route('/add_feedback', methods=['POST'])
def add_feedback():
    """API to handle adding feedback."""
    data = request.json
    feedback = data.get('feedback', '').strip()
    if not feedback:
        return jsonify({'error': 'Feedback cannot be empty'}), 400
    feedbacks.append(feedback)
    return jsonify({'message': 'Feedback added successfully', 'feedbacks': feedbacks})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
