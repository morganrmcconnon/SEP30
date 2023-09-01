from geopy.geocoders import Nominatim
GEOLOCATOR = Nominatim(user_agent="location_detection", timeout=60)


def detect_coordinates(location_description, language="en"):
    """
    Detect the location of a location description text in English using geopy.

    Returns location latitude and longitude as a tuple.

    Sometimes the geocoding service returns None. In this case, the function returns None.

    The source code of this function is editable. Instead of returning location.raw, you can return any part of the location object:
    
    `location.address`

    `location.altitude`
    
    `location.latitude`
    
    `location.longitude`
    
    `location.point`
    
    `location.raw`

    The most complete return value you can return is `location.raw`, a dictionary containing the raw JSON response from the geocoding service.
    
    Example output of `location.raw`:

    ```json
    {
        'place_id': 253308938, 
        'licence': 'Data © OpenStreetMap contributors, ODbL 1.0. http://osm.org/copyright', 
        'osm_type': 'relation', 
        'osm_id': 2067731, 
        'lat': '14.8971921', 
        'lon': '100.83273', 
        'class': 'boundary', 
        'type': 'administrative', 
        'place_rank': 4, 
        'importance': 0.7626272891555399, 
        'addresstype': 'country', 
        'name': 'ประเทศไทย', 
        'display_name': 'ประเทศไทย', 
        'boundingbox': ['5.6128510', '20.4648337', '97.3438072', '105.6368120']
    }
    ```

    """
    try:
        location = GEOLOCATOR.geocode(location_description, timeout=60, language=language)
        if location:
            return location.latitude, location.longitude
        else:
            return None
        
    except Exception as e:
        print(e)
        return None
    


