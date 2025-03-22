from condition import Condition
from action import Action
from folder_info import FolderInfo
from file_info import FileInfo

class SortingRule:
    def __init__(self, condition, action, folder):
        if not isinstance(condition, Condition):
            raise ValueError("SortingRule must take a Condition object")
        if not isinstance(action, Action):
            raise ValueError("SortingRule must take an Action object")
        if not isinstance(folder, FolderInfo):
            raise ValueError("SortingRule must take a FolderInfo object for folder assignment")

        self.condition = condition
        self.action = action
        self.folder = folder
            
    
    def runRule(self, file):
        if not isinstance(file, FileInfo):
            raise ValueError("runRule must take a FileInfo object")
        
        if self.condition.check(file):
            self.action.execute(file)