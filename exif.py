import exifread

def parse(fileName):
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