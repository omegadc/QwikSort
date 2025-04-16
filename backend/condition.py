from datetime import datetime
from backend.file_info import *
import operator

class Condition:
    operators = {
        ">": operator.gt,
        "<": operator.lt,
        ">=": operator.ge,
        "<=": operator.le,
        "==": operator.eq, 
        "!=": operator.ne,
        "includes": lambda a, b: b.lower() in a.lower(),
        "excludes": lambda a, b: b.lower() not in a.lower()
    }

    def __init__(self, type, operation, value):
        self.type = type
        self.operation = operation
        self.value = value
        self.functions = {
            "name": self.check_name,
            "extension": self.check_extension,
            "size": self.check_size,
            "dateCreated": self.check_creation,
            "dateModified": self.check_modified
        }

    # Helper function to verify if a file is of type FileInfo
    @staticmethod
    def verify(file):
        if not isinstance(file, FileInfo):
            raise TypeError("Condition only handles type FileInfo")
    
    # Helper function to evaluate a comparison using a string operator
    @staticmethod
    def evaluate(left, op, right):
        if op not in Condition.operators:
            raise ValueError(f"Invalid operator {op}")
        
        print(f"Evaluating: {left!r} {op} {right!r}")

        # Convert to strings
        if isinstance(left, str) and isinstance(right, str):
            left, right = left.lower(), right.lower()

        return Condition.operators[op](left, right)
    
    # Function to return the class operation to a string
    def operation_to_string(self):
        operation_map = {
            ">": "is greater than",
            "<": "is less than",
            ">=": "is greater or equal to",
            "<=": "is less or equal to",
            "==": "is equal to",
            "!=": "is not equal to",
            "includes": "contains",
            "excludes": "does not contain"
        }
        return operation_map.get(self.operation, f"Unknown operation: {self.operation}")
    
    # Function to compare value to file name
    def check_name(self, file):
        Condition.verify(file)

        if not isinstance(self.value, str):
            raise ValueError("Condition check of type \"name\" must take value type string")

        return Condition.evaluate(file.name, self.operation, self.value)
    
    # Function to compare value to file extension
    def check_extension(self, file):
        Condition.verify(file)

        if not isinstance(self.value, str):
            raise ValueError("Condition check of type \"extension\" must take value type string")

        return Condition.evaluate(file.extension, self.operation, self.value)

    # Function to compare value to file size
    def check_size(self, file):
        Condition.verify(file)

        if isinstance(self.value, int):
            self.value = float(self.value)

        if not isinstance(self.value, float):
            raise ValueError("Condition check of type \"size\" must take value type int or float")

        return Condition.evaluate(file.size, self.operation, self.value)

    # Function to compare value to file creation date
    def check_creation(self, file):
        Condition.verify(file)

        if not isinstance(self.value, datetime):
            raise ValueError("Condition check of type \"dateCreated\" must take value type datetime")

        return Condition.evaluate(file.dateCreated, self.operation, self.value)
    
    # Function to compare value to file modified date
    def check_modified(self, file):
        Condition.verify(file)

        if not isinstance(self.value, datetime):
            raise ValueError("Condition check of type \"dateModified\" must take value type datetime")
        
        return Condition.evaluate(file.dateModified, self.operation, self.value)

    # Primary function to check if a file meets the condition
    def check(self, file):
        if self.type in self.functions:
            return self.functions[self.type](file)
        else:
            raise ValueError(f"Invalid key: {self.type}")
    
    def to_dict(self):
        value = self.value
        if isinstance(value, datetime):
            value = value.isoformat()

        return {
            "type": self.type,
            "operation": self.operation,
            "value": value
        }

    @classmethod
    def from_dict(cls, data):
        value = data["value"]
        if "date" in data["type"]:
            value = datetime.fromisoformat(value)
        return cls(
            type=data["type"],
            operation=data["operation"],
            value=value
        )
    
    def __repr__(self):
        return (f"Condition(type={self.type!r}, operation={self.operation!r}, "
                f"value={self.value!r})")
