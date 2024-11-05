
from sqlite3 import connect
from backend.src.repositories.db_service import DBService

class Exam:
    def __init__(self, exam_id: int, patient_id: int, content: str):
        self.exam_id = exam_id
        self.patient_id = patient_id
        self.content = content

    def prescribe_exam(self, exam: 'Exam'):
        # Implementation for prescribing an exam

        #insert a new exam onto the table. #user enters info. 
        createExam = input("""Insert into examtable(examid, examdate, healthid, workersid, examtype) values (%d, %s, %d, %d, %s)""")
        db = DBService()
        conn = db.get_db_connection()
        cursor = conn.cursor()
        cursor.execute(createExam(exam.examid, exam.examdate,exam.healtid,  ))


        pass

    def remove_exam(self, exam_id: int):
        # Implementation for removing an exam

        #remove based on examID.
        removeExam =("""delete from examtable where examid = %d """) #user enters id info
        db = DBService()
        conn = db.get_db_connection()
        cursor = conn.cursor()

        # check to see if userID exist. 
        try:
        
        cursor.execute(removeExam,(removeExam.examid))

        conn.commit()
        print(f"{exam_id} removed")

        except Exception as e: #if the user ID does not exist.
            
        connect.rollback()
        
        finally: 
    
        cursor.close()
        conn.close()
        pass

    def return_list_of_exams(self, email: str):
        # Implementation for returning a list of exams based on email
        pass

