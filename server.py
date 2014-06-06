import requests
import json
import ConfigParser

def post(endpoint, payload):
    """
    POST a json payload to the photostreamer-server
    """
    config = ConfigParser.ConfigParser()
    config.readfp(open('config.cfg'))
    url = config.get('server', 'url') + endpoint
    r = requests.post(url,
        data=json.dumps(payload), headers={'content-type': 'application/json'})
    return r.status_code

def get(endpoint):
    """
    GET a json payload from the photostreamer-server
    """
    config = ConfigParser.ConfigParser()
    config.readfp(open('config.cfg'))
    url = config.get('server', 'url') + endpoint
    r = requests.get(url)
    return r.json()