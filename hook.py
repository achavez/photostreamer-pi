#!/usr/bin/env python
import os
import time
from PIL import Image
import exifread

import s3
import server
import settings
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
    quality = cfg.getint('thumbs', 'quality')
    width = cfg.getint('thumbs', 'width')
    height = cfg.getint('thumbs', 'height')
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
    l.info("Thumbnail photo %s transferred to Amazon S3 as %s", file_name, key)
    return saved

def post_to_server(saved):
    """
    Notify photostreamer-server that a new thumbnail photo has been posted
    to S3.
    """
    l.debug("Notifying photostreamer-server of thumbnail photo %s", key)
    tags = parse_exif(file_name)
    filesize = os.path.getsize(file_name)
    # Move the full-resolution photo to the full directory and rename it
    os.rename(file_name, 'full/' + key)
    payload = {
        "sender" : sender,
        "filesize": filesize,
        "fileid": key,
        "thumbnail": saved.generate_url(expires_in=0, query_auth=False),
        "exif": tags
    }
    server.post('/photo/thumb', payload)

def parse_exif(fileName):
    """
    Pull the EXIf info from a photo and sanitize it so for sending as JSON
    by converting values to strings.
    """
    f = open(fileName, 'rb')
    exif = exifread.process_file(f, details=False)
    parsed = {}
    for key, value in exif.iteritems():
        parsed[key] = str(value)
    return parsed


# Handle actions fired by gphoto2

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