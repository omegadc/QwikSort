from Backend.condition import Condition
from Backend.action import Action
from Backend.folder_info import FolderInfo
from Backend.file_info import FileInfo

class SortingRule:
    def __init__(self, condition, action):
        if not isinstance(condition, Condition):
            raise ValueError("SortingRule must take a Condition object")
        if not isinstance(action, Action):
            raise ValueError("SortingRule must take an Action object")

        self.condition = condition
        self.action = action
            
    
    def runRule(self, file):
        if not isinstance(file, FileInfo):
            raise ValueError("runRule must take a FileInfo object")
        
        if self.condition.check(file):
            self.action.execute(file)