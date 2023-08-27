
"""#Install Geocoder
pip install geopy
"""
import json
from geopy.geocoders import Nominatim


with open('test.json', 'r') as json_file:
    for line in json_file:
        try:
            data = json.loads(line)
            # Check if the "user" field is a dictionary
            if "user" in data and isinstance(data["user"], dict):
                # Extract the user's location
                user_location_eng = data["user"].get("location", "")

                # Initialize a geocoder
                geolocator = Nominatim(user_agent="location_detection")

                if user_location_eng:
                    location_eng = geolocator.geocode(user_location_eng)

                    if location_eng:
                        # Extract the latitude and longitude
                        latitude = location_eng.latitude
                        longitude = location_eng.longitude

                        # Print the coordinates
                        print(f"Latitude: {latitude}, Longitude: {longitude}")
                    else:
                        print("Location not found")
                else:
                    print("User location not provided")

            else:
                print("Invalid JSON structure: 'user' should be a dictionary")

        except json.JSONDecodeError as e:
            print("Error decoding JSON:", str(e))
        except Exception as e:
            print("Error:", str(e))