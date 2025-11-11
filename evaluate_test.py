import json

# Function to classify area type based on address data (same as in classify_areas.py)
def classify_area_type(address):
    addresstype = address.get('addresstype', '')
    addr_class = address.get('class', '')
    addr_type = address.get('type', '')

    if addresstype == 'building':
        return 'residential'
    elif addresstype == 'amenity':
        return 'business'
    elif addresstype == 'road':
        # Assume residential
        return 'residential'
    else:
        return 'residential'  # Default

# Load test predictions
with open('test_predictions.json', 'r', encoding='utf-8') as f:
    test_data = json.load(f)

correct = 0
total = len(test_data)
residential_true = 0
business_true = 0
wrong_indices = []

for i, point in enumerate(test_data):
    addr = point['address']
    true_label = classify_area_type(addr)
    pred_label = point['predicted_area_type']
    
    if true_label == 'residential':
        residential_true += 1
    else:
        business_true += 1
    
    if true_label == pred_label:
        correct += 1
    else:
        wrong_indices.append(i + 1)  # 1-based index

accuracy = correct / total
print(f"Accuracy on test dataset: {accuracy:.2f} ({correct}/{total})")
print(f"True labels: Residential {residential_true}, Business {business_true}")
print(f"Errors on lines: {wrong_indices}")