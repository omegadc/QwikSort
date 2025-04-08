import copy
import os
from dataclasses import dataclass
from typing import List, Optional
from Backend.action import Action
from Backend.folder_info import FolderInfo
from Backend.file_info import FileInfo
from datetime import datetime

restore_point: Optional[FolderInfo] = None

@dataclass
class ActionRecord:
    forward_action: Action
    reverse_action: Action
    file: FileInfo
    result_path: str

@dataclass
class UndoBatch:
    description: str
    timestamp: datetime
    actions: List[ActionRecord]

MAX_UNDO = 5
undo_stack: List[UndoBatch] = []
restore_point: Optional[UndoBatch] = None

def recordBatch(action_records: List[ActionRecord], description: str):
    batch = UndoBatch(
        timestamp=datetime.now(),
        description=description,
        actions=action_records
    )
    undo_stack.append(batch)

    if len(undo_stack) > MAX_UNDO:
        undo_stack.pop(0)

def performSortAndRecord(files: List[FileInfo], action: Action, logger=None, description="Sort Operation"):
    records = []

    for file in files:
        new_path = action.get_target_path(file)
        reverse_action = action.get_reverse_action(file, new_path)
        action.execute(file, logger=logger)

        record = ActionRecord(
            forward_action=action,
            reverse_action=reverse_action,
            file=file,
            result_path=new_path
        )
        records.append(record)

    recordBatch(records, description)

def undoLast():
    if not undo_stack:
        print("No operations to undo.")
        return

    batch = undo_stack.pop()
    print(f"Undoing: {batch.description}")

    for record in reversed(batch.actions):
        try:
            record.reverse_action.execute(record.file)
            print(f"Undid: {record.forward_action.type} -> {record.file.path}")
        except Exception as e:
            print(f"Failed to undo {record.file.path}: {e}")

def saveRestorePoint(folder: FolderInfo):
    """
    Save a deep copy of the current FolderInfo snapshot as a restore point.
    
    Args:
        folder (FolderInfo): A snapshot of the current directory layout.
    """
    global restore_point
    restore_point = copy.deepcopy(folder)
    print(f"Restore point saved for folder: {folder.path}")

def find_file(file_name: str, start_dir: str) -> Optional[str]:
    """
    Recursively search for a file by its name starting from start_dir.
    
    Args:
        file_name (str): The name of the file to search for.
        start_dir (str): The directory from which to start the search.
        
    Returns:
        Optional[str]: The full path of the found file, or None if not found.
    """
    for root, dirs, files in os.walk(start_dir):
        if file_name in files:
            return os.path.join(root, file_name)
    return None

def rollbackToRestorePoint():
    """
    Roll back the current directory layout to match the saved restore point.
    
    For each file in the restore point snapshot, if the file is not found at its
    original (restore point) location, this function searches for the file starting the
    restore point folder, and if found, uses an Action of type 'move' to return it 
    to its original location.
    """
    if not restore_point:
        print("No restore point saved.")
        return

    print(f"Rolling back to restore point at folder: {restore_point.path}")

    def restore_file(snapshot_file: FileInfo):
        # Check if the file already exists in the expected (snapshot) location.
        if os.path.exists(snapshot_file.path):
            return  # The file is already in its restore location.

        base_dir = os.path.dirname(restore_point.path)
        full_file_name = snapshot_file.name + snapshot_file.extension
        current_location = find_file(full_file_name, base_dir)

        if current_location:
            # Move the file back to its original location
            action = Action("move", finalFolder=os.path.dirname(snapshot_file.path))

            # Create a temporary FileInfo instance that reflects the current location.
            temp_file = copy.deepcopy(snapshot_file)
            temp_file.path = current_location

            try:
                action.execute(temp_file)
                print(f"Restored {snapshot_file.name} to {snapshot_file.path}")
            except Exception as e:
                print(f"Failed to restore {snapshot_file.name}: {e}")
        else:
            print(f"Could not locate file {snapshot_file.name} for rollback.")

    def restore_folder(folder: FolderInfo):
        for item in folder.contents:
            if isinstance(item, FolderInfo):
                restore_folder(item)
            else:
                restore_file(item)

    restore_folder(restore_point)
