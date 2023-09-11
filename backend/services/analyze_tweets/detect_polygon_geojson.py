import os
import geopandas as gpd
from shapely.geometry import Point

# Load the country polygons

current_dir = os.path.dirname(__file__)
geojson_file = os.path.join(current_dir, "..", "data", "countries.geojson")
COUNTRIES_DF : gpd.GeoDataFrame = gpd.read_file(geojson_file)
country_name_key_in_properties = "ADMIN"

def detect_geojson_ploygon(latitude, longitude):
    """
    Given the latitude and longitude in floating digits, return the country name in the geojson file if the point is in the country polygon.
    """    
    location = Point(longitude, latitude)

    country_names = COUNTRIES_DF.loc[COUNTRIES_DF.geometry.contains(location), country_name_key_in_properties]

    if len(country_names) == 0:
        return None
    else:
        return country_names.values[0]
