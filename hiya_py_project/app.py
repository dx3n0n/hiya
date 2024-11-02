from flask import Flask, request, jsonify, render_template
import pickle

app = Flask(__name__)

# Load the trained model
with open('phishing_model.pkl', 'rb') as model_file:
    model = pickle.load(model_file)

# Feature extraction function (same as used during training)
def extract_features(url):
    url_length = len(url)
    num_dots = url.count('.')
    num_digits = sum(c.isdigit() for c in url)
    num_special_chars = sum(1 for c in url if not c.isalnum())
    return [url_length, num_dots, num_digits, num_special_chars]

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    # Get JSON data from the request
    data = request.get_json()
    
    # Check if 'url' exists in the JSON data
    if not data or 'url' not in data:
        return jsonify({'error': 'No URL provided'}), 400  # Error handling

    # Extract URL and make prediction
    url = data['url']
    features = extract_features(url)
    prediction = model.predict([features])[0]
    result = 'Phishing' if prediction == 1 else 'Benign'
    
    # Return the result as JSON
    return jsonify({'url': url, 'result': result})

if __name__ == "__main__":
    app.run(debug=True)
