from repositories.db_service import DBService

class Exam:
    @staticmethod
    def fetch_exam_types():
        db = DBService()
        conn = db.get_db_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT examtype FROM examtype")  # Fetch all exam types
        exam_types = cursor.fetchall()

        # Return exam types as a list
        exam_types_list = [exam[0] for exam in exam_types]

        cursor.close()
        conn.close()
        return exam_types_list


    @staticmethod
    def fetch_test_types():
        db = DBService()
        conn = db.get_db_connection()
        cursor = conn.cursor()

        # Fetch all test types related to blood tests, filtering based on the 'Blood Test' exam type
        cursor.execute("SELECT * FROM testtypes;")
        test_types = cursor.fetchall()

        # Return test types as a list
        test_types_list = [test[0] for test in test_types]

        cursor.close()
        conn.close()
        return test_types_list


    @staticmethod
    def prescribe_exam(data):
        exam_type = data.get('examType')
        healthid = data.get('patientId')  # Patient ID
        workersid = data.get('doctorId')  # Doctor's ID (logged in user)
        content = data.get('content')  # Exam content (e.g., notes)
        test_types = data.get('testTypes', [])  # List of test types
        
        db = DBService()
        conn = db.get_db_connection()
        cursor = conn.cursor()
        
        # Insert the exam data into the examtable
        cursor.execute(
            "INSERT INTO examtable (examdate, healthid, workersid, examtype, notes) VALUES (CURRENT_DATE, %s, %s, %s, %s) RETURNING examid",
            (healthid, workersid, exam_type, content)
        )
        exam_id = cursor.fetchone()[0]
        
        # Insert prescribed test types for this exam
        for test_type in test_types:
            cursor.execute(
                "INSERT INTO presecribedTest (examid, testtype) VALUES (%s, %s)",
                (exam_id, test_type)
            )
        
        conn.commit()
        cursor.close()
        conn.close()
        
        return exam_id
    @staticmethod
    def return_test_types_with_examtype():
        db = DBService()
        conn = db.get_db_connection()
        cursor = conn.cursor()
    
        cursor.execute("SELECT testtype, examtype FROM testtypes")
        test_types = cursor.fetchall()
    
        test_type_list = [{
            'testtype': test[0],
            'examtype': test[1]
        } for test in test_types]
    
        cursor.close()
        conn.close()
    
        return test_type_list

