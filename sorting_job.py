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


def runSortingJob(rulesets, target_folder, log_dir="logs"):
    if not isinstance(target_folder, FolderInfo):
        raise ValueError("Target folder must be a valid FolderInfo object.")

    log_file = createLogFile(log_dir)

    try:
        for filename in os.listdir(target_folder):
            file_path = os.path.join(target_folder, filename)

            if os.path.isfile(file_path):
                file_info = FileInfo.fromPath(file_path)

                for ruleset in rulesets:
                    ruleset.runRules(file_info, logger=log_file)
    finally:
        log_file.close()

# TODO: Finish logging functionality, edit action.py accordingly
