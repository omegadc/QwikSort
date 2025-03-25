import os
from datetime import datetime
from file_info import FileInfo
from folder_info import FolderInfo

from sorting_rule import SortingRule
from ruleset import Ruleset
from condition import Condition
from action import Action

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

def main():
    # Define the target directory
    target_directory = r"C:\Users\Reggie\Files\Documents\Code\Python\QwikSortTestFolders\perf_test_data - Copy"
    target = FolderInfo.fromPath(target_directory, True)

    # Create some rulesets

    photosAction = Action("move", os.path.join(target_directory, "Photos"))
    photosRuleset = Ruleset.fromRules(target, [ 
        SortingRule(Condition("extension", "==", ".png"), photosAction),
        SortingRule(Condition("extension", "==", ".jpg"), photosAction),
        SortingRule(Condition("name", "contains", "photo"), photosAction)
    ])

    videosAction = Action("move", os.path.join(target_directory, "Videos"))
    videosRuleset = Ruleset.fromRules(target, [ 
        SortingRule(Condition("extension", "==", ".mp4"), videosAction),
        SortingRule(Condition("name", "contains", "video"), videosAction)
    ])

    rulesets = [photosRuleset, videosRuleset]

    # Run the job with the created rulesets on the target folder
    runSortingJob(rulesets, target)

if __name__ == "__main__":
    main()