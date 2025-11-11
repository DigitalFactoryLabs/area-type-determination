import json

with open('geocoded_points.json', 'r', encoding='utf-8') as f:
    points = json.load(f)

business_points = [p for p in points if p.get('area_type') == 'business']

print(f"Found {len(business_points)} business zones:")
for i, p in enumerate(business_points, 1):
    print(f"\n{i}. Lat: {p['lat']}, Lon: {p['lon']}")
    addr = p['address']
    print(f"   Name: {addr.get('name', 'N/A')}")
    print(f"   Display: {addr.get('display_name', 'N/A')}")
    print(f"   Type: {addr.get('addresstype', 'N/A')}")