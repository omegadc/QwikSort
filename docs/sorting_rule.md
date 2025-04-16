## Overview

The `SortingRule` class acts as a container that pairs a `Condition` object with an `Action` object. It represents a single, complete rule within a `Ruleset`: "If a file meets *this condition*, then perform *this action*."

## Class: `SortingRule`

Encapsulates a condition-action pair.

### `__init__(self, condition, action)`

-   **Purpose:** Constructs a `SortingRule` object.
-   **Parameters:**
    -   `condition` (Condition): The condition object that determines if the rule applies to a file.
    -   `action` (Action): The action object to be executed if the condition is met.
-   **Raises:** `ValueError` if `condition` is not a `Condition` instance or if `action` is not an `Action` instance.

### `__str__(self)`

-   **Purpose:** Provides a human-readable string representation of the rule.
-   **Returns:** (str) A descriptive sentence summarizing the rule (e.g., "If file name contains report, move file here."). Uses `Condition.operation_to_string()`.

### `run_rule(self, file)`

-   **Purpose:** Evaluates the rule's condition against a file and executes the action if the condition is met.
-   **Parameters:**
    -   `file` (FileInfo): The file object to evaluate and potentially act upon.
-   **Details:** Calls `self.condition.check(file)`. If it returns `True`, it then calls `self.action.execute(file)`.
-   **Raises:** `ValueError` if `file` is not a `FileInfo` instance.
-   **Note:** While this method exists, the primary execution flow for rules typically happens within the `Ruleset.run_rules` method, which manages multiple rules and logging.

### `to_dict(self)` / `classmethod from_dict(cls, data)`

-   **Purpose:** Standard serialization and deserialization methods.
-   **Details:** Delegates the process to the `to_dict` and `from_dict` methods of the contained `Condition` and `Action` objects. Ensures that the necessary classes (`Condition`, `Action`) are imported correctly during deserialization.