## Overview

The `Condition` class defines the criteria used to evaluate files during the sorting process. Each `SortingRule` contains a `Condition` object, which specifies what property of a file (e.g., name, size, date) should be checked, how it should be compared (e.g., equals, contains, greater than), and against what value.

## Class: `Condition`

Represents a specific condition to check against a `FileInfo` object.

### `operators` (dict)

-   **Purpose:** A class-level dictionary mapping string representations of operators (e.g., `>`, `includes`) to their corresponding function implementations (primarily from the `operator` module or lambda functions).
-   **Supported Operators:** `>` (greater than), `<` (less than), `>=` (greater or equal), `<=` (less or equal), `==` (equal), `!=` (not equal), `includes` (substring check, case-insensitive), `excludes` (negative substring check, case-insensitive).

### `__init__(self, type, operation, value)`

-   **Purpose:** Constructs a `Condition` object.
-   **Parameters:**
    -   `type` (str): The attribute of the `FileInfo` object to check. Supported types: `"name"`, `"extension"`, `"size"`, `"dateCreated"`, `"dateModified"`.
    -   `operation` (str): The comparison operator to use (must be a key in `Condition.operators`).
    -   `value`: The value to compare the file attribute against. The required type depends on the `type` parameter (e.g., `str` for name/extension, `int` or `float` for size, `datetime` for dates).

### `staticmethod verify(file)`

-   **Purpose:** A helper method to ensure that the object passed to check methods is indeed a `FileInfo` instance.
-   **Raises:** `TypeError` if the input `file` is not a `FileInfo` object.

### `staticmethod evaluate(left, op, right)`

-   **Purpose:** A helper method to perform the actual comparison between a file attribute and the condition's value using the specified operator.
-   **Parameters:**
    -   `left`: The value from the `FileInfo` object.
    -   `op` (str): The operator string (e.g., `">"`).
    -   `right`: The value from the `Condition` object.
-   **Returns:** (bool) The result of the comparison.
-   **Details:** Looks up the operator function in `Condition.operators`. Handles case-insensitive comparison for strings.
-   **Raises:** `ValueError` if `op` is not a supported operator.

### `operation_to_string(self)`

-   **Purpose:** Provides a human-readable description of the condition's operator.
-   **Returns:** (str) A string like "is greater than", "contains", etc.

### `check_name(self, file)` / `check_extension(self, file)` / `check_size(self, file)` / `check_creation(self, file)` / `check_modified(self, file)`

-   **Purpose:** Internal methods dedicated to checking a specific file attribute (`name`, `extension`, `size`, `dateCreated`, `dateModified`).
-   **Parameters:**
    -   `file` (FileInfo): The file object to evaluate.
-   **Returns:** (bool) The result of the specific condition check.
-   **Details:** Each method first calls `verify`, then performs type checking on `self.value` appropriate for the attribute, and finally calls `evaluate` to get the comparison result.
-   **Raises:** `ValueError` if `self.value` has an incorrect type for the check being performed.

### `check(self, file)`

-   **Purpose:** The main public method to evaluate the condition against a given file.
-   **Parameters:**
    -   `file` (FileInfo): The file object to evaluate.
-   **Returns:** (bool) `True` if the file meets the condition, `False` otherwise.
-   **Details:** Dispatches the call to the appropriate internal `check_*` method based on `self.type`.
-   **Raises:** `ValueError` if `self.type` is invalid.

### `to_dict(self)`

-   **Purpose:** Serializes the `Condition` object into a dictionary format suitable for saving (e.g., to JSON).
-   **Returns:** (dict) A dictionary representation of the condition. `datetime` values are converted to ISO format strings.

### `classmethod from_dict(cls, data)`

-   **Purpose:** Deserializes a dictionary (presumably loaded from storage) back into a `Condition` object.
-   **Parameters:**
    -   `data` (dict): The dictionary representation of the condition.
-   **Returns:** (Condition) A new `Condition` instance.
-   **Details:** Handles the conversion of ISO format date strings back into `datetime` objects for date-related condition types.

### `__repr__(self)`

-   **Purpose:** Provides a detailed string representation of the `Condition` object, useful for debugging.
-   **Returns:** (str) A string showing the type, operation, and value.