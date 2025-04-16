# Backend Documentation: `app_state.py`

## Overview

The `AppState` class is intended to serve as a central container for holding the application's current runtime state. This typically includes references to loaded rulesets, the currently selected target directory, and potentially other UI or configuration states.

**Note:** The provided implementation is minimal and primarily acts as a placeholder structure.

## Class: `AppState`

Manages the overall application state.

### `__init__(self)`

-   **Purpose:** Initializes the application state container.
-   **Details:** Sets up initial (likely empty or default) values for state variables. In the provided code:
    -   `self.rulesets` (dict): Intended to store the loaded `Ruleset` objects, possibly keyed by folder path or another identifier. Initialized as an empty dictionary.
    -   `self.target_directory` (None): Intended to hold a `FolderInfo` object representing the main directory selected by the user for scanning and sorting. Initialized as `None`.
    -   `self.selected_folder` (None): Possibly intended to hold a reference to a `FolderInfo` object currently selected or focused in the UI (which might be the `target_directory` or a subfolder). Initialized as `None`.

## Usage Context

While the implementation is basic, this class would typically be instantiated once when the application starts. Other parts of the application (UI controllers, backend services) would interact with this instance to access or modify the current state, such as:
-   Loading rulesets from a file and storing them in `self.rulesets`.
-   Scanning a user-selected directory and storing the resulting `FolderInfo` in `self.target_directory`.
-   Updating `self.selected_folder` based on user navigation in the UI.
-   Passing the `self.rulesets` and `self.target_directory` to `sorting_job.run_sorting_job` when a sort is initiated.