import os
from Backend.file_info import FileInfo

class FolderInfo:
    def __init__(self, name, contents, isTarget, path, ruleset=None):
        self.name = name
        self.contents = contents
        self.isTarget = isTarget
        self.path = path
        self.ruleset = ruleset

    # Create a FolderInfo object from a given path
    @classmethod
    def fromPath(cls, folderPath, isTarget, ruleset=None, depth=0, max_depth=3):
        folderName = os.path.basename(folderPath)
        folderRuleset = ruleset if ruleset is not None else None
        contents = []

        # Check if the folder exists and is a directory
        if not os.path.exists(folderPath) or not os.path.isdir(folderPath):
            print(f"Folder not found or not a directory: {folderPath}")
            return cls(folderName, contents, isTarget, folderPath, ruleset=folderRuleset)

        try:
            with os.scandir(folderPath) as entries:
                for entry in entries:
                    try:
                        # Handle directories
                        if entry.is_dir(follow_symlinks=False):
                            if depth < max_depth - 1:  # Allow scanning up to the maximum depth
                                contents.append(cls.fromPath(entry.path, False, ruleset, depth + 1, max_depth))
                            else:
                                # At max depth include the folder without scanning further
                                contents.append(cls(os.path.basename(entry.path), [], False, entry.path, ruleset=folderRuleset))
                        # Handle files
                        elif entry.is_file():
                            try:
                                contents.append(FileInfo.fromPath(entry.path))
                            except FileNotFoundError as e:
                                print(f"FileNotFoundError: Skipping {entry.path} - {e}")
                    except (PermissionError, FileNotFoundError) as e:
                        print(f"Error accessing {entry.path} - {e}")
        except (PermissionError, FileNotFoundError) as e:
            print(f"Error accessing {folderPath} - {e}")
            return cls(folderName, contents, isTarget, folderPath, ruleset=folderRuleset)

        return cls(folderName, contents, isTarget, folderPath, ruleset=folderRuleset)

    # Returns a tree-structured string; useful for debugging
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

# Test function
def main():
    test_folder = "test_folder"
    testFolderInfo = FolderInfo.fromPath(test_folder, True)
    print(testFolderInfo.toTreeString())

if __name__ == "__main__":
    main()