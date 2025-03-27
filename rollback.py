from dataclasses import dataclass
from typing import List, Optional
from action import Action
from file_info import FileInfo
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
restore_point: Optional[UndoBatch] = None # optional snapshot


def recordBatch(file_actions: List[tuple], description: str):
    batch = UndoBatch(timestamp=datetime.now(), description=description, actions=[])

    for action, file, result_path in file_actions:
        reverse_action = action.getReverseAction(file)
        record = ActionRecord(
            forward_action=action,
            reverse_action=reverse_action,
            file=file,
            result_path=result_path
        )
        batch.actions.append(record)

    undo_stack.append(batch)

    if len(undo_stack) > MAX_UNDO:
        undo_stack.pop(0)

def perform_sort_and_record(files: List[FileInfo], action: Action, logger=None, description="Sort Operation"):
    records = []

    for file in files:
        original_path = file.path
        new_path = action.get_target_path(file)

        action.execute(file, logger=logger)

        reverse_action = action.get_reverse_action(file, new_path)

        record = ActionRecord(
            forward_action=action,
            reverse_action=reverse_action,
            file=file,
            original_path=original_path,
            new_path=new_path
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
    restore_point = undo_stack[-1]
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

