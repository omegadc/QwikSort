import copy
from dataclasses import dataclass
from typing import List, Optional
from Backend.action import Action
from Backend.file_info import FileInfo
from datetime import datetime

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

def saveRestorePoint():
    global restore_point
    if not undo_stack:
        print("No operations to save as restore point.")
        return
    # Make a deep copy of the last undo batch to save a restore point that is independent of future changes.
    restore_point = copy.deepcopy(undo_stack[-1])
    print(f"Restore point saved: {restore_point.description}")

def rollbackToRestorePoint():
    global restore_point
    if not restore_point:
        print("No restore point saved.")
        return

    print(f"Rolling back to restore point: {restore_point.description}")
    for record in reversed(restore_point.actions):
        try:
            record.reverse_action.execute(record.file)
        except Exception as e:
            print(f"Failed to restore {record.file.path}: {e}")