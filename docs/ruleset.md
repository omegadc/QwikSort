## Overview

The `Ruleset` class manages a collection of `SortingRule` objects associated with a specific folder. It defines how rules are applied to files within the user's current target directory (either applying the first matching rule or requiring all rules to match) and orchestrates the execution of those rules.

## Class: `Ruleset`

Manages and executes a set of sorting rules for an associated folder.

### `__init__(self, folder, match_all=False)`

-   **Purpose:** Constructs a `Ruleset` object.
-   **Parameters:**
    -   `folder` (FolderInfo): The `FolderInfo` object representing the folder to which this ruleset applies. This association is primarily conceptual; the ruleset itself doesn't directly operate *on* the folder object but uses it for context (like its path).
    -   `match_all` (bool): If `False` (default), the first `SortingRule` whose condition matches the file will have its action executed, and processing stops for that file within this ruleset. If `True`, *all* conditions in the ruleset must match the file for *any* action to occur. If all match, only the action from the *last* rule in the list is executed.
-   **Raises:** `ValueError` if the provided `folder` is not a `FolderInfo` instance.

### `run_rules(self, file, logger=None)`

-   **Purpose:** Applies the rules within this ruleset to a single file.
-   **Parameters:**
    -   `file` (FileInfo): The file object to process.
    -   `logger` (optional): An open file object for logging actions.
-   **Returns:** (list[ActionRecord]) A list of `ActionRecord` objects representing the actions performed and their corresponding reverse actions for use in undo operations. This list will be empty if no rules matched or if the action was of type "recycle" (which doesn't generate a reversible record).
-   **Details:**
    -   Verifies `file` is a `FileInfo` instance.
    -   **If `match_all` is `False`:** Iterates through `self.sorting_rules`. For the first rule where `rule.condition.check(file)` is `True`, it retrieves the `rule.action`, calculates the target path, gets the reverse action (if not "recycle"), executes the action (passing the logger), creates an `ActionRecord`, adds it to the `records` list, and breaks the loop.
    -   **If `match_all` is `True`:** Checks if *all* rule conditions match the file using `all(rule.condition.check(file) for rule in self.sorting_rules)`. If they do, it validates that all rules have the same action type (important constraint). It then takes the action from the *last* rule, calculates paths, gets the reverse action, executes the action, logs it, creates an `ActionRecord`, and adds it to the `records` list.
-   **Raises:**
    -   `ValueError`: If `file` is not a `FileInfo` instance.
    -   `ValueError`: If `match_all` is `True` but the rules have different action types.

### `add_rule(self, rule)`

-   **Purpose:** Adds a `SortingRule` to the ruleset's list.
-   **Parameters:**
    -   `rule` (SortingRule): The rule to add.
-   **Raises:** `ValueError` if `rule` is not a `SortingRule` instance.

### `delete_rule(self, rule)`

-   **Purpose:** Removes a specific `SortingRule` from the ruleset's list.
-   **Parameters:**
    -   `rule` (SortingRule): The rule object to remove.
-   **Raises:**
    -   `ValueError`: If `rule` is not a `SortingRule` instance.
    -   `ValueError`: If the specified `rule` object is not found in the list.

### `classmethod from_rules(cls, folder, rules)`

-   **Purpose:** Alternative constructor to create a `Ruleset` instance with a pre-defined list of rules.
-   **Parameters:**
    -   `folder` (FolderInfo): The associated folder.
    -   `rules` (list[SortingRule]): The list of sorting rules.
-   **Returns:** (Ruleset) A new `Ruleset` instance.

### `to_dict(self)` / `classmethod from_dict(cls, data)`

-   **Purpose:** Standard serialization and deserialization methods.
-   **Details:**
    -   `to_dict`: Saves the associated folder's path (`self.folder.path`), the `match_all` flag, and a list of serialized rules (using `rule.to_dict()`).
    -   `from_dict`: Reconstructs the `Ruleset`. It uses `FolderInfo.from_path` to create a minimal `FolderInfo` object from the saved path (note: this doesn't rescan the folder contents, it just uses the path for context) and deserializes the rules using `SortingRule.from_dict`.

### `__repr__(self)`

-   **Purpose:** Provides a concise string representation of the `Ruleset`.
-   **Returns:** (str) A string indicating the associated folder and the number of rules (e.g., `<Ruleset for Documents with 5 rules>`).