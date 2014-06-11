import requests
import json
import os

import settings
import exif
import logger
l = logger.setup(__name__)

sender = 0

def post(endpoint, payload):
    """
    POST a json payload to the photostreamer-server
    """
    cfg = settings.config()
    url = cfg.get('server', 'url') + endpoint
    try:
        r = requests.post(url, 
            data=json.dumps(payload), headers={'content-type':'application/json'})
        l.debug("POSTed %s to photostreamer-server endpoint %s.", payload, endpoint)
        if r.status_code != 200:
            l.error("Received HTTP status code %d while POSTing to %s.",
                r.status_code, url)
    except requests.ConnectionError:
        l.exception("Network error trying to POST to %s.", url)


        # Send failures to the database for resending later



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

def post_thumb(local_file, s3_file, key):
    """
    Notify photostreamer-server that a new thumbnail photo has been posted
    to S3.
    """
    l.debug("Notifying photostreamer-server of thumbnail photo %s", key)
    tags = exif.parse(local_file)
    filesize = os.path.getsize(local_file)
    payload = {
        "sender" : sender,
        "filesize": filesize,
        "fileid": key,
        "thumbnail": s3_file.generate_url(expires_in=0, query_auth=False),
        "exif": tags
    }
    success = post('/photo/thumb', payload)