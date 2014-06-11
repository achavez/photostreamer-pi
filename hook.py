#!/usr/bin/env python
import os
import time
from PIL import Image
from ConfigParser import NoOptionError

import s3
import server
import settings
import db
import logger
l = logger.setup('hook')
cfg = settings.config()

sender = 0

def generate_key(fileName):
    """
    Generate a unique filename based on the current timestamp.
    """
    timestamp = str(time.time()).replace(".", "")
    file_extension = fileName.split(".")[1]
    return timestamp + "." + file_extension

def generate_thumb(src, dest):
    """
    Create a thumbnail of the file using Pillow and return
    the path to the created thumbnail.
    """
    try:
        quality = cfg.getint('thumbs', 'quality')
        width = cfg.getint('thumbs', 'width')
        height = cfg.getint('thumbs', 'height')
    except NoOptionError as e:
        l.error("Error reading a setting from the config.cfg file: %s", e)
        raise
    size = width, height
    i = Image.open(src)
    i.thumbnail(size, Image.ANTIALIAS)
    i.save(dest, "JPEG", quality=quality)
    return dest

def transfer_to_s3(file_name):
    """
    Transfer a thumbnail photo to Amazon S3 and return the S3 Key object.
    """
    l.debug("Transferring thumbnail photo %s to Amazon S3 as %s.", file_name, key)
    dest = str(sender) + '/thumbs/' + key
    src = 'thumbs/' + key
    thumb = generate_thumb(file_name, 'thumbs/' + key)
    saved = s3.save(thumb, dest)
    if saved:
        l.info("Thumbnail photo %s transferred to Amazon S3 as %s", file_name, key)
        return saved
    else:
        l.warning("Sending thumbnail photo %s to Amazon S3 failed. Schedling for resending.",
            file_name)
        sql = db.connect()
        thumbs = sql['thumbs']
        thumbs.insert(dict(key=key, src=thumb, dest=dest))
        return False

# Handle actions fired by gphoto2

if os.environ.get("ACTION") == "init":
    if (os.path.isdir('thumbs') == False):
        os.mkdir('thumbs')
    if (os.path.isdir('full') == False):
        os.mkdir('full')

if os.environ.get("ACTION") == "download":
    file_name = os.environ.get("ARGUMENT")
    # Generate a unique filename
    key = generate_key(file_name)
    # Move the full-resolution file out of the temp folder
    os.rename(file_name, 'full/' + key)
    # Save a thumb to Amazon S3
    saved = transfer_to_s3('full/' + key)
    # And if that succeeds, notify photostreamer-server
    if saved:
        server.post_thumb('full/' + key, saved, key)