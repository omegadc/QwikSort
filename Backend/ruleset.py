from Backend.sorting_rule import SortingRule
from Backend.folder_info import FolderInfo
from Backend.file_info import FileInfo
from Backend.rollback import ActionRecord

class Ruleset:
    def __init__(self, folder, match_all=False):
        if not isinstance(folder, FolderInfo):
            raise ValueError("Ruleset must take a FolderInfo object for the assigned folder")

        self.sortingRules = []
        self.folder = folder
        self.match_all = match_all

    def runRules(self, file, logger=None):
        records = []

        if not isinstance(file, FileInfo):
            raise ValueError("runRules must take a FileInfo object")

        if self.match_all:
            if all(rule.condition.check(file) for rule in self.sortingRules):
                # Ensure all actions are the same type
                action_types = [type(rule.action) for rule in self.sortingRules]
                if len(set(action_types)) != 1:
                    raise ValueError("All rules must have the same action type when match_all is enabled.")

                # Execute only the final rule's action
                final_rule = self.sortingRules[-1]
                action = final_rule.action
                new_path = action.getTargetPath(file)
                reverse_action = action.getReverseAction(file)

                if logger:
                    action.execute(file, logger)
                else:
                    action.execute(file)

                record = ActionRecord(
                    forward_action=action,
                    reverse_action=reverse_action,
                    file=file,
                    result_path=new_path
                )
                records.append(record)
        else:
            for rule in self.sortingRules:
                if rule.condition.check(file):
                    action = rule.action
                    new_path = action.getTargetPath(file)
                    reverse_action = action.getReverseAction(file)

                    if logger:
                        action.execute(file, logger)
                    else:
                        action.execute(file)

                    record = ActionRecord(
                        forward_action=action,
                        reverse_action=reverse_action,
                        file=file,
                        result_path=new_path
                    )
                    records.append(record)
                    break  # Stop after the first match

        return records

    def addRule(self, rule):
        if not isinstance(rule, SortingRule):
            raise ValueError("addRule must take a SortingRule object")
        
        self.sortingRules.append(rule)
    
    def deleteRule(self, rule):
        if not isinstance(rule, SortingRule):
            raise ValueError("deleteRule must take a SortingRule object.")
        try:
            self.sortingRules.remove(rule)
        except ValueError:
            raise ValueError("The rule does not exist in the ruleset.")
    
    @classmethod
    def fromRules(cls, folder, rules):
        instance = cls(folder)
        instance.sortingRules = rules
        return instance
    
    def to_dict(self):
        return {
            "folder": self.folder.path,
            "match_all": self.match_all,
            "rules": [rule.to_dict() for rule in self.sortingRules]
        }

    @classmethod
    def from_dict(cls, data):
        from Backend.folder_info import FolderInfo
        from Backend.sorting_rule import SortingRule

        folder = FolderInfo(data["folder"])
        ruleset = cls(folder, match_all=data["match_all"])
        ruleset.sortingRules = [SortingRule.from_dict(rule) for rule in data["rules"]]
        return ruleset

    
    def __repr__(self):
        return f"<Ruleset for {self.folder.name} with {len(self.sortingRules)} rules>"