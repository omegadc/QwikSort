import os
from datetime import datetime

class FileInfo:
    # Default constructor
    def __init__(self, name, extension, path, size, dateCreated, dateModified):
        self.name = name
        self.extension = extension
        self.path = path
        self.size = size
        self.dateCreated = dateCreated
        self.dateModified = dateModified

    # Helper function to retrieve metadata for a file and return a dictionary
    @staticmethod
    def getMetadata(filePath):
        filename, fileextension = os.path.splitext(os.path.basename(filePath))
        filesize = os.path.getsize(filePath)
        fileDateModified = datetime.fromtimestamp(os.path.getmtime(filePath))
        fileDateCreated = datetime.fromtimestamp(os.path.getctime(filePath))

        return dict(
            path = filePath, 
            name = filename, 
            extension = fileextension, 
            size = filesize, 
            dateModified = fileDateModified, 
            dateCreated = fileDateCreated
        )

    # Construct a FileInfo object from the path of the file
    @classmethod
    def fromPath(cls, filePath):
        fileMetadata = cls.getMetadata(filePath)
        return cls(
            fileMetadata["name"], 
            fileMetadata["extension"], 
            fileMetadata["path"], 
            fileMetadata["size"], 
            fileMetadata["dateCreated"], 
            fileMetadata["dateModified"]
        )
    
    def __repr__(self):
        return f"FileInfo(name='{self.name}', size={self.size}B)"