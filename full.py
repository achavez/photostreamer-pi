#!/usr/bin/env python
import os
from boto.s3.connection import S3Connection
from boto.s3.key import Key
import json
import requests

import s3

sender = 0

def upload_full_image(fileId):
    print "Transferring " + fileId + " to Amazon S3."
    dest = str(sender) + '/full/' + fileId
    src = 'full/' + fileId
    s3.save(src, dest)
    print "Transfer of " + fileId + " to Amazon S3 complete."
    return saved

def post_to_server(saved, fileId):
    payload = {
        "sender" : sender,
        "fileid": fileId,
        "full": s3.generate_url(expires_in=0, query_auth=False)
    }
    r = requests.post('http://localhost:8080/photo/full',
        data=json.dumps(payload), headers={'content-type': 'application/json'})
    print r.status_code

r = requests.get('http://localhost:8080/requests/' + str(sender))
response = r.json()
if response:
	for fileId in response:
		saved = upload_full_image(fileId)
		post_to_server(saved, fileId)
else:
	print "No photos requested" 