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
    url = request.form['url']
    features = extract_features(url)
    prediction = model.predict([features])[0]
    result = 'Phishing' if prediction == 1 else 'Benign'
    return jsonify({'url': url, 'result': result})

if __name__ == "__main__":
    app.run(debug=True)

