from boto.s3.connection import S3Connection
from boto.s3.key import Key

import settings

def connect():
    """
    Return a connected S3 bucket based on settings in
    config.cfg.
    """
    cfg = settings.config()
    aws_access_key = cfg.get('s3', 'access_key')
    aws_secret_key = cfg.get('s3', 'secret_key')
    aws_s3_bucket = cfg.get('s3', 'bucket')
    conn = S3Connection(aws_access_key, aws_secret_key)
    bucket = conn.get_bucket(aws_s3_bucket)
    return bucket

def save(src, dest):
    """
    Save a file to S3 and return the S3 object.
    """
    bucket = connect()
    s3 = Key(bucket)
    s3.key = dest
    s3.set_contents_from_filename(src)
    return s3