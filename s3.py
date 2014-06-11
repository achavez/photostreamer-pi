from boto.s3.connection import S3Connection
import boto
from boto.s3.key import Key
from socket import gaierror
from ConfigParser import NoOptionError

import settings
import logger
l = logger.setup(__name__)

def connect():
    """
    Return a connected S3 bucket based on settings in
    config.cfg.
    """
    # Reduce the number of retries to 1 if it's not set already so requests
    # fail quickly rather than delaying the downloading of photos
    if not boto.config.has_option('Boto', 'num_retries'):
        if not boto.config.has_section('Boto'):
            boto.config.add_section('Boto')
            boto.config.set('Boto', 'num_retries', '1')
    cfg = settings.config()
    try:
        aws_access_key = cfg.get('s3', 'access_key')
        aws_secret_key = cfg.get('s3', 'secret_key')
        aws_s3_bucket = cfg.get('s3', 'bucket')
    except NoOptionError as e:
        l.error("Error reading a setting from the config.cfg file: %s", e)
        raise
    conn = S3Connection(aws_access_key, aws_secret_key)
    bucket = conn.get_bucket(aws_s3_bucket, validate=False)
    return bucket

def save(src, dest):
    """
    Save a file to S3 and return the S3 object.
    """
    bucket = connect()
    s3 = Key(bucket)
    s3.key = dest
    try:
        s3.set_contents_from_filename(src)
        return s3
    except gaierror as e:
        l.error("Network error encountered trying to reach Amazon S3: %s", e)
        return False
    except IOError as e:
        l.exception("Error reading from source file: %s", e)
        return False
    except:
        l.exception("Uncaught exception while saving to Amazon S3.")
        return False