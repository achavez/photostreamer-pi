import os
import mimetypes
import shutil
from progressbar import *

import logger
l = logger.setup('external')

def copy_files(path):
    """
    Walk the directory tree and copy all files with the image MIME type
    """
    for root, dirs, files in os.walk(path):
        l.info("Checking directory %s", root)
        for file in files:
            mimetype = mimetypes.guess_type(file)[0]
            if isinstance(mimetype, str):
                if mimetype.split("/")[0] == "image":
                    l.info("Copying image file %s", file)

copy_files(".")

pbar = ProgressBar().start()
for i in range(100):
    time.sleep(0.1)
    pbar.update(i + 1)
pbar.finish()