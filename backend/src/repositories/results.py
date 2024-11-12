from enum import Enum
from typing import List
from repositories.db_service import DBService

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

    @staticmethod
    def return_list_of_results():
        db = DBService()
        conn = db.get_db_connection()
        cursor = conn.cursor()

        # Query to fetch all test results from the testresults table
        cursor.execute("""
            SELECT testresultsid, testtype, results, resultdate 
            FROM testresults;
        """)
        rows = cursor.fetchall()

        results = []
        for row in rows:
            results.append({
                'result_id': row[0],
                'test_name': row[1],
                'results': row[2],
                'test_date': row[3]
            })
        
        cursor.close()
        conn.close()

        return results

    @staticmethod
    def remove_result(result_id: int):
        db = DBService()
        conn = db.get_db_connection()
        cursor = conn.cursor()

        # Delete the result with the given result_id
        cursor.execute("DELETE FROM testresults WHERE testresultsid = %s", (result_id,))
        
        conn.commit()
        cursor.close()
        conn.close()

    @staticmethod
    def new_result(exam_id, result_data):
        db = DBService()
        conn = db.get_db_connection()
        cursor = conn.cursor()

        # Get associated test types from prescribedTest
        cursor.execute("""
            SELECT testtype FROM presecribedTest WHERE examId = %s
        """, (exam_id,))
        test_types = cursor.fetchall()

        for test_type in test_types:
            cursor.execute("""
                INSERT INTO testresults (examid, testtype, results, resultdate)
                VALUES (%s, %s, %s, CURRENT_DATE)
            """, (exam_id, test_type[0], result_data))

        conn.commit()
        cursor.close()
        conn.close()

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