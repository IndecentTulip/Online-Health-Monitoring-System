from enum import Enum
from typing import List
from backend.src.repositories.db_service import DBService

class Status(Enum):
    NORMAL = "normal"
    ABNORMAL = "abnormal"

class Results:
    def __init__(self, exam_id: int, patient_id: int, test_type: str, test_date: str, status: Status, value: float):
        self.exam_id = exam_id
        self._patient_id = patient_id  # Private attribute
        self.test_type = test_type
        self.test_date = test_date
        self.status = status
        self.value = value

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
        db = DBService()
        conn = db.get_db_connection()
        cursor = conn.cursor()
        # Implementation for adding a new result
        addRes = "INSERT INTO testresults (testtype, examid, result) VALUES (%s, %s, %s)"

        cursor.execute(addRes, (result.test_type, result.exam_id, result.value))

        cursor.commit()

        cursor.close()
        conn.close()
       

    def remove_result(self, result: 'Results'):
        """
        Removes a result by its ID.
        """
        # Implementation for removing a result
        db = DBService()
        conn = db.get_db_connection()
        cursor = conn.cursor()
        # Implementation for adding a new result
        delRes = "DELETE FROM WHERE testtype = %s AND examid = %s)"

        cursor.execute(delRes, ( result.test_type, result.exam_id,))

        cursor.commit()

        cursor.close()
        conn.close()

    def modify_results(self, result: 'Results'):
        """
        Modifies an existing result by its ID.
        """
        # Implementation for modifying results
        db = DBService()
        conn = db.get_db_connection()
        cursor = conn.cursor()
        # Implementation for adding a new result
        updateRes = "UPDATE testresults SET result = %s WHERE testtype = %s AND examid = %s)"

        cursor.execute(updateRes, (result.value, result.test_type, result.exam_id,))

        cursor.commit()

        cursor.close()
        conn.close()

    def download_result(self, result_id: int):
        """
        Downloads the result by its ID.
        """
        # Implementation for downloading the result
        pass

