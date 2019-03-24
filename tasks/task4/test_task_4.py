"""Test file for the task 4."""

import json
import pytest
import unittest
from elasticsearch import NotFoundError, ConnectionError
from ..task3.task_3 import ProcessInspector
from .task_4 import ElasticSearchClient


TEST_INDEX = "dpliakos-my-index"
TEST_INDEX_2 = "dpliakos-my-index-2"
TEST_INDEX_3 = "dpliakos-my-index-3"


@pytest.fixture
def create_the_process_file():
    """Trigger the process creation from the ProcessInspector."""
    pi = ProcessInspector()
    pi.collect_process_information()
    pi.save_process_info()


@pytest.fixture
def delete_test_index():
    """Delete the test index."""
    try:
        ElasticSearchClient().delete_index(TEST_INDEX)
    except NotFoundError:
        pass


@pytest.fixture
def create_some_indices():
    """Create dome indices for the list."""
    ElasticSearchClient().create_index(TEST_INDEX_2)
    ElasticSearchClient().create_index(TEST_INDEX_3)


class TaskFour(unittest.TestCase):
    """Test the Elastic search client module."""

    def setUp(self):
        """Initialize the connection."""
        self.test_index = TEST_INDEX

    def tearDown(self):
        """Remove the indices that were made from the test."""
        try:
            ElasticSearchClient().delete_index(self.test_index)
            ElasticSearchClient().delete_index(TEST_INDEX_2)
            ElasticSearchClient().delete_index(TEST_INDEX_3)
        except NotFoundError:
            pass

    def test_connect_to_the_running_instance(self):
        """Test for the correct connection.

        if info fail, there is not a connection.
        """
        try:
            client = ElasticSearchClient()
            es = client.getES()
            es.info()
            connected = True
        except ConnectionError:
            connected = False

        self.assertTrue(connected)

    @pytest.mark.usefixtures("delete_test_index")
    def test_create_an_index(self):
        """Create an index in Elastic Search and then verify it's existance."""
        client = ElasticSearchClient()
        res = client.create_index(self.test_index)
        status = res['acknowledged']
        self.assertTrue(status)

        # verify
        exist = client.getES().indices.exists([self.test_index])
        self.assertTrue(exist)

    @pytest.mark.usefixtures("create_some_indices")
    def test_list_all_indices(self):
        """List all the indices."""
        client = ElasticSearchClient()
        res = client.get_all_indices()

        # no output will beshow at console on a successful run.
        for key in res:
            print (key)

        self.assertTrue(len(res) >= 2)

        res = client.delete_all_indices()
        deleted = res["acknowledged"]
        self.assertTrue(deleted)

        # verify that no index exist
        res = client.get_all_indices()
        self.assertEqual(len(res), 0)

    # WARNING:
    # Although the last test, completes with no errors and with the `tearDown`
    # function commented out, I can not find the dpliakos-my-index index
    # using my console.
    # The data are retrieved correctly as I see with `print`.
    # If I run the same code outside the test_task_4.py file I see the index
    # from consoele/browser.

    @pytest.mark.usefixtures("delete_test_index")
    @pytest.mark.usefixtures("create_the_process_file")
    def test_create_the_index_again(self):
        """Create the index again."""
        client = ElasticSearchClient()
        res = client.create_index(self.test_index)
        status = res['acknowledged']
        self.assertTrue(status)

        # read data from the file
        file_name = ProcessInspector().get_file_path()
        with open(file_name, 'r') as json_file:
            process_info = json.load(json_file)

        # add data to elastic search
        res_add = client.add_data(self.test_index, 'process', 1, process_info)
        status = res_add['_shards']['successful']
        self.assertEqual(status, 1)

        # get data from elastic search
        res_read = client.read_data(self.test_index, 'process', 1)

        # compars received data and data read from the file.
        match = res_read['_source'] == process_info
        self.assertTrue(match)
