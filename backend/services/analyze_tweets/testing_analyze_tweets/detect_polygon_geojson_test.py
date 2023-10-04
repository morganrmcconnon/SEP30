import json
from detect_polygon_geojson import detect_geojson_ploygon

# Test cases
test_cases = [
    {
        "latitude": 37.7749,
        "longitude": -122.4194,
        "geo_dataframe_key": "ADMIN",
        "expected_country": "United States",
    },
    {
        "latitude": 51.5074,
        "longitude": -0.1278,
        "geo_dataframe_key": "ADMIN",
        "expected_country": "United Kingdom",
    },
    {
        "latitude": 48.8566,
        "longitude": 2.3522,
        "geo_dataframe_key": "ADMIN",
        "expected_country": "France",
    },
    {
        "latitude": 40.7128,
        "longitude": -74.0060,
        "geo_dataframe_key": "ADMIN",
        "expected_country": "United States",
    },
    {
        "latitude": -34.6118,
        "longitude": -58.4173,
        "geo_dataframe_key": "ADMIN",
        "expected_country": "Argentina",
    },
]

# Run test cases
for idx, test_case in enumerate(test_cases):
    latitude = test_case["latitude"]
    longitude = test_case["longitude"]
    geo_dataframe_key = test_case["geo_dataframe_key"]
    expected_country = test_case["expected_country"]

    result = detect_geojson_ploygon(latitude, longitude, geo_dataframe_key)

    if result == expected_country:
        print(f"Test case {idx + 1}: PASS")
    else:
        print(f"Test case {idx + 1}: FAIL")
        print(f"Expected: {expected_country}")
        print(f"Actual: {result}")

