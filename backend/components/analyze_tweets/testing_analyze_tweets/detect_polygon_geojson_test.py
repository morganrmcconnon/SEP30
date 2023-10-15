import unittest
from ..detect_polygon_geojson import detect_geojson_ploygon

class TestDetectPolygonGeoJSON(unittest.TestCase):

    def test_detect_geojson_polygon(self):
        # Define a test case with known latitude and longitude
        latitude = 37.7749  # Example latitude
        longitude = -122.4194  # Example longitude
        geo_dataframe_key = 'name'  # Replace with the actual key used in your GeoDataFrame

        # Call the detect_geojson_ploygon function
        country_name = detect_geojson_ploygon(latitude, longitude, geo_dataframe_key)

        # Print the detected country name for debugging purposes
        print(f"Detected country: {country_name}")

        # Assert that the detected country name is not None
        # You can also assert for a specific country name if you know the expected result
        self.assertIsNotNone(country_name)

    def test_detect_geojson_polygon_outside_any_country(self):
        # Define a test case with latitude and longitude outside any country's polygon
        latitude = 0.0
        longitude = 0.0
        geo_dataframe_key = 'name'  # Replace with the actual key used in your GeoDataFrame

        # Call the detect_geojson_ploygon function
        country_name = detect_geojson_ploygon(latitude, longitude, geo_dataframe_key)

        # Print the detected country name for debugging purposes
        print(f"Detected country: {country_name}")

        # Assert that the detected country name is None as the coordinates are not inside any country's polygon
        self.assertIsNone(country_name)

if __name__ == "__main__":
    unittest.main()
