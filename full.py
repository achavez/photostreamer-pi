#!/usr/bin/env python
import pickledb

import s3
import server

sender = 0

def upload_full_image(fileId):
    print "Transferring " + fileId + " to Amazon S3."
    dest = str(sender) + '/full/' + fileId
    src = 'full/' + fileId
    saved = s3.save(src, dest)
    print "Transfer of " + fileId + " to Amazon S3 complete."
    return saved

def post_to_server(saved, fileId):
    payload = {
        "sender" : sender,
        "fileid": fileId,
        "full": saved.generate_url(expires_in=0, query_auth=False)
    }
    print server.post('/photo/full', payload)

db = pickledb.load('photostreamer.db', True)
sending = db.get('sending')

# There is no semaphore, so make one
if sending == None:
	db.set('sending', False)
	sending = False

# The script isn't running, so run it
if sending == False:
	db.set('sending', True)
	response = server.get('/requests/' + str(sender))
	if response:
		for fileId in response:
			saved = upload_full_image(fileId)
			post_to_server(saved, fileId)
		print "Finished sending full quality files."
	else:
		print "No photos have been requested."
	db.set('sending', False)
# The script is running, so don't run it for now
else:
	print "Still sending last files ... will try again later."