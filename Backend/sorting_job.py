import os
import time
import Backend.rollback
from datetime import datetime

from Backend.file_info import FileInfo
from Backend.folder_info import FolderInfo
from Backend.sorting_rule import SortingRule
from Backend.ruleset import Ruleset
from Backend.condition import Condition
from Backend.action import Action

def createLogFile(log_dir="logs"):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    log_path = os.path.join(base_dir, log_dir)

    if not os.path.exists(log_path):
        os.makedirs(log_path)

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    full_log_path = os.path.join(log_path, f"sorting_log_{timestamp}.txt")
    return open(full_log_path, "a") # Caller is responsible for closing log file

# Helper function to flatten a folder structure
def getAllFiles(folder):
    for item in folder.contents:
        if isinstance(item, FileInfo):
            yield item
        elif isinstance(item, FolderInfo):
            yield from getAllFiles(item)

def runSortingJob(rulesets, target_folder, log_dir="logs", description="Sorting Job"):
    if not isinstance(target_folder, FolderInfo):
        raise ValueError("Target folder must be a valid FolderInfo object.")

    log_file = createLogFile(log_dir)
    all_files = list(getAllFiles(target_folder))
    all_records = []

    try:
        for file in all_files:
            for _, ruleset in rulesets.items():
                records = ruleset.runRules(file, logger=log_file)
                all_records.extend(records)
                if records:
                    break
    finally:
        log_file.close()
    
    if all_records:
        Backend.rollback.recordBatch(all_records, description)

def main():
    # Define the target directory
    target_directory = r"C:\Users\Reggie\Files\Documents\Code\Python\QwikSortTestFolders\testing"
    target = FolderInfo.fromPath(target_directory, True)

    # Create some rulesets

    photosAction = Action("move", os.path.join(target_directory, "Photos"))
    photosRuleset = Ruleset.fromRules(target, [ 
        SortingRule(Condition("extension", "==", ".png"), photosAction),
        SortingRule(Condition("extension", "==", ".jpg"), photosAction),
        SortingRule(Condition("name", "includes", "photo"), photosAction)
    ])

    videosAction = Action("move", os.path.join(target_directory, "Videos"))
    videosRuleset = Ruleset.fromRules(target, [ 
        SortingRule(Condition("extension", "==", ".mp4"), videosAction),
        SortingRule(Condition("name", "includes", "video"), videosAction)
    ])

    rulesets = [photosRuleset, videosRuleset]

    # Run the job with the created rulesets on the target folder
    runSortingJob(rulesets, target, description="Test sort")

    # Undo the changes in 10 seconds
    print("------------------")
    time.sleep(10)

    Backend.rollback.undoLast()

if __name__ == "__main__":
    main()