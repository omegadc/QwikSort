import os
from backend.file_info import FileInfo
from pathlib import Path
import send2trash
import shutil
import time

class Action:
    def __init__(self, type, final_folder = None, new_name = None):
        self.type = type
        self.new_name = new_name
        
        if final_folder is None:
            self.final_folder = final_folder
        elif os.path.isdir(final_folder):
            self.final_folder = final_folder
        else:
            raise TypeError("Action.final_folder must be an existing directory")
        
        self.functions = {
            "move": self.move_file,
            "copy": self.copy_file,
            "recycle": self.recycle_file,
            "rename": self.rename_file
        }
    
    # Helper function to verify if a file is of type FileInfo and if the file actually exists
    @staticmethod
    def verify(file):
        if not isinstance(file, FileInfo):
            raise TypeError("Action only handles type FileInfo")
        if not os.path.exists(file.path):
            raise FileNotFoundError(f"File not found: {file.path}")
    
    # Helper function to get the final path of the file
    def get_target_path(self, file):
        if self.type in ["move", "copy"]:
            return os.path.join(self.final_folder, file.name + file.extension)
        elif self.type == "rename":
            return file.path.replace(file.name, self.new_name)
        elif self.type == "recycle":
            return "Recycled"
        return "Unknown"
    
    def get_reverse_action(self, file: FileInfo) -> 'Action':
        if self.type == "move":
            print(f"REVERSE: Reverse destination for file at path {file.path} is {os.path.dirname(file.path)}")
            return Action("move", final_folder=os.path.dirname(file.path))
        elif self.type == "copy":
            return Action("recycle")
        elif self.type == "rename":
            return Action("rename", new_name=file.name)
        elif self.type == "copy":
            return Action("recycle") # Delete the copy
        elif self.type == "recycle":
            # Can't restore recycled files without backup
            raise NotImplementedError("Undo for recycle is not supported without a backup.")
        else:
            raise ValueError(f"No reverse defined for action type {self.type}")
        

    # Function to move a given file to the final folder
    def move_file(self, file):
        Action.verify(file)

        destination = os.path.join(self.final_folder, os.path.basename(file.path))

        try:
            if os.path.exists(destination):
                return  # Skip the file
            shutil.move(file.path, destination)
        except Exception as e:
            print(f"Failed to move file '{file.path}' to '{destination}': {e}")

    
    # Function to copy a given file to the final folder
    def copy_file(self, file):
        Action.verify(file)

        if os.path.exists(os.path.join(self.final_folder, file.path)):
            # TODO: Implement overwriting logic
            raise NotImplementedError("Overwrite logic has not been implemented")
        
        shutil.copy(file.path, self.final_folder)

    # Function to rename a given file
    def rename_file(self, file):
        Action.verify(file)

        if not self.new_name:
            raise ValueError("No argument provided for rename operation")

        new_path = file.path.replace(file.name, self.new_name)

        if os.path.exists(new_path):
            # TODO: Implement overwriting logic
            raise NotImplementedError("Overwrite logic has not been implemented")

        os.rename(file.path, new_path)
        
    # Function to recycle a given file
    def recycle_file(self, file):
        Action.verify(file)

        clean_path = Path(file.path).resolve()
        send2trash.send2trash(str(clean_path))
    
    # Function to log the action
    def log_action(self, file, logger):
        old_path = file.path
        new_path = self.get_target_path(file)
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
                self.log_action(file, logger)
            file.path = self.get_target_path(file)
            file.name = os.path.basename(file.path)
            return result
        else:
            raise ValueError(f"Invalid key: {self.type}")
    
    def __repr__(self):
        return (f"Action(type={self.type!r}, final_folder={self.final_folder!r}, "
                f"new_name={self.new_name!r})")
    
    def to_dict(self):
        return {
            "type": self.type,
            "final_folder": self.final_folder,
            "new_name": self.new_name
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            type=data["type"],
            final_folder=data.get("final_folder"),
            new_name=data.get("new_name")
        )
    