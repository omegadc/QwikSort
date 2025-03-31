import os
import time # TODO: Remove once done debugging, implement pytests
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
    
# TODO: Remove the code below once done debugging, implement pytests

# Test function
def main():
    test_file = "test_file.txt"

    # Create test file
    if not os.path.exists(test_file):
        with open(test_file, "w") as f:
            f.write("This is a test file.")
        print(f"Test file '{test_file}' created.")

    time.sleep(1)

    # Create FileInfo object from path
    file_info = FileInfo.fromPath(test_file)

    print("\nFileInfo object:")
    print(repr(file_info))

    print("\nExtracted Metadata:")
    print(f"File Name: {file_info.name}")
    print(f"Extension: {file_info.extension}")
    print(f"Path: {file_info.path}")
    print(f"Size: {file_info.size} bytes")
    print(f"Date Created: {file_info.dateCreated.strftime("%Y-%m-%d %H:%M:%S")}")
    print(f"Date Modified: {file_info.dateModified.strftime("%Y-%m-%d %H:%M:%S")}")

# Only run main when directly testing
if __name__ == "__main__":
    main()