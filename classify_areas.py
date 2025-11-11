import json

# Load the geocoded points
with open('geocoded_points.json', 'r', encoding='utf-8') as f:
    points = json.load(f)

# Function to classify area type based on address data
def classify_area_type(address):
    addresstype = address.get('addresstype', '')
    addr_class = address.get('class', '')
    addr_type = address.get('type', '')

    if addresstype == 'building':
        return 'residential'
    elif addresstype == 'amenity':
        return 'business'
    elif addresstype == 'road':
        # Check if it's a main road or in business area
        name = address.get('name', '').lower()
        if 'highway' in name or 'parkway' in name or 'drive' in name:
            # Assume residential unless specific
            return 'residential'
        else:
            return 'residential'  # Default
    else:
        return 'residential'  # Default

# Add area_type to each point
for point in points:
    point['area_type'] = classify_area_type(point['address'])

# Save back to file
with open('geocoded_points.json', 'w', encoding='utf-8') as f:
    json.dump(points, f, ensure_ascii=False, indent=2)

print("Area types added to geocoded_points.json")