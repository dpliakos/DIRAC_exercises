"""Simple test on using mock.

The test of the task 2 will fail because the fakeObject does not have a
`aMethodToMock` method.

In order to fix the test, I set the `fakeObject.aMethodToMock` method to a
`MagicMock` method that returns the bumber 3. The number 3 is found subtracting
the  5 (excepted number) from the 2 (hard coded number at test).
"""

import mock
import pytest
import unittest


#########################
# function to test
def myFunction(objectIn):
    """What you are supposed to test."""
    return objectIn.aMethodToMock() + 2

#########################
# Actual test
@pytest.fixture
def objectMock():
    """A fixture to create a fake object as we want it."""
    fakeObject = mock.MagicMock()
    fakeObject.aMethodToMock = mock.MagicMock(return_value=3)
    return fakeObject


def test_myFunction(objectMock):
    """Test myFunction."""
    assert myFunction(objectMock) == 5
