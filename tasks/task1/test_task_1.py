"""Test file for the task1."""

import os
import unittest
import pytest
from task1 import SingleFileManager

FILE_TO_BE_CREATED = "dpliakos_test_file_create"
FILE_TO_BE_DELETED = "dpliakos_test_file_delete"


@pytest.fixture
def mannually_create_file(scope="function"):
    """Create a file manually."""
    with open(FILE_TO_BE_DELETED, 'w'):
        pass


class TaskOne(unittest.TestCase):
    """Test the SingleFileManager module."""

    def setUp(self):
        """Decide the file name."""
        self.filename_to_be_created = FILE_TO_BE_CREATED
        self.filename_to_be_deleted = FILE_TO_BE_DELETED

    def tearDown(self):
        """Clear the any files will be created by the test."""
        file_create_exist = os.path.isfile(self.filename_to_be_created)
        file_delete_exist = os.path.isfile(self.filename_to_be_deleted)

        if (file_create_exist):
            os.remove(self.filename_to_be_created)

        if (file_delete_exist):
            os.remove(self.filename_to_be_created)

    def test_create_file(self):
        """Test the file creation of the module."""
        fileManager = SingleFileManager(self.filename_to_be_created)
        fileManager.createFile()

        fileCreated = os.path.isfile(self.filename_to_be_created)
        self.assertTrue(fileCreated)

    @pytest.mark.usefixtures("mannually_create_file")
    def test_delete_file(self):
        """Test the file delete of the module."""
        fileManager = SingleFileManager(self.filename_to_be_deleted)
        fileManager.deleteFile()

        fileExist = os.path.isfile(self.filename_to_be_deleted)
        self.assertFalse(fileExist)
