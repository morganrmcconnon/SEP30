import geopandas as gpd
from shapely.geometry import Point

# Load the country polygons
GEOJSON_FILE = 'countries.geojson'
countries : gpd.GeoDataFrame = gpd.read_file(GEOJSON_FILE)
country_name_key_in_properties = 'ADMIN'

def point_is_in_geojson_ploygon(latitude, longitude):
    """
    Given the latitude and longitude in floating digits, return the country name in the geojson file if the point is in the country polygon.
    """    

    location = Point(longitude, latitude)

    return countries.loc[countries.geometry.contains(location), country_name_key_in_properties].values[0]