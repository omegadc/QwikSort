## Overview

The `rollback` module provides functionality for undoing file operations performed during sorting jobs and for attempting to restore a directory's state to a previously saved snapshot. It maintains a limited history of actions performed.

## Data Structures

### `@dataclass ActionRecord`

-   **Purpose:** Stores the details of a single file operation that was executed, including how to reverse it.
-   **Attributes:**
    -   `forward_action` (Action): The `Action` object that was executed.
    -   `reverse_action` (Action): The `Action` object that can undo the `forward_action`.
    -   `file` (FileInfo): The `FileInfo` object representing the file *after* the `forward_action` was executed (its path/name reflects the state post-action). Note: The `reverse_action` needs to operate correctly on this potentially modified `FileInfo` state.
    -   `result_path` (str): The path the file ended up at after the `forward_action`.

### `@dataclass UndoBatch`

-   **Purpose:** Groups multiple `ActionRecord` objects from a single sorting job or operation into one undoable unit.
-   **Attributes:**
    -   `description` (str): A user-friendly description of the operation batch (e.g., "Sorting Job on Downloads").
    -   `timestamp` (datetime): When the batch was created/recorded.
    -   `actions` (List[ActionRecord]): A list of the individual actions performed in this batch.

## Global State

### `undo_stack: List[UndoBatch]`

-   A list acting as a stack holding the most recent `UndoBatch` objects.

### `MAX_UNDO = 5`

-   The maximum number of `UndoBatch` objects to keep in the `undo_stack`. Older batches are discarded.

### `folder_restore_point: Optional[FolderInfo]`

-   Stores a deep copy of a `FolderInfo` object, captured via `save_restore_point`, representing a snapshot of the directory state at a specific time. Used by `rollback_to_restore_point`.

## Functions

### `record_batch(action_records: List[ActionRecord], description: str)`

-   **Purpose:** Creates an `UndoBatch` from a list of `ActionRecord`s generated during an operation (like `run_sorting_job`) and adds it to the `undo_stack`.
-   **Parameters:**
    -   `action_records` (List[ActionRecord]): The list of records for the completed operation.
    -   `description` (str): Description for the batch.
-   **Details:** Creates the `UndoBatch` with the current timestamp. Appends it to `undo_stack`. If the stack size exceeds `MAX_UNDO`, removes the oldest batch (FIFO).

### `undo_last()`

-   **Purpose:** Reverses the most recent operation recorded in the `undo_stack`.
-   **Details:**
    -   Checks if `undo_stack` is empty. If so, prints a message and returns.
    -   Pops the most recent `UndoBatch` from the stack.
    -   Iterates through the `actions` list of the batch *in reverse order*.
    -   For each `ActionRecord`, calls `record.reverse_action.execute(record.file)`. The `record.file` object (which reflects the state *after* the forward action) is passed to the reverse action's `execute` method.
    -   Prints success or failure messages for each reversal attempt. Catches exceptions during reversal.

### `save_restore_point(folder: FolderInfo)`

-   **Purpose:** Saves a snapshot of the current directory structure and file state for potential restoration later.
-   **Parameters:**
    -   `folder` (FolderInfo): The `FolderInfo` object (presumably representing the currently scanned target directory) to save.
-   **Details:** Performs a `copy.deepcopy` of the provided `folder` object and stores it in the global `folder_restore_point` variable. Overwrites any previous restore point.

### `find_file(file_name: str, start_dir: str) -> Optional[str]`

-   **Purpose:** Helper function to search recursively for a file by its full name (name + extension) starting from a given directory.
-   **Parameters:**
    -   `file_name` (str): The exact file name (e.g., `document.txt`) to search for.
    -   `start_dir` (str): The directory path to begin the search from.
-   **Returns:** (str | None) The full path to the first instance of the file found, or `None` if not found.
-   **Details:** Uses `os.walk`.

### `rollback_to_restore_point()`

-   **Purpose:** Attempts to restore the file system state to match the snapshot saved in `folder_restore_point`. **This is NOT a generic undo.** It specifically tries to move files back to their locations as recorded in the restore point.
-   **Details:**
    -   Checks if `folder_restore_point` exists.
    -   Defines nested helper functions `restore_file` and `restore_folder`.
    -   `restore_folder` recursively traverses the `folder_restore_point` structure.
    -   `restore_file` takes a `FileInfo` object (`snapshot_file`) from the restore point:
        -   Checks if a file already exists at the `snapshot_file.path`. If yes, it assumes the file is already correctly placed and does nothing.
        -   If the file is *not* at its snapshot location, it calls `find_file` to search for the file (using its name + extension) starting from the *parent directory* of the `folder_restore_point`'s path (`base_dir`).
        -   If `find_file` locates the file at a `current_location`:
            -   It creates a "move" `Action` targeting the original directory (`os.path.dirname(snapshot_file.path)`).
            -   It creates a *temporary* `FileInfo` object (`temp_file`) reflecting the file's `current_location` but otherwise copying data from `snapshot_file`.
            -   It executes the move action using this `temp_file`.
        -   If the file cannot be found via `find_file`, it prints a "Could not locate" message.
    -   Calls `restore_folder` on the root `folder_restore_point` to start the process.
-   **Limitations:** This function relies on finding files that may have moved. It doesn't handle file deletions, content changes, or files created *after* the restore point was saved. It primarily addresses files that were present in the snapshot but subsequently moved elsewhere within the searched `base_dir`. Its effectiveness depends heavily on the nature of the changes made since the restore point was saved.