import json
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
import joblib

# Load the dataset
with open('geocoded_points.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Extract features and labels
texts = []
labels = []
for point in data:
    addr = point['address']
    name = addr.get('name', '')
    display_name = addr.get('display_name', '')
    # Use display_name as text feature
    text = display_name if display_name else name
    texts.append(text)
    labels.append(point['area_type'])

# Encode labels: residential=0, business=1
encoded_labels = [1 if label == 'business' else 0 for label in labels]

print(f"Dataset size: {len(texts)}")
business_count = sum(encoded_labels)
residential_count = len(encoded_labels) - business_count
print(f"Residential: {residential_count}, Business: {business_count}")

# Split data
X_train, X_test, y_train, y_test = train_test_split(texts, encoded_labels, test_size=0.2, random_state=42)

# Vectorize text
vectorizer = TfidfVectorizer(max_features=1000)
X_train_vec = vectorizer.fit_transform(X_train)
X_test_vec = vectorizer.transform(X_test)

# Train model (using LogisticRegression as simple classifier, can be replaced with NN)
model = LogisticRegression()
model.fit(X_train_vec, y_train)

# Evaluate
y_pred = model.predict(X_test_vec)
print(classification_report(y_test, y_pred))

# Save model and vectorizer
joblib.dump(model, 'area_classifier.pkl')
joblib.dump(vectorizer, 'vectorizer.pkl')

print("Model saved as area_classifier.pkl")