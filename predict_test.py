import json
import joblib

# Load model and vectorizer
model = joblib.load('area_classifier.pkl')
vectorizer = joblib.load('vectorizer.pkl')

# Load test data
with open('test_geocoded_points.json', 'r', encoding='utf-8') as f:
    test_data = json.load(f)

predictions = []
residential_count = 0
business_count = 0

for point in test_data:
    addr = point['address']
    name = addr.get('name', '')
    display_name = addr.get('display_name', '')
    text = display_name if display_name else name
    
    # Predict
    text_vec = vectorizer.transform([text])
    pred = model.predict(text_vec)[0]
    label = 'business' if pred == 1 else 'residential'
    
    if label == 'residential':
        residential_count += 1
    else:
        business_count += 1
    
    # Add prediction to point
    point['predicted_area_type'] = label
    predictions.append(point)

# Save predictions
with open('test_predictions.json', 'w', encoding='utf-8') as f:
    json.dump(predictions, f, ensure_ascii=False, indent=2)

print(f"Predictions saved to test_predictions.json")
print(f"Residential: {residential_count}")
print(f"Business: {business_count}")