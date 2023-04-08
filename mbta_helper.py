# Your API KEYS (you need to use your own keys - very long random characters)
from config import MAPBOX_TOKEN, MBTA_API_KEY
import requests
import urllib.request
import json
from pprint import pprint

# Useful URLs (you need to add the appropriate parameters for your requests)
MAPBOX_BASE_URL = "https://api.mapbox.com/geocoding/v5/mapbox.places"
MBTA_BASE_URL = "https://api-v3.mbta.com/stops"
MAPBOX_TOKEN = "pk.eyJ1IjoianNhYmhhcndhbDEiLCJhIjoiY2xnNzZoNGh6MDF5ajNvcDlpdXA2MGVjeiJ9.5qRWcIwZI12qAcsQBtcRnw"
MBTA_API_KEY = "b32b95585d7e4380860cd897dcb6b8ae"
OPENWEATHER_API_KEY = "339c066686f54c82b7751d1e834fb4ef"


def get_json(url: str) -> dict:
    """
    Given a properly formatted URL for a JSON web API request, return a Python JSON object containing the response to that request.

    Both get_lat_long() and get_nearest_station() might need to use this function.
    """
    f = urllib.request.urlopen(url)
    response_text = f.read().decode('utf-8')
    response_data = json.loads(response_text)
    return response_data 


def get_lat_long(place_name: str) -> tuple[str, str]:
    """
    Given a place name or address, return a (latitude, longitude) tuple with the coordinates of the given place.

    See https://docs.mapbox.com/api/search/geocoding/ for Mapbox Geocoding API URL formatting requirements.
    """
    place_name = urllib.parse.quote_plus(place_name)
    url = f"{MAPBOX_BASE_URL}/{place_name}.json?access_token={MAPBOX_TOKEN}"
    
    url = "https://api.mapbox.com/geocoding/v5/mapbox.places/{}.json".format(place_name)
    data = get_json(url)
    coords = data['features'][0]['geometry'][0]['coordinates']
    coordinates = coords['1'], coords['0']
    return coordinates
    


def get_nearest_station(latitude: str, longitude: str) -> tuple[str, bool]:
    """
    Given latitude and longitude strings, return a (station_name, wheelchair_accessible) tuple for the nearest MBTA station to the given coordinates.

    See https://api-v3.mbta.com/docs/swagger/index.html#/Stop/ApiWeb_StopController_index for URL formatting requirements for the 'GET /stops' API.
    """
    url = f'{MBTA_BASE_URL}?sort=distance&filter%5Blatitude%5D={latitude}&filter%5Blongitude%5D={longitude}&filter%5Bradius%5D=5000'
    data = get_json(url)
    nearest_station = data['data'][0]['attributes']['name']
    wheelchair = data['data'][0]['attributes']['wheelchair_boarding']
    if wheelchair == 0:
        accessibility = 'No Information'
    elif wheelchair == 1:
        accessibility = 'Accessible'
    else:
        accessibility = 'Inaccessible'
    return nearest_station, accessibility


def find_stop_near(place_name: str) -> tuple[str, bool]:
    """
    Given a place name or address, return the nearest MBTA stop and whether it is wheelchair accessible.

    This function might use all the functions above.
    """
    place_name = str(place_name) + ', MA'
    #print(place_name)
    coordinates = get_lat_long(place_name)
    latitude = str(coordinates[0])
    longitude = str(coordinates[1])
    res = get_nearest_station(latitude, longitude)
    return res

def get_weather(place_name: str):  
    """
    Given a place name, return the current weather at that location. 
    """     
    lat, long = get_lat_long(place_name)
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={long}&appid={OPENWEATHER_API_KEY}"
    response = get_json(url)
    return response

def main():
    """
    You can test all the functions here
    """
    print(get_nearest_station(42.3551, 71.0656))
    print(find_stop_near("Fenway, MA"))

if __name__ == '__main__':
    main()
