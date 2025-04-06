from datetime import datetime
from Backend.file_info import *
import operator

# TODO: Remove these imports below once done debugging, implement pytests
import os
import time

class Condition:
    operators = {
        ">": operator.gt,
        "<": operator.lt,
        ">=": operator.ge,
        "<=": operator.le,
        "==": operator.eq, 
        "!=": operator.ne,
        "includes": lambda a, b: b in a,
        "excludes": lambda a, b: b not in a
    }

    def __init__(self, type, operation, value):
        self.type = type
        self.operation = operation
        self.value = value
        self.functions = {
            "name": self.checkName,
            "extension": self.checkExtension,
            "size": self.checkSize,
            "dateCreated": self.checkCreation,
            "dateModified": self.checkModified
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
        
        # Convert to strings
        if isinstance(left, str) or isinstance(right, str):
            left, right = str(left), str(right)

        return Condition.operators[op](left, right)
    
    # Function to return the class operation to a string
    def operationToString(self):
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
    def checkName(self, file):
        Condition.verify(file)

        if not isinstance(self.value, str):
            raise ValueError("Condition check of type \"name\" must take value type string")

        return Condition.evaluate(file.name, self.operation, self.value)
    
    # Function to compare value to file extension
    def checkExtension(self, file):
        Condition.verify(file)

        if not isinstance(self.value, str):
            raise ValueError("Condition check of type \"extension\" must take value type string")

        return Condition.evaluate(file.extension, self.operation, self.value)

    # Function to compare value to file size
    def checkSize(self, file):
        Condition.verify(file)

        if isinstance(self.value, int):
            self.value = float(self.value)

        if not isinstance(self.value, float):
            raise ValueError("Condition check of type \"size\" must take value type int or float")

        return Condition.evaluate(file.size, self.operation, self.value)

    # Function to compare value to file creation date
    def checkCreation(self, file):
        Condition.verify(file)

        if not isinstance(self.value, datetime):
            raise ValueError("Condition check of type \"dateCreated\" must take value type datetime")

        return Condition.evaluate(file.dateCreated, self.operation, self.value)
    
    # Function to compare value to file modified date
    def checkModified(self, file):
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
    
    def __repr__(self):
        return (f"Condition(type={self.type!r}, operation={self.operation!r}, "
                f"value={self.value!r})")



# TODO: Remove the code below once done debugging, implement pytests

# Test function
def main():
    test_file = "test_file.txt"

    # Create test file
    if not os.path.exists(test_file):
        with open(test_file, "w") as f:
            f.write("This is a test file.")
        print(f"Test file '{test_file}' created.")

    time.sleep(1)

    # Create FileInfo object from path
    testFileInfo = FileInfo.fromPath(test_file)

    # Create Condition objects to check several attributes
    conditions = [
        Condition("extension", "==", ".txt"),
        Condition("extension", "includes", "txt"),
        Condition("name", "includes", "test"),
        Condition("name", "==", "test_file"),
        Condition("size", ">=", 20),
        Condition("size", ">", 20),
        Condition("dateCreated", ">", datetime(2025, 3, 10)),
        Condition("dateCreated", "<", datetime(2025, 3, 21)),
        Condition("dateModified", "==", datetime(2025, 3, 13)),
        Condition("dateModified", "!=", datetime(2025, 3, 13))
    ]

    print("\nCondition checks against test_file.txt:")
    for condition in conditions:
        print(f"{repr(condition)}: {condition.check(testFileInfo)}")
    

# Only run main when directly testing
if __name__ == "__main__":
    main()
