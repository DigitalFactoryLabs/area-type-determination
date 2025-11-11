import requests
import json

# First, find the exact coordinates of the address
address = "11 Devonshire, Winnipeg"
print(f"Searching for coordinates: {address}")

# Nominatim for address search
nominatim_url = "https://nominatim.openstreetmap.org/search"
params = {
    'q': address,
    'format': 'json',
    'limit': 1
}
headers = {'User-Agent': 'OverpassScript/1.0'}

resp = requests.get(nominatim_url, params=params, headers=headers)
results = resp.json()

if results:
    lat = float(results[0]['lat'])
    lon = float(results[0]['lon'])
    print(f"Found: {lat}, {lon}")
    
    # 20 meters ≈ 0.0002 degrees
    delta = 0.0002
    south = lat - delta
    north = lat + delta
    west = lon - delta
    east = lon + delta
    
    # Query to Overpass
    query = f"""
    [out:json];
    (
      node({south},{west},{north},{east});
      way({south},{west},{north},{east});
    );
    out center;
    """
    
    print("Getting data from Overpass API...")
    response = requests.post(
        'https://overpass-api.de/api/interpreter',
        data={'data': query}
    )
    
    data = response.json()
    objects = data['elements']
    
    print(f"\nReceived objects: {len(objects)}")
    
    # Save
    with open('devonshire_20m.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print("Data saved to devonshire_20m.json")
    
    # Show what was found
    print("\nObjects within 20m radius:")
    for obj in objects[:15]:
        tags = obj.get('tags', {})
        name = tags.get('name', 'unnamed')
        print(f"- {name}: {tags}")
else:
    print("Address not found")
