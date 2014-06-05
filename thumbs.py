#!/usr/bin/env python
import os
import time
from pgmagick import Image
import json
import requests
import exifread

import s3

sender = 0

def generate_key(orig_name):
    timestamp = str(time.time()).replace(".", "")
    file_extension = orig_name.split(".")[1]
    return timestamp + "." + file_extension

def transfer_to_s3(file_name):
    print "Transferring " + file_name + " to Amazon S3 as " + key
    dest = str(sender) + '/thumbs/' + key
    src = 'thumbs/' + key
    im = Image(file_name)
    im.quality(75)
    im.scale('400x400')
    im.write(src)
    saved = s3.save(src, dest)
    print "Transfer of " + key + " to Amazon S3 complete."
    return saved

def post_to_server(saved):
    # Open image file for reading (binary mode)
    f = open(file_name, 'rb')
    # Return Exif tags
    tags = exifread.process_file(f, details=False)
    filesize = os.path.getsize(file_name)
    os.rename(file_name, 'full/' + key)
    payload = {
        "sender" : sender,
        "filesize": filesize,
        "fileid": key,
        "dimensions": {
            "width": 1700,
            "height": 300
        },
        "thumbnail": saved.generate_url(expires_in=0, query_auth=False),
        "exif": parse_exif(tags)
    }
    r = requests.post('http://localhost:8080/photo/thumb',
        data=json.dumps(payload), headers={'content-type': 'application/json'})
    print r.status_code

def parse_exif(raw):
    parsed = {}
    for key, value in raw.iteritems():
        parsed[key] = str(value)
    return parsed

if os.environ.get("ACTION") == "init":
    if (os.path.isdir('thumbs') == False):
        os.mkdir('thumbs')
    if (os.path.isdir('full') == False):
        os.mkdir('full')

if os.environ.get("ACTION") == "download":
    file_name = os.environ.get("ARGUMENT")
    key = generate_key(file_name)
    saved = transfer_to_s3(file_name)
    post_to_server(saved)