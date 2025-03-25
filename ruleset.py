from sorting_rule import SortingRule
from folder_info import FolderInfo
from file_info import FileInfo

class Ruleset:
    def __init__(self, folder):
        if not isinstance(folder, FolderInfo):
            raise ValueError("Ruleset must take a FolderInfo object for the assigned folder")

        self.sortingRules = []
        self.folder = folder
            
    
    def runRules(self, file, logger=None):
        if not isinstance(file, FileInfo):
            raise ValueError("runRules must take a FileInfo object")
        
        for rule in self.sortingRules:
            if rule.condition.check(file):
                if logger:
                    rule.action.execute(file, logger)
                else:
                    rule.action.execute(file)  
    
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