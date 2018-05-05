import requests
import logging
import config
from flask_ask import context, statement

# Retrieve the user's location
def get_location():
    URL =  "https://api.amazonalexa.com/v1/devices/{}/settings" \
           "/address".format(context.System.device.deviceId)
    TOKEN =  context.System.user.permissions.consentToken
    HEADER = {'Accept': 'application/json',
             'Authorization': 'Bearer {}'.format(TOKEN)}
    r = requests.get(URL, headers=HEADER)
    
    if(r.status_code == 200):
        loc = r.json()
        address = "{}".format(loc["addressLine1"].encode("utf-8"))
        city = "{}".format(loc["city"].encode("utf-8"))
        state = "{}".format(loc["stateOrRegion"].encode("utf-8"))
        logging.info("City: " + city)
        logging.info("Address: " + address)
        logging.info("State: " + state)
        return address, city, state
    else:
        #error
        pass

# Use Google Places API and user's address to find nearby help
def find_nearby_help():
    # Google API key
    key = config.API_KEY
    # keyword for Google Places search
    keyword = "therapist OR psychologist OR counselor"
    # defaulting return contents to None
    
    try:
        # attempt to access Alexa's address
        address, city, state = get_location()
    except:
        return statement("I don't have permission to get your location. Please allow access to your location and try again")
    
    location = "'{} {} {}'".format(address, city, state)
    geocodeURL = "https://maps.googleapis.com/maps/api/geocode/json?address={}&key={}".format(location,key)
   
    # request latitude and longitude values using Alexa's address
    latlng_req = requests.get(geocodeURL)
    # checking for successful request (at least 1 geocode returned)
    if latlng_req.status_code == 200:
        latlng_json = latlng_req.json()
        # extracting first geocode latitude and longitude values
        lat = latlng_json['results'][0]['geometry']['location']['lat']
        lng = latlng_json['results'][0]['geometry']['location']['lng']
        latlng = "{},{}".format(lat, lng)
        # specifying ~15 mi radius for search
        radius = 24000
        placesURL = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={}&radius={}&keyword={}&key={}".format(latlng,radius,keyword,key)
        
        # request nearby clinics
        places_req = requests.get(placesURL)
        
        # checking for successful request (at least 1 place returned)
        if places_req.status_code == 200:
            places_json = places_req.json()
            # extracting first place_id
            place_id = places_json['results'][0]['place_id']
            detailsURL = "https://maps.googleapis.com/maps/api/place/details/json?placeid={}&key={}".format(place_id, key)
            
            # request for place details
            details_req = requests.get(detailsURL)
            
            # checking for successful request
            if details_req.status_code == 200:
                details_json = details_req.json()
                # extracting place name and phone number
                place_name = places_json['results'][0]['name']
                place_phone = details_json['result']['international_phone_number']
                # constructing return statement with place name and phone number
                return "I've found professional help nearby. The place is called {} and their phone number is {}.".format(place_name, place_phone)
    return "Sorry, I'm having trouble doing that right now. Please try again later."