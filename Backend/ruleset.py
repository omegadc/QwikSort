from Backend.sorting_rule import SortingRule
from Backend.folder_info import FolderInfo
from Backend.file_info import FileInfo
from Backend.rollback import ActionRecord

class Ruleset:
    def __init__(self, folder, match_all=False):
        if not isinstance(folder, FolderInfo):
            raise ValueError("Ruleset must take a FolderInfo object for the assigned folder")

        self.sorting_rules = []
        self.folder = folder
        self.match_all = match_all

    def run_rules(self, file, logger=None):
        records = []

        if not isinstance(file, FileInfo):
            raise ValueError("run_rules must take a FileInfo object")

        if self.match_all:
            if all(rule.condition.check(file) for rule in self.sorting_rules):
                # Ensure all actions are the same type
                action_types = [type(rule.action) for rule in self.sorting_rules]
                if len(set(action_types)) != 1:
                    raise ValueError("All rules must have the same action type when match_all is enabled.")

                # Execute only the final rule's action
                final_rule = self.sorting_rules[-1]
                action = final_rule.action
                new_path = action.get_target_path(file)
                if action.type != "recycle":
                    reverse_action = action.get_reverse_action(file)

                if logger:
                    action.execute(file, logger)
                else:
                    action.execute(file)

                if action.type != "recycle":
                    record = ActionRecord(
                        forward_action=action,
                        reverse_action=reverse_action,
                        file=file,
                        result_path=new_path
                    )
                    records.append(record)
        else:
            for rule in self.sorting_rules:
                if rule.condition.check(file):
                    action = rule.action
                    new_path = action.get_target_path(file)
                    if action.type != "recycle":
                        reverse_action = action.get_reverse_action(file)

                    if logger:
                        action.execute(file, logger)
                    else:
                        action.execute(file)
                    if action.type != "recycle":
                        record = ActionRecord(
                            forward_action=action,
                            reverse_action=reverse_action,
                            file=file,
                            result_path=new_path
                        )
                        records.append(record)
                    break  # Stop after the first match

        return records

    def add_rule(self, rule):
        if not isinstance(rule, SortingRule):
            raise ValueError("add_rule must take a SortingRule object")
        
        self.sorting_rules.append(rule)
    
    def delete_rule(self, rule):
        if not isinstance(rule, SortingRule):
            raise ValueError("delete_rule must take a SortingRule object.")
        try:
            self.sorting_rules.remove(rule)
        except ValueError:
            raise ValueError("The rule does not exist in the ruleset.")
    
    @classmethod
    def from_rules(cls, folder, rules):
        instance = cls(folder)
        instance.sorting_rules = rules
        return instance
    
    def to_dict(self):
        return {
            "folder": self.folder.path,
            "match_all": self.match_all,
            "rules": [rule.to_dict() for rule in self.sorting_rules]
        }

    @classmethod
    def from_dict(cls, data):
        folder = FolderInfo.from_path(
            folder_path=data["folder"],
            is_target=False 
        )
        ruleset = cls(folder, match_all=data["match_all"])
        ruleset.sorting_rules = [SortingRule.from_dict(rule) for rule in data["rules"]]
        return ruleset

    
    def __repr__(self):
        return f"<Ruleset for {self.folder.name} with {len(self.sorting_rules)} rules>"