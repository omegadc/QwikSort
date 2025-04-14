import os
from Backend.file_info import FileInfo
from pathlib import Path
import send2trash
import shutil

class Action:
    def __init__(self, type, finalFolder = None, newName = None):
        self.type = type
        self.newName = newName
        
        if finalFolder is None:
            self.finalFolder = finalFolder
        elif os.path.isdir(finalFolder):
            self.finalFolder = finalFolder
        else:
            raise TypeError("Action.finalFolder must be an existing directory")
        
        self.functions = {
            "move": self.moveFile,
            "copy": self.copyFile,
            "recycle": self.recycleFile,
            "rename": self.renameFile
        }
    
    # Helper function to verify if a file is of type FileInfo and if the file actually exists
    @staticmethod
    def verify(file):
        if not isinstance(file, FileInfo):
            raise TypeError("Action only handles type FileInfo")
        if not os.path.exists(file.path):
            raise FileNotFoundError(f"File not found: {file.path}")
    
    # Helper function to get the final path of the file
    def getTargetPath(self, file):
        if self.type in ["move", "copy"]:
            return os.path.join(self.finalFolder, file.name + file.extension)
        elif self.type == "rename":
            return file.path.replace(file.name, self.newName)
        elif self.type == "recycle":
            return "Recycled"
        return "Unknown"
    
    def getReverseAction(self, file: FileInfo) -> 'Action':
        if self.type == "move":
            print(f"REVERSE: Reverse destination for file at path {file.path} is {os.path.dirname(file.path)}")
            return Action("move", finalFolder=os.path.dirname(file.path))
        elif self.type == "copy":
            return Action("recycle")
        elif self.type == "rename":
            return Action("rename", newName=file.name)
        elif self.type == "copy":
            return Action("recycle") # Delete the copy
        elif self.type == "recycle":
            # Can't restore recycled files without backup
            raise NotImplementedError("Undo for recycle is not supported without a backup.")
        else:
            raise ValueError(f"No reverse defined for action type {self.type}")
        

    # Function to move a given file to the final folder
    def moveFile(self, file):
        Action.verify(file)

        destination = os.path.join(self.finalFolder, os.path.basename(file.path))

        try:
            if os.path.exists(destination):
                return  # Skip the file
            shutil.move(file.path, destination)
        except Exception as e:
            print(f"Failed to move file '{file.path}' to '{destination}': {e}")

    
    # Function to copy a given file to the final folder
    def copyFile(self, file):
        Action.verify(file)

        if os.path.exists(os.path.join(self.finalFolder, file.path)):
            # TODO: Implement overwriting logic
            raise NotImplementedError("Overwrite logic has not been implemented")
        
        shutil.copy(file.path, self.finalFolder)

    # Function to rename a given file
    def renameFile(self, file):
        Action.verify(file)

        if not self.newName:
            raise ValueError("No argument provided for rename operation")

        new_path = file.path.replace(file.name, self.newName)

        if os.path.exists(new_path):
            # TODO: Implement overwriting logic
            raise NotImplementedError("Overwrite logic has not been implemented")

        os.rename(file.path, new_path)
        
    # Function to recycle a given file
    def recycleFile(self, file):
        Action.verify(file)

        clean_path = Path(file.path).resolve()
        send2trash.send2trash(str(clean_path))
    
    # Function to log the action
    def logAction(self, file, logger):
        old_path = file.path
        new_path = self.getTargetPath(file)
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")

        log_entry = f"[{timestamp}] {self.type.upper()} | From: {old_path} -> To: {new_path}\n"
        logger.write(log_entry)
        logger.flush()
            
    # Primary function to execute the action based on given arguments
    def execute(self, file, logger=None):
        if self.type in self.functions:
            print(f"ACTION: Executing action of type {self.type}")
            result = self.functions[self.type](file)
            if logger:
                self.logAction(file, logger)
            file.path = self.getTargetPath(file)
            file.name = os.path.basename(file.path)
            return result
        else:
            raise ValueError(f"Invalid key: {self.type}")
    
    def __repr__(self):
        return (f"Action(type={self.type!r}, finalFolder={self.finalFolder!r}, "
                f"newName={self.newName!r})")
    
    def to_dict(self):
        return {
            "type": self.type,
            "finalFolder": self.finalFolder,
            "newName": self.newName
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            type=data["type"],
            finalFolder=data.get("finalFolder"),
            newName=data.get("newName")
        )
    