from backend.condition import Condition
from backend.action import Action
from backend.folder_info import FolderInfo
from backend.file_info import FileInfo

class SortingRule:
    def __init__(self, condition, action):
        if not isinstance(condition, Condition):
            raise ValueError("SortingRule must take a Condition object")
        if not isinstance(action, Action):
            raise ValueError("SortingRule must take an Action object")

        self.condition = condition
        self.action = action

    def __str__(self):
        condition_type = self.condition.type

        if condition_type == "date_created":
            condition_type = "date created"
        elif condition_type == "date_modified":
            condition_type = "date modified"

        return f"If file {condition_type} {self.condition.operation_to_string()} {self.condition.value}, move file here."
    
    def run_rule(self, file):
        if not isinstance(file, FileInfo):
            raise ValueError("run_rule must take a FileInfo object")
        
        if self.condition.check(file):
            self.action.execute(file)
    
    def to_dict(self):
        return {
            "condition": self.condition.to_dict(),
            "action": self.action.to_dict()
        }

    @classmethod
    def from_dict(cls, data):
        from backend.condition import Condition
        from backend.action import Action
        return cls(
            condition=Condition.from_dict(data["condition"]),
            action=Action.from_dict(data["action"])
        )
    
