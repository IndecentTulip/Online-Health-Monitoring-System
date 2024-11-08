from repositories.user import Status, User, Role, UserInfo
from repositories.db_service import DBService
import datetime

class Patient(User):
    def __init__(self, name: str, email: str, phone_number: str, dob: datetime.date, doctor: int, password: str):
        self.name = name
        self.email = email
        self.phone_number = phone_number
        self._dob = dob 
        self._status = False
        self.doctor = doctor
        self.password = password
    #def create_patient_instance(self) -> 'Patient':
    #    """
    #    Creates and returns a new instance of Patient.
    #    """
    #    # Implementation for creating a new Patient instance
    #    return Patient(0, "", "", 0, datetime.date(2024, 11, 2), 8, "")  # Placeholder, replace with actual logic

    # REQUIRED TO RUN AFTER using Patient() constractor
    def create_patient(self):
        """
        Creates a new patient record.
        """
        db = DBService()
        conn = db.get_db_connection()

        cursor = conn.cursor()
         #insert into table from test#
        creatPat = """INSERT INTO patient
         (patientname, email, dob, status, doctorid, patientpassword, phonenumber)
         VALUES (%s, %s, %s, %s, %s, %s, %s) """

        try:
            cursor.execute(creatPat, (self.name, self.email, self._dob, self._status, self.doctor, self.password, self.phone_number))
            conn.commit()  # Commit the transaction to save changes
            print("Patient record created successfully.")
            out = Status.OK
        except Exception as e:
            print(f"Failed to create patient record: {e}")
            conn.rollback()  # Rollback the transaction in case of error
            out = Status.ERROR
        finally:
            cursor.close()
            conn.close()  # Close the connection to free resources

        return out 

    def give_list_of_pending(self):
        """
        Returns a list of patients with pending status.
        """
         # Implementation for returning a list of pending patients
        db = DBService()
        conn = db.get_db_connection()

        cursor = conn.cursor()
       
        findPending = """SELECT patientID FROM patient WHERE status = FALSE"""

        cursor.execute(findPending)

        result = cursor.fetchall()
        
        cursor.close()
        del cursor
        return result
    
    def approve_patient(self, email: str):
        """
        Approves a patient based on their email.
        """
        # Implementation for approving a patient
        db = DBService()
        conn = db.get_db_connection()
        cursor = conn.cursor()
        approve = "UPDATE patient SET status = TRUE WHERE email = %s"
        cursor.execute(approve, (email))
        cursor.close()
        del cursor

    @staticmethod
    def get_user_record(email: str, password: str) -> UserInfo:
        checkPat = """SELECT COUNT(healthid) FROM patient WHERE email = %s AND patientpassword = %s"""
        fetchPat = """SELECT healthid FROM patient WHERE email = %s AND patientpassword = %s"""

        intID =0;

        db = DBService()
        conn = db.get_db_connection()

        cursor = conn.cursor()
        cursor.execute(checkPat, (email, password))
        check = cursor.fetchone()

        if check:
            userRole = Role.PAT
            cursor.execute(fetchPat, (email, password))
            fetch= cursor.fetchone()

            if fetch:
                intID = fetch[0]
        else:  
            userRole = Role.NONE
        
        cursor.close()
        del cursor
        print(check)

        info = UserInfo()
        info.setRole(userRole)
        info.setEmail(email)
        info.setId(intID)
        info.setPassword(password)
        return info

