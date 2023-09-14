import geopandas as gpd
from shapely.geometry import Point

# Load the country polygons


def detect_geojson_ploygon(latitude, longitude, geojson_file = 'countries.geojson', country_name_key_in_properties = 'ADMIN'):
    """
    Given the latitude and longitude in floating digits, return the country name in the geojson file if the point is in the country polygon.
    """    
    countries : gpd.GeoDataFrame = gpd.read_file(geojson_file)

    location = Point(longitude, latitude)

    return countries.loc[countries.geometry.contains(location), country_name_key_in_properties].values[0]