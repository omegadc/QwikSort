import os
from datetime import datetime
from file_info import FileInfo
from folder_info import FolderInfo

def createLogFile(log_dir="logs"):
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    log_path = os.path.join(log_dir, f"sorting_log_{timestamp}.txt")
    return open(log_path, "a")  # Caller is responsible for closing log file

# Helper function to flatten a folder structure
def getAllFiles(folder):
    for item in folder.contents:
        if isinstance(item, FileInfo):
            yield item
        elif isinstance(item, FolderInfo):
            yield from getAllFiles(item)

def runSortingJob(rulesets, target_folder, log_dir="logs"):
    if not isinstance(target_folder, FolderInfo):
        raise ValueError("Target folder must be a valid FolderInfo object.")

    log_file = createLogFile(log_dir)
    all_files = list(getAllFiles(target_folder))

    try:
        for file in all_files:
            for ruleset in rulesets:
                ruleset.runRules(file, logger=log_file)

    finally:
        log_file.close()
