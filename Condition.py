import operator
import FileInfo

class Condition:
    def __init__(self, type, operation, value):
        self.type = type
        self.operation = operation
        self.value = value
        self.actions = {
            "name": self.checkName,
            "extension": self.checkExtension,
            "size": self.checkSize,
            "dateCreated": self.checkCreation,
            "dateModified": self.checkModified
        }
        self.operators = {
            ">": operator.gt,
            "<": operator.lt,
            ">=": operator.ge,
            "<=": operator.le,
            "==": operator.eq, 
            "!=": operator.ne,
            "contains": lambda a, b: b in a  # String containment
        }

    # Helper function to verify if a file is of type FileInfo
    def verify(self, file):
        if type(file) != FileInfo:
            raise TypeError("Condition only handles type FileInfo")
    
    # Helper function to evaluate a comparison using a string operator
    def evaluate(self, left, op, right):
        if op not in self.operators:
            raise ValueError(f"Invalid operator {op}")
        
        # Convert to strings
        if isinstance(left, str) or isinstance(right, str):
            left, right = str(left), str(right)

        return self.operators[op](left, right)
    
    # Function to compare value to file name
    def checkName(self, file):
        Condition.verify(file)

        if not isinstance(self.value, str):
            raise ValueError("checkName must take value type string")

        return Condition.evaluate(file.name, self.value)
    
    # Function to compare value to file extension
    def checkExtension(self, file):
        Condition.verify(file)

        if not isinstance(self.value, str):
            raise ValueError("checkExtension must take value type string")

        return Condition.evaluate(file.extension, self.value)

    # Function to compare value to file name
    def checkSize(self, file):
        Condition.verify(file)

        if not isinstance(self.value, float):
            raise ValueError("checkSize must take value type float")

        return Condition.evaluate(file.size, self.value)
    
    # TODO: Implement checkCreation and checkModified by supporting datetime objects