## Overview

The `FolderInfo` class represents a directory and its contents within the file system hierarchy. It is used to build an in-memory snapshot of the target directory structure, including subfolders (up to a defined depth) and files (represented as `FileInfo` objects). This structure is fundamental for browsing directories in the UI and for identifying files to be processed by sorting jobs.

*Note: FolderInfo contains references to an assigned `ruleset`, but this functionality has been implemented elsewhere.*

## Class: `FolderInfo`

Represents a directory and its contents (files and subdirectories).

### `__init__(self, name, contents, is_target, path, ruleset=None)`

-   **Purpose:** Constructs a `FolderInfo` object.
-   **Parameters:**
    -   `name` (str): The name of the folder (basename).
    -   `contents` (list): A list containing `FileInfo` objects (for files) and other `FolderInfo` objects (for subdirectories) within this folder.
    -   `is_target` (bool): A flag indicating if this folder is the primary target directory selected by the user for sorting.
    -   `path` (str): The absolute path to the folder.
    -   `ruleset` (Ruleset, optional): A potential reference to a `Ruleset` associated with this folder (implemented elsewhere).

### `classmethod from_path(cls, folder_path, is_target, ruleset=None, depth=0, max_depth=3)`

-   **Purpose:** Factory method to recursively scan a directory path and build a `FolderInfo` object representing its structure and contents.
-   **Parameters:**
    -   `folder_path` (str): The absolute path to the directory to scan.
    -   `is_target` (bool): Flag indicating if this is the root target folder.
    -   `ruleset` (optional): Passed down during recursion (implemented elsewhere).
    -   `depth` (int): Current recursion depth (internal use).
    -   `max_depth` (int): The maximum depth to scan into subdirectories. Defaults to 3.
-   **Returns:** (FolderInfo) A new `FolderInfo` object representing the scanned directory.
-   **Details:**
    -   Uses `os.scandir` for efficient directory iteration.
    -   Checks if `folder_path` exists and is a directory.
    -   For each entry:
        -   If it's a directory and `depth < max_depth - 1`, recursively calls `from_path` to scan the subdirectory.
        -   If it's a directory and `depth == max_depth - 1`, includes it as an empty `FolderInfo` object (stops recursion).
        -   If it's a file, creates a `FileInfo` object using `FileInfo.from_path`.
    -   Handles `PermissionError` and `FileNotFoundError` during scanning by printing an error message and skipping the problematic entry or folder. Returns a partially constructed or empty `FolderInfo` object in case of errors accessing the main `folder_path`.

### `to_tree_string(self, level=0)`

-   **Purpose:** Generates a string representation of the folder hierarchy in a tree-like format, useful for debugging.
-   **Parameters:**
    -   `level` (int): The current indentation level (internal use).
-   **Returns:** (str) A multi-line string visualizing the folder structure.

### `__repr__(self)`

-   **Purpose:** Provides a concise string representation of the `FolderInfo` object.
-   **Returns:** (str) A string showing the folder name, target status, and the number of items in its contents (e.g., `FolderInfo(name='Documents', is_target=True, items=15)`).