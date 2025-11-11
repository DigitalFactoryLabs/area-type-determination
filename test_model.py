import joblib

# Load model and vectorizer
model = joblib.load('area_classifier.pkl')
vectorizer = joblib.load('vectorizer.pkl')

# Function to predict
def predict_area_type(text):
    # Vectorize the text
    text_vec = vectorizer.transform([text])
    # Predict
    prediction = model.predict(text_vec)[0]
    # Map back to label
    label = 'business' if prediction == 1 else 'residential'
    return label

# Test with some examples
test_texts = [
    "McDonald's, 847 Leila Avenue, Winnipeg",
    "Ibrahima Diallo Avenue, Winnipeg",
    "Tim Hortons, Main Street, Winnipeg",
    "Leighton Avenue, Winnipeg",
    "Ibrahima Diallo Avenue, Stock Yards, St. Boniface, Winnipeg, Manitoba, R2J 0K4, Canada",
    "Garden View Drive, Rosser–Old Kildonan, Old Kildonan, Winnipeg, Rural Municipality of West St. Paul, Rural Municipality of Rosser, Manitoba, R2P 2T5, Canada",
    "Canadian Mennonite University, Grant Avenue, Tuxedo, Charleswood - Tuxedo - Westwood, Winnipeg, Manitoba, R3P 0M4, Canada",
    "476, Leighton Avenue, Rossmere–B, Rossmere-B, Elmwood - East Kildonan, Winnipeg, Manitoba, R2K 2T4, Canada"
]

print("Testing the model:")
for text in test_texts:
    pred = predict_area_type(text)
    print(f"Text: {text}")
    print(f"Prediction: {pred}")
    print()