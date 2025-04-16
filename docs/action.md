## Overview

The `Action` class defines the file system operation (e.g., move, copy, rename, recycle) that should be performed on a file if its corresponding `Condition` is met. Each `SortingRule` contains an `Action` object specifying what to do with the matched file. It also includes logic for reversing actions, essential for the undo functionality.

## Class: `Action`

Represents a file operation to be executed.

### `__init__(self, type, final_folder = None, new_name = None)`

-   **Purpose:** Constructs an `Action` object.
-   **Parameters:**
    -   `type` (str): The type of action to perform. Supported types: `"move"`, `"copy"`, `"recycle"`, `"rename"`.
    -   `final_folder` (str, optional): The absolute path to the destination directory. Required for `"move"` and `"copy"` actions. Must be an existing directory.
    -   `new_name` (str, optional): The new base name (without extension) for the file. Required for the `"rename"` action.
-   **Raises:** `TypeError` if `final_folder` is provided but is not an existing directory.

### `staticmethod verify(file)`

-   **Purpose:** A helper method to ensure the input is a `FileInfo` object and that the corresponding file exists on the file system before attempting an operation.
-   **Parameters:**
    -   `file` (FileInfo): The file object to verify.
-   **Raises:**
    -   `TypeError`: If `file` is not a `FileInfo` instance.
    -   `FileNotFoundError`: If the file specified by `file.path` does not exist.

### `get_target_path(self, file)`

-   **Purpose:** Calculates the destination path or identifier for a file based on the action type.
-   **Parameters:**
    -   `file` (FileInfo): The file object the action would apply to.
-   **Returns:** (str) The calculated target path. For `"move"`/`"copy"`, it's the path in `final_folder`. For `"rename"`, it's the path with the new name in the original directory. For `"recycle"`, it returns the string `"Recycled"`. Returns `"Unknown"` for unsupported types.

### `get_reverse_action(self, file: FileInfo) -> 'Action'`

-   **Purpose:** Creates an `Action` object that can reverse the effect of the current action. This is crucial for the undo mechanism.
-   **Parameters:**
    -   `file` (FileInfo): The *original* state of the file *before* the forward action was executed. This is important for determining the reverse parameters (e.g., the original directory for a move).
-   **Returns:** (Action) A new `Action` object representing the reverse operation.
    -   `move` -> `move` (back to the original directory)
    -   `copy` -> `recycle` (delete the created copy)
    -   `rename` -> `rename` (back to the original name)
    -   `recycle` -> Raises `NotImplementedError` (reversing recycle bin actions is not supported directly by this class).
-   **Raises:**
    -   `NotImplementedError`: For reversing `"recycle"`.
    -   `ValueError`: If the action type has no defined reverse action.

### `move_file(self, file)`

-   **Purpose:** Moves the specified file to the `final_folder`.
-   **Parameters:**
    -   `file` (FileInfo): The file to move.
-   **Details:** Uses `shutil.move`. Checks if the destination already exists; if so, the operation is skipped to prevent accidental overwrites. Includes basic error catching and printing.

### `copy_file(self, file)`

-   **Purpose:** Copies the specified file to the `final_folder`.
-   **Parameters:**
    -   `file` (FileInfo): The file to copy.
-   **Details:** Uses `shutil.copy`. Currently raises `NotImplementedError` if the destination file already exists, as overwrite logic is not implemented.

### `rename_file(self, file)`

-   **Purpose:** Renames the specified file using `self.new_name`.
-   **Parameters:**
    -   `file` (FileInfo): The file to rename.
-   **Details:** Uses `os.rename`. Calculates the new path within the same directory. Currently raises `NotImplementedError` if a file with the new name already exists.
-   **Raises:** `ValueError` if `self.new_name` was not provided during initialization.

### `recycle_file(self, file)`

-   **Purpose:** Moves the specified file to the system's Recycle Bin (or equivalent).
-   **Parameters:**
    -   `file` (FileInfo): The file to recycle.
-   **Details:** Uses the `send2trash` library. Resolves the path using `pathlib.Path` for robustness.

### `log_action(self, file, logger)`

-   **Purpose:** Writes a log entry detailing the action performed.
-   **Parameters:**
    -   `file` (FileInfo): The file object *before* the action was executed (to log the original path).
    -   `logger`: An open file object or similar stream writer to write the log entry to.
-   **Details:** Calculates the target path using `get_target_path`. Formats a log string including a timestamp, action type, original path, and target path. Writes and flushes the log entry.

### `execute(self, file, logger=None)`

-   **Purpose:** The main public method to execute the defined action on a file.
-   **Parameters:**
    -   `file` (FileInfo): The file object to perform the action on.
    -   `logger` (optional): An open log file object. If provided, `log_action` will be called.
-   **Returns:** The result from the specific action function (e.g., `move_file`), though typically `None`.
-   **Details:** Dispatches to the appropriate internal action method (`move_file`, `copy_file`, etc.) based on `self.type`. Handles logging via `log_action`. **Crucially, it updates the `file.path` and `file.name` attributes of the passed `FileInfo` object in-place to reflect the result of the action.**
-   **Raises:** `ValueError` if `self.type` is invalid.

### `to_dict(self)` / `classmethod from_dict(cls, data)`

-   **Purpose:** Standard serialization and deserialization methods for saving/loading `Action` objects.
-   **Details:** Handle the `type`, `final_folder`, and `new_name` attributes.

### `__repr__(self)`

-   **Purpose:** Provides a detailed string representation of the `Action` object, useful for debugging.
-   **Returns:** (str) A string showing the type and any relevant parameters (`final_folder`, `new_name`).