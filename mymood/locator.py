import requests
import logging
from flask_ask import context

def get_location():
    URL =  "https://api.amazonalexa.com/v1/devices/{}/settings" \
           "/address".format(context.System.device.deviceId)
    TOKEN =  context.System.user.permissions.consentToken
    HEADER = {'Accept': 'application/json',
             'Authorization': 'Bearer {}'.format(TOKEN)}
    r = requests.get(URL, headers=HEADER)
    
    if(r.status_code == 200):
        loc = r.json()
        city = "{}".format(loc["city"].encode("utf-8"))
        address = "{}".format(loc["addressLine1"].encode("utf-8"))
        postal = "{}".format(loc["postalCode"].encode("utf-8"))
        logging.info("City: " + city)
        logging.info("Address: " + address)
        logging.info("Postal: " + postal)
        return city, address, postal
    else:
        #error
        pass

def find_nearby_help():
    #TODO find nearby help based on location
    city, address, postal = get_location()
    helps = None
    
    return helps