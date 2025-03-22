import os
from file_info import FileInfo

class FolderInfo:
    def __init__(self, name, contents, isTarget):
        self.name = name
        self.contents = contents
        self.isTarget = isTarget
    
    # Function to crete a FolderInfo object from a given path
    @classmethod
    def fromPath(cls, folderPath, isTarget):
        folderName = os.path.basename(folderPath)
        contents = []

        obj = os.scandir(folderPath)

        for entry in obj:
            if entry.is_dir():
                contents.append(cls.fromPath(entry.path, False)) # A subfolder from construction should never be a target directory
            elif entry.is_file():
                contents.append(FileInfo.fromPath(entry.path))
        
        return cls(folderName, contents, isTarget)
    
    # Returns a tree structured string; useful for debugging
    def toTreeString(self, level=0):
        indent = '  ' * level
        tree = f"{indent}- {self.name}/ (target={self.isTarget})\n"
        for item in self.contents:
            if isinstance(item, FolderInfo):
                tree += item.toTreeString(level + 1)
            else:
                tree += '  ' * (level + 1) + f"- {item.name} ({item.size}B)\n"
        return tree

    def __repr__(self):
        return f"FolderInfo(name='{self.name}', isTarget={self.isTarget}, items={len(self.contents)})"


# TODO: Remove the code below once done debugging, implement pytests

# Test function
def main():
    test_folder = "test_folder"

    # Create FolderInfo object from path
    testFolderInfo = FolderInfo.fromPath(test_folder, True)

    print(testFolderInfo.toTreeString())
            
# Only run main when directly testing
if __name__ == "__main__":
    main()