#!/usr/bin/env python
import pickledb
import json

import s3
import server
import logger
import db
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

pickle = pickledb.load('photostreamer.db', True)
sending = pickle.get('sending')

# There is no semaphore, so make one
if sending == None:
    l.info("No semaphore found in database. Creating one.")
    pickle.set('sending', False)
    sending = False

# The script isn't running, so run it
if sending == False:
    l.debug("Semaphore is False. Running background jobs.")

    # Set a semaphore using PickleDB
    pickle.set('sending', True)

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

        # Then, send thumbnails that failed to send earlier
        sql = db.connect()
        thumbs = sql['thumbs']
        if len(thumbs) > 0:
            l.info("Attempting to resend %d thumbnail photos to Amazon S3.",
                len(thumbs))
            successes = list()
            for thumb in thumbs:
                saved = s3.save(thumb['src'], thumb['dest'])
                if saved:
                    l.info("Thumbnail photo %s transferred to Amazon S3 as %s",
                        thumb['src'], thumb['dest'])
                    successes.append(thumb['key'])
                    server.post_thumb(thumb['src'], saved, thumb['key'])
                else:
                    l.warning("Sending thumbnail photo %s to Amazon S3 failed again.",
                        thumb['src'])
            # Delete sent photos from the database
            for success in successes:
                thumbs.delete(key=success)
                l.debug("Deleted thumbnail photo %s from the failures database.", success)
        else:
            l.debug("No thumbnail photos need to be resent to Amazon S3.")

        # Finally, resend all POSTs that have failed to send
        posts = sql['posts']
        if len(posts) > 0:
            l.info("Attempting to resend %d POSTs to photostreamer-server.",
                len(posts))
            successes = list()
            for post in posts:
                posted = server.post(post['endpoint'], json.loads(post['payload']), resend=True)
                if posted:
                    successes.append(post['id'])
                    l.info("Resending POST with ID %d to photostreamer-server succeeded.",
                        post['id'])
                else:
                    l.warning("Sending POST with ID %d to photostreamer-server failed again.",
                        post['id'])
            for success in successes:
                posts.delete(id=success)
                l.debug("Deleted POST with ID %d from the failures database.", success)

        # Clear the semaphore
        pickle.set('sending', False)

    # Catch the exception, reset the semaphore and raise it anyway
    except:
        pickle.set('sending', False)
        raise

# The script is running, so don't run it for now
else:
    l.info("Not launching the background job because it's already running")

l.debug("Finished running background job.")