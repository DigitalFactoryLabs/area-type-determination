import urllib.request
import urllib.parse
import json
import time

# Function for reverse geocoding
def reverse_geocode(lat, lon):
    url = "https://nominatim.openstreetmap.org/reverse"
    params = {
        'lat': str(lat),
        'lon': str(lon),
        'format': 'json'
    }
    query_string = urllib.parse.urlencode(params)
    full_url = url + '?' + query_string
    headers = {'User-Agent': 'AreaTypeDetermination/1.0'}
    req = urllib.request.Request(full_url, headers=headers)
    try:
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode('utf-8'))
            return data
    except Exception as e:
        print(f"Error for {lat}, {lon}: {e}")
        return None

# Reading points from file
points = []
with open('test_random_points.txt', 'r') as f:
    for line in f:
        lat, lon = line.strip().split(',')
        points.append((float(lat), float(lon)))

# Processing each point
results = []
for i, (lat, lon) in enumerate(points):
    print(f"Processing point {i+1}: {lat}, {lon}")
    data = reverse_geocode(lat, lon)
    if data:
        results.append({
            'lat': lat,
            'lon': lon,
            'address': data
        })
    time.sleep(1)  # Delay to comply with Nominatim limits

# Saving to JSON
with open('test_geocoded_points.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print("Results saved to test_geocoded_points.json")