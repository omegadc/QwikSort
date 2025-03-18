import os

class FileInfo:
    def __init__(self, name, extension, path, size, dateCreated, dateModified, playbackLength):
        self.name = name
        self.extension = extension
        self.path = path
        self.size = size
        self.dateCreated = dateCreated
        self.dateModified = dateModified
        self.playbackLength = playbackLength # -1 for non-video files

# Helper function to retrieve metadata for a file and return a dictionary
def getMetadata(path):
    size = os.path.getsize()
    dateModified = os.path.getmtime()
    dateCreated = os.path.getctime()

# Construct a FileInfo object from the path of the file
# @classmethod
# def fromPath(cls, filePath):