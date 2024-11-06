
from sqlite3 import connect
from backend.src.repositories.db_service import DBService

class Exam:
    def __init__(self, exam_id: int, patient_id: int, content: str):
        self.exam_id = exam_id
        self.patient_id = patient_id
        self.content = content

    def prescribe_exam(self, exam: 'Exam'):
        # Implementation for prescribing an exam
        pass

    def remove_exam(self, exam_id: int):
        # Implementation for removing an exam

        #remove based on examID.
        removeExam =("""delete from examtable where examid = %d """) #user enters id info
        db = DBService()
        conn = db.get_db_connection()
        cursor = conn.cursor()
        cursor.execute(removeExam)
        #commit te change.
        cursor.commit()
        #close the execution
        cursor.close()
        conn.close()
        pass

    def return_list_of_exams(self, email: str):
        # Implementation for returning a list of exams based on email
        pass

    def addExam(): #insert query for exam. 
          #insert a new exam onto the table. #user enters info. 
        createExam = ("""Insert into examtable(examid, examdate, healthid, workersid, examtype) values (%d, %s, %d, %d, %s)""")
        db = DBService()
        conn = db.get_db_connection()
        cursor = conn.cursor()
        cursor.execute(createExam)
        cursor.commit()
        print("exam updated.")

    
    