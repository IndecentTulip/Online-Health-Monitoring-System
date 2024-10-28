from enum import Enum
from typing import List

class Status(Enum):
    NORMAL = "normal"
    ABNORMAL = "abnormal"

class Results:
    def __init__(self, result_id: int, patient_id: int, test_type: str, test_date: str, status: Status):
        self.result_id = result_id
        self._patient_id = patient_id  # Private attribute
        self.test_type = test_type
        self.test_date = test_date
        self.status = status

    def return_list_of_results(self, user_type: str, email: str) -> List['Results']:
        """
        Returns a list of results based on the user type (Patient or Doctor) and email.
        """
        # Implementation for returning results
        pass

    def new_result(self, result: 'Results'):
        """
        Adds a new result to the system.
        """
        # Implementation for adding a new result
        pass

    def remove_result(self, result_id: int):
        """
        Removes a result by its ID.
        """
        # Implementation for removing a result
        pass

    def modify_results(self, result_id: int):
        """
        Modifies an existing result by its ID.
        """
        # Implementation for modifying results
        pass

    def download_result(self, result_id: int):
        """
        Downloads the result by its ID.
        """
        # Implementation for downloading the result
        pass

