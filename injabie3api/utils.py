
from .constants import ALLOWED_EXTENSIONS

def isAllowedFilename(filename):
    dotInName = "." in filename
    allowedExtension = filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
    return dotInName and allowedExtension
