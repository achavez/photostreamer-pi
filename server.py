import requests
import json

import settings
import logger
l = logger.setup(__name__)

def post(endpoint, payload):
    """
    POST a json payload to the photostreamer-server
    """
    cfg = settings.config()
    url = cfg.get('server', 'url') + endpoint
    try:
        r = requests.post(url, 
            data=json.dumps(payload), headers={'content-type':'application/json'})
        l.debug("POSTed to %s photostreamer-server endpoing %s.", payload, endpoint)
        if r.status_code != 200:
            l.error("Received HTTP status code %d while trying to reach %s.",
                r.status_code, url)
    except requests.ConnectionError:
        l.exception("Network error trying to POST to %s.", url)

def get(endpoint):
    """
    GET a json payload from the photostreamer-server
    """
    cfg = settings.config()
    url = cfg.get('server', 'url') + endpoint
    try:
        r = requests.get(url)
        if r.status_code == 200:
            l.debug("photostreamer-server endpoint %s responded with %s", endpoint, r.json())
            return r.json()
        else:
            l.error("Received HTTP status code %d while trying to reach %s.",
                r.status_code, url)
            return False
    except requests.ConnectionError:
        l.error("Network error trying to GET %s.", url)
        return False