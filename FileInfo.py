import os
import time

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
    def getMetadata(self, filePath):
        filename, fileextension = os.path.splitext(filePath)
        filesize = os.path.getsize(filePath)
        fileDateModified = os.path.getmtime(filePath)
        fileDateCreated = os.path.getctime(filePath)

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
        return (f"FileInfo(name={self.name!r}, extension={self.extension!r}, "
                f"path={self.path!r}, size={self.size}, "
                f"dateCreated={self.dateCreated}, dateModified={self.dateModified})")
    
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
    print(f"Date Created: {time.ctime(file_info.dateCreated)}")
    print(f"Date Modified: {time.ctime(file_info.dateModified)}")

# Only run main when directly testing
if __name__ == "__main__":
    main()