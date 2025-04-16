import os
import time
import backend.rollback
from datetime import datetime

from backend.file_info import FileInfo
from backend.folder_info import FolderInfo
from backend.sorting_rule import SortingRule
from backend.ruleset import Ruleset
from backend.condition import Condition
from backend.action import Action

def create_log_file(log_dir="logs"):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    log_path = os.path.join(base_dir, log_dir)

    if not os.path.exists(log_path):
        os.makedirs(log_path)

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    full_log_path = os.path.join(log_path, f"sorting_log_{timestamp}.txt")
    return open(full_log_path, "a") # Caller is responsible for closing log file

# Helper function to flatten a folder structure
def get_all_files(folder):
    for item in folder.contents:
        if isinstance(item, FileInfo):
            yield item
        elif isinstance(item, FolderInfo):
            yield from get_all_files(item)

def run_sorting_job(rulesets, target_folder, log_dir="logs", description="Sorting Job"):
    if not isinstance(target_folder, FolderInfo):
        raise ValueError("Target folder must be a valid FolderInfo object.")

    log_file = create_log_file(log_dir)
    all_files = list(get_all_files(target_folder))
    all_records = []

    try:
        for file in all_files:
            for _, ruleset in rulesets.items():
                records = ruleset.run_rules(file, logger=log_file)
                all_records.extend(records)
                if records:
                    break
    finally:
        log_file.close()
    
    if all_records:
        backend.rollback.record_batch(all_records, description)