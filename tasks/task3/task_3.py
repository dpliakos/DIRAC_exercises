"""The task3 module."""

import psutil
import json


class ProcessInspector(object):
    """Persist information about the current process."""

    def __init__(self):
        """Save the current process at a variable."""
        self.process = psutil.Process()
        self.file_name = "dpliakos_test_file_process"
        print (self.process)

    def collect_process_information(self):
        """Collect data for the current process."""
        process_data = {
            'id': self.process.pid,
            'name': self.process.name(),
            'status': self.process.status(),
            'number_of_threads': self.process.num_threads()
        }

        return process_data

    def save_process_info(self):
        """Save the process data to a JSON file."""
        data = self.collect_process_information()

        with open(self.file_name, 'w') as file:
            json.dump(data, file)
