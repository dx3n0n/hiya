import pandas as pd
import re
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
import pickle

# Load your dataset (assume it has 'url' and 'label' columns, where 'label' is 0 for benign and 1 for phishing)
# dataset.csv should be a CSV file with at least two columns: 'url' and 'label'
data = pd.read_csv('dataset.csv')  

# Feature extraction from URLs
def extract_features(url):
    url_length = len(url)
    num_dots = url.count('.')
    num_digits = sum(c.isdigit() for c in url)
    num_special_chars = sum(1 for c in url if not c.isalnum())
    return [url_length, num_dots, num_digits, num_special_chars]

# Apply feature extraction to all URLs
data['features'] = data['url'].apply(extract_features)
X = list(data['features'])
y = data['label']

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train a model (logistic regression)
model = LogisticRegression()
model.fit(X_train, y_train)

# Test model accuracy
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"Model Accuracy: {accuracy * 100:.2f}%")

# Save the trained model for later use
with open('phishing_model.pkl', 'wb') as model_file:
    pickle.dump(model, model_file)
