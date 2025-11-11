import urllib.request
import urllib.parse
import json
import time

# Function to search Nominatim
def search_nominatim(query, limit=10):
    url = "https://nominatim.openstreetmap.org/search"
    params = {
        'q': query,
        'format': 'json',
        'limit': limit,
        'bounded': 1,
        'viewbox': '-97.3499,49.9925,-96.9497,49.7136'  # Winnipeg bbox
    }
    query_string = urllib.parse.urlencode(params)
    full_url = url + '?' + query_string
    headers = {'User-Agent': 'AreaTypeDetermination/1.0'}
    req = urllib.request.Request(full_url, headers=headers)
    with urllib.request.urlopen(req) as response:
        data = json.loads(response.read().decode('utf-8'))
    return data

# Function to reverse geocode
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
    with urllib.request.urlopen(req) as response:
        data = json.loads(response.read().decode('utf-8'))
    return data

# Search for Tim Hortons in Winnipeg
tim_hortons = search_nominatim("Tim Hortons Winnipeg", 50)
print(f"Found {len(tim_hortons)} Tim Hortons locations")

# Load existing points
with open('geocoded_points.json', 'r', encoding='utf-8') as f:
    points = json.load(f)

# Add Tim Hortons as business points
for th in tim_hortons:
    lat = float(th['lat'])
    lon = float(th['lon'])
    # Reverse geocode to get full address
    address = reverse_geocode(lat, lon)
    point = {
        'lat': lat,
        'lon': lon,
        'address': address,
        'area_type': 'business'
    }
    points.append(point)
    time.sleep(1)  # Delay

# Save back
with open('geocoded_points.json', 'w', encoding='utf-8') as f:
    json.dump(points, f, ensure_ascii=False, indent=2)

print(f"Added {len(tim_hortons)} Tim Hortons locations. Total points: {len(points)}")