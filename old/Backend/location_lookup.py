import json
import geopandas as gpd
from shapely.geometry import Point

# Load the country polygons
countries = gpd.read_file('countries.geojson')

# For each line (user) in the user data
with open('test_user_location.json') as f:
    for line in f:
        user = json.loads(line)

        # If the user has a latitude and longitude
        if 'latitude' in user and 'longitude' in user:
            user_location = Point(user['longitude'], user['latitude'])

            # Find the country that contains the user's location
            country = countries.loc[countries.geometry.contains(user_location), 'ADMIN']

            # Print the user's Twitter username and the country
            print("Name:", "@" + user['screen_name'][0])
            if not country.empty:
                print("Country:", country.iloc[0])
            else:
                print("Country: Not found")
