## Overview

The `FileInfo` class serves as a fundamental data structure within the QwikSort backend. It encapsulates all relevant metadata for a single file detected within the target directory or its subdirectories. This object-oriented representation allows for consistent handling and querying of file properties throughout the sorting process.

## Class: `FileInfo`

Represents a file and its associated metadata.

### `__init__(self, name, extension, path, size, dateCreated, dateModified)`

-   **Purpose:** Constructs a `FileInfo` object.
-   **Parameters:**
    -   `name` (str): The base name of the file (without extension).
    -   `extension` (str): The file extension (including the leading dot, e.g., `.txt`).
    -   `path` (str): The absolute path to the file.
    -   `size` (int): The size of the file in bytes.
    -   `dateCreated` (datetime): The creation timestamp of the file.
    -   `dateModified` (datetime): The last modification timestamp of the file.
-   **Usage:** Typically instantiated via the `from_path` class method rather than direct constructor calls.

### `staticmethod get_metadata(filePath)`

-   **Purpose:** Retrieves file metadata directly from the file system.
-   **Parameters:**
    -   `filePath` (str): The absolute path to the file.
-   **Returns:** (dict) A dictionary containing the file's metadata (`path`, `name`, `extension`, `size`, `dateModified`, `dateCreated`).
-   **Details:** Uses `os.path.splitext`, `os.path.basename`, `os.path.getsize`, `os.path.getmtime`, `os.path.getctime`, and `datetime.fromtimestamp` to gather the information.

### `classmethod from_path(cls, filePath)`

-   **Purpose:** Factory method to create a `FileInfo` instance from a given file path.
-   **Parameters:**
    -   `filePath` (str): The absolute path to the file.
-   **Returns:** (FileInfo) A new `FileInfo` object populated with metadata retrieved from the specified path.
-   **Details:** Calls `get_metadata` internally and uses the returned dictionary to instantiate the class. This is the preferred way to create `FileInfo` objects.

### `__repr__(self)`

-   **Purpose:** Provides a concise string representation of the `FileInfo` object, primarily for debugging.
-   **Returns:** (str) A string showing the file name and size (e.g., `FileInfo(name='document', size=1024B)`).