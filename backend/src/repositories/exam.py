
from sqlite3 import connect
from backend.src.repositories.db_service import DBService
import datetime
class Exam:
    def __init__(self, exam_id: int, patient_id: int, content: str):
        self.exam_id = exam_id
        self.patient_id = patient_id
        self.content = content

    def prescribe_exams(self, examtypes: list, bloodtesttypesL: list, pat_id: int, doc_id: int ):
        # Implementation for prescribing an exam
        for val in examtypes:
            self.addExam(val, pat_id, doc_id, bloodtesttypesL)

        

    def remove_exam(self, exam_id: int):
        # Implementation for removing an exam

        #remove based on examID.
        removeExam =("""delete from examtable where examid = %s """) #user enters id info
        removeExamTests = """DELETE FROM prescribedTest WHERE examid = %s"""
        removeExamtestResults = """DELETE FROM testresults WHERE examid = %s"""
        db = DBService()
        conn = db.get_db_connection()
        cursor = conn.cursor()

        cursor.execute(removeExamtestResults, (exam_id))
        cursor.execute(removeExamTests, (exam_id))
        cursor.execute(removeExam, (exam_id))
        #commit te change.
        cursor.commit()
        #close the execution
        cursor.close()
        conn.close()
        

    def return_list_of_exams(self, email: str):
        # Implementation for returning a list of exams based on email
        pass

    def addExam(self, examtype: str, health_id: int, doc_id: int, bloodtests: list): #insert query for exam. 
          #insert a new exam onto the table. #user enters info. 
        createExam = """Insert into examtable( examdate, healthid, workersid, examtype) values ( %s, %s, %s, %s)"""
        createPerTests ="""Insert into presecribedTest (examId, testtype) values (%s, %s)"""
        getnewExamID = """SELECT Auto_increment FROM information_schema.tables WHERE table_name='examtable';"""
        db = DBService()
        conn = db.get_db_connection()
        cursor = conn.cursor()

        cursor.execute(getnewExamID)
        newID = cursor.fetchone

        cursor.execute(createExam, (datetime.today(), health_id, doc_id, examtype))

        if examtype == 'Blood':
            for value in bloodtests:
                cursor.execute(createPerTests, (newID, value))
        else:
            cursor.execute(createPerTests, (newID, examtype))

        cursor.commit()
        cursor.close()
        conn.close()
        print("exam updated.")
    
    def getExams(): #select statement for getting the exams.
        Examinfo = """select * from examtable"""
        db = DBService
        conn =db.get_db_connection()
        cursor = conn.cursor()
        cursor.execute(Examinfo)    

    