import os
from file_info import FileInfo
import send2trash
import shutil
import time # TODO: Remove once done debugging, implement pytests

class Action:
    def __init__(self, type, finalFolder, newName = None):
        self.type = type
        self.newName = newName

        if os.path.isdir(finalFolder):
            self.finalFolder = finalFolder
        else:
            raise TypeError("Action.finalFolder must be an existing directory")
        
        self.functions = {
            "move": self.moveFile,
            "copy": self.copyFile,
            "recycle": self.recycleFile,
            "rename": self.renameFile
        }
    
    # Helper function to verify if a file is of type FileInfo
    @staticmethod
    def verify(file):
        if not isinstance(file, FileInfo):
            raise TypeError("Action only handles type FileInfo")
    
    # Helper function to get the final path of the file
    def get_target_path(self, file):
        if self.type in ["move", "copy"]:
            return os.path.join(self.finalFolder, file.name)
        elif self.type == "rename":
            return file.path.replace(file.name, self.newName)
        elif self.type == "recycle":
            return "Recycled"
        return "Unknown"

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

        send2trash(file.path)
    
    # Function to log the action
    def logAction(self, file, logger):
        old_path = file.path
        new_path = self.get_target_path(file)
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")

        log_entry = f"[{timestamp}] {self.type.upper()} | From: {old_path} -> To: {new_path}\n"
        logger.write(log_entry)
        logger.flush()
            
    # Primary function to execute the action based on given arguments
    def execute(self, file, logger=None):
        if self.type in self.functions:
            result = self.functions[self.type](file)
            if logger:
                self.logAction(file, logger)
            return result
        else:
            raise ValueError(f"Invalid key: {self.type}")
    
    def __repr__(self):
        return (f"Action(type={self.type!r}, finalFolder={self.finalFolder!r}, "
                f"newName={self.newName!r})")
    

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

    # Create a new action to move a file to test_folder
    moveFile = Action("copy", "test_folder")

    # Execute the action
    moveFile.execute(testFileInfo)
    print(repr(moveFile))
    print("Executed!")
    

# Only run main when directly testing
if __name__ == "__main__":
    main()