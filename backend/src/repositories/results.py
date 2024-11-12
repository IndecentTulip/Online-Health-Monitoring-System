from enum import Enum
from typing import List
from repositories.db_service import DBService
from datetime import date

class Status(Enum):
    NORMAL = "normal"
    ABNORMAL = "abnormal"

class Results:
    def __init__(self, result_id: int, test_type: str, exam_id: int, results: int, test_date: str):
        self.result_id = result_id
        self.exam_id = exam_id  
        self.test_type = test_type
        self.test_date = test_date
        self.results = results

    @staticmethod
    def result_search(search_type: int, date: date, test_type: str, pat_name: str, patient_ID: int )-> List['Results']:
     
        # 0 = search by date  (patient)              4 = search by patient name + date (doctor)
        # 1 = search by exam item (patient)          5 = search by name + exam item (doctor)
        # 2 = search by abnormal results (patient)   6 = search by abnormal result (doctor)
        # 3 = search by patient name (doctor)
        query_0 = """SELECT testresults.testresultsid, testresults.testtype, testresults.examid, testresults.results, testresults.resultdate 
                    FROM testresults LEFT JOIN examtable ON testresults.examid = examtable.examid
                    WHERE examtable.patientid = %d AND testresults.resultdate = %s"""
        query_1 = """SELECT testresults.testresultsid, testresults.testtype, testresults.examid, testresults.results, testresults.resultdate 
                    FROM testresults LEFT JOIN examtable ON testresults.examid = examtable.examid
                    WHERE examtable.patientid = %d AND testresults.testtype = %s"""
        query_2 = """SELECT testresults.testresultsid, testresults.testtype, testresults.examid, testresults.results, testresults.resultdate 
                    FROM testresults LEFT JOIN examtable ON testresults.examid = examtable.examid
                    LEFT JOIN testtypes ON testresults.test = testtypes.testtype
                    WHERE examtable.patientid = %d AND NOT (testtype.lowerbound < testresults.result < testtype.upperbound)"""
        query_3 = """SELECT testresults.testresultsid, testresults.testtype, testresults.examid, testresults.results, testresults.resultdate 
                    FROM testresults LEFT JOIN examtable ON testresults.examid = examtable.examid
                    LEFT JOIN patient ON examtable.healthid = patient.healthid
                    WHERE patient.patientname = %s"""
        query_4 = """SELECT testresults.testresultsid, testresults.testtype, testresults.examid, testresults.results, testresults.resultdate 
                    FROM testresults LEFT JOIN examtable ON testresults.examid = examtable.examid
                    LEFT JOIN patient ON examtable.healthid = patient.healthid
                    WHERE patient.patientname = %s AND examtable.examdate = %s"""
        query_5 = """SELECT testresults.testresultsid, testresults.testtype, testresults.examid, testresults.results, testresults.resultdate 
                    FROM testresults LEFT JOIN examtable ON testresults.examid = examtable.examid
                    LEFT JOIN patient ON examtable.healthid = patient.healthid
                    WHERE patient.patientname = %s AND testresults.testtype = %s"""
        query_6 = """SELECT testresults.testresultsid, testresults.testtype, testresults.examid, testresults.results, testresults.resultdate 
                    FROM testresults LEFT JOIN testtypes ON testresults.test = testtypes.testtype
                    WHERE NOT (testtype.lowerbound < testresults.result < testtype.upperbound)"""
        db = DBService()
        conn = db.get_db_connection()
        cursor = conn.cursor()
        returnlist = []

        if search_type == 0:
            cursor.execute(query_0, (patient_ID, date))
        elif search_type == 1:
            cursor.execute(query_1, (patient_ID, test_type))
        elif search_type == 2:
            cursor.execute(query_2, (patient_ID,))
        elif search_type == 3:
            cursor.execute(query_3, (pat_name,))
        elif search_type == 4:
            cursor.execute(query_4, (pat_name, date))
        elif search_type == 5:
            cursor.execute(query_5, (pat_name, test_type))
        elif search_type == 6:
            cursor.execute(query_6)

        for row in results:
            returnlist.append(Results(row[0], row[1], row[2], row[3], row[4]))
        return returnlist


    @staticmethod
    def return_list_of_results():
        # Initialize DBService and establish a connection
        db = DBService()
        conn = db.get_db_connection()
        cursor = conn.cursor()

        # Query to fetch all test results from the testresults table
        print("TEST 1")
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
