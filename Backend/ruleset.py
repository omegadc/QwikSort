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

        matching_rules = []

        if self.match_all:
            if all(rule.condition.check(file) for rule in self.sortingRules):
                matching_rules = self.sortingRules
        else:
            for rule in self.sortingRules:
                if rule.condition.check(file):
                    matching_rules.append(rule)
                    break

        for rule in matching_rules:
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
    
    def __repr__(self):
        return f"<Ruleset for {self.folder.name} with {len(self.sortingRules)} rules>"