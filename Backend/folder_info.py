import os
from backend.file_info import FileInfo

class FolderInfo:
    def __init__(self, name, contents, is_target, path, ruleset=None):
        self.name = name
        self.contents = contents
        self.is_target = is_target
        self.path = path
        self.ruleset = ruleset

    # Create a FolderInfo object from a given path
    @classmethod
    def from_path(cls, folder_path, is_target, ruleset=None, depth=0, max_depth=3):
        folder_name = os.path.basename(folder_path)
        folder_ruleset = ruleset if ruleset is not None else None
        contents = []

        # Check if the folder exists and is a directory
        if not os.path.exists(folder_path) or not os.path.isdir(folder_path):
            print(f"Folder not found or not a directory: {folder_path}")
            return cls(folder_name, contents, is_target, folder_path, ruleset=folder_ruleset)

        try:
            with os.scandir(folder_path) as entries:
                for entry in entries:
                    try:
                        # Handle directories
                        if entry.is_dir(follow_symlinks=False):
                            if depth < max_depth - 1:  # Allow scanning up to the maximum depth
                                contents.append(cls.from_path(entry.path, False, ruleset, depth + 1, max_depth))
                            else:
                                # At max depth include the folder without scanning further
                                contents.append(cls(os.path.basename(entry.path), [], False, entry.path, ruleset=folder_ruleset))
                        # Handle files
                        elif entry.is_file():
                            try:
                                contents.append(FileInfo.from_path(entry.path))
                            except FileNotFoundError as e:
                                print(f"FileNotFoundError: Skipping {entry.path} - {e}")
                    except (PermissionError, FileNotFoundError) as e:
                        print(f"Error accessing {entry.path} - {e}")
        except (PermissionError, FileNotFoundError) as e:
            print(f"Error accessing {folder_path} - {e}")
            return cls(folder_name, contents, is_target, folder_path, ruleset=folder_ruleset)

        return cls(folder_name, contents, is_target, folder_path, ruleset=folder_ruleset)

    # Returns a tree-structured string; useful for debugging
    def to_tree_string(self, level=0):
        indent = '  ' * level
        tree = f"{indent}- {self.name}/ (target={self.is_target})\n"
        for item in self.contents:
            if isinstance(item, FolderInfo):
                tree += item.to_tree_string(level + 1)
            else:
                tree += '  ' * (level + 1) + f"- {item.name} ({item.size}B)\n"
        return tree

    def __repr__(self):
        return f"FolderInfo(name='{self.name}', is_target={self.is_target}, items={len(self.contents)})"