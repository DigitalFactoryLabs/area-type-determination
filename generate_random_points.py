import random

# Bounding box for Winnipeg (approximately: south, north, west, east)
# Source: OpenStreetMap, approximate values
south = 49.7136
north = 49.9925
west = -97.3499
east = -96.9497

print(f"Bounding box for Winnipeg: south={south}, north={north}, west={west}, east={east}")

# Step 2: Generate 100 random points
points = []
for _ in range(100):
    lat = random.uniform(south, north)
    lon = random.uniform(west, east)
    points.append((lat, lon))

# Step 3: Print and save
print("Random geo points:")
for i, (lat, lon) in enumerate(points, 1):
    print(f"{i}. {lat:.6f}, {lon:.6f}")

# Save to file
with open('test_random_points.txt', 'w') as f:
    for lat, lon in points:
        f.write(f"{lat:.6f},{lon:.6f}\n")

print("Points saved to test_random_points.txt")