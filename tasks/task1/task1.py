"""The code fot the task 1.

Most important commands:

command1:
with open(__FILE_PATH__, __FILE_CMD__):
    pass

command2:
os.remote(__FILE_PATH__)

"""
import os


class SingleFileManager(object):
    """Can create or delete a file, given it's path."""

    def __init__(self, file_path):
        """Initialize the class with the file path."""
        self.file_path = file_path

    def createFile(self):
        """Create the file."""
        with open(self.file_path, 'w'):
            pass

    def deleteFile(self):
        """Delete the file."""
        os.remove(self.file_path)
