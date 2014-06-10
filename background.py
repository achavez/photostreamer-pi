#!/usr/bin/env python
import pickledb

import s3
import server
import logger
l = logger.setup('background');

sender = 0

def upload_full_image(fileId):
    """
    Upload a full-resolution image to Amazon S3.
    """
    l.debug("Transferring full-resolution photo %s to Amazon S3.", fileId)
    dest = str(sender) + '/full/' + fileId
    src = 'full/' + fileId
    saved = s3.save(src, dest)
    if saved:
        l.info("Full-resolution photo %s transferred to Amazon S3.", fileId)
        return saved
    else:
        l.error("Failed to transfer full-resolution photo %s to Amazon S3.", fileId)
        return False

def post_to_server(saved, fileId):
    """
    Notify photostreamer-server that a new full-resolution photo is available
    on Amazon S3.
    """
    l.debug("Notifying photostreamer-server of full-resolution photo %s", fileId)
    payload = {
        "sender" : sender,
        "fileid": fileId,
        "full": saved.generate_url(expires_in=0, query_auth=False)
    }
    server.post('/photo/full', payload)

l.debug("Starting background job.")

db = pickledb.load('photostreamer.db', True)
sending = db.get('sending')

# There is no semaphore, so make one
if sending == None:
    l.info("No semaphore found in database. Creating one.")
    db.set('sending', False)
    sending = False

# The script isn't running, so run it
if sending == False:
    l.debug("Semaphore is False. Running background jobs.")

    # Set a semaphore using PickleDB
    db.set('sending', True)

    # Catch all exceptions here to make sure the semaphore doesn't get stuck
    # at True
    try:
        # First, send full quality versions of any files that have been
        # requested by photostreamer-server
        response = server.get('/requests/' + str(sender))
        if response:
            for fileId in response:
                saved = upload_full_image(fileId)
                if saved:
                    post_to_server(saved, fileId)
            l.info("Uploaded %d full-resolution file(s) to Amazon S3.",
                len(response))
        elif response == False:
            # API error
            pass
        else:
            l.info("No full-resolution photos have been requested.")
        db.set('sending', False)
        # Then, send thumbnails that failed to send earlier
    # Catch the exception, reset the semaphore and raise it anyway
    except:
        db.set('sending', False)
        raise

# The script is running, so don't run it for now
else:
    l.info("Not launching the background job because it's already running")

l.debug("Finished running background job.")