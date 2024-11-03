from repositories.user import User, Role, UserInfo
from repositories.db_service import DBService
import datetime

class Patient(User):
    def __init__(self, health_id: int, name: str, email: str, phone_number: int, dob: datetime.date, doctor: int, password: str):
        self.health_id = health_id
        self.name = name
        self.email = email
        self.phone_number = phone_number
        self._dob = dob  # Private attribute
        self._status = False  # Private attribute, default to pending (False)
        self.doctor = doctor
        self.password = password
    def create_patient_instance(self) -> 'Patient':
        """
        Creates and returns a new instance of Patient.
        """
        # Implementation for creating a new Patient instance
        return Patient(0, "", "", 0, datetime.date(2024, 11, 2), 8, "")  # Placeholder, replace with actual logic

    def create_patient(self, patient: 'Patient'):
        """
        Creates a new patient record.
        """
        # Implementation for creating a patient
        db = DBService()
        conn = db.get_db_connection()

        cursor = conn.cursor()

        creatPat = """INSERT INTO patients
         (healthid, patientname, email, dob, status, doctorid, patientpassword, phonenumber)
          VALUES (%s, %s, %s, %s, %s, %s, %s, %s) """

        cursor.execute(creatPat, (Patient.health_id, Patient.name, Patient.email, Patient._dob, False, Patient.doctor, Patient.password, Patient.phone_number))

        cursor.close()
        del cursor

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

        db = DBService()
        conn = db.get_db_connection()

        cursor = conn.cursor()
        cursor.execute(checkPat, (email, password))
        check = cursor.fetchone()

        cursor.close()
        del cursor

        if check:
            userRole = Role.PAT
        else:  
            userRole = Role.NONE
        
        info = UserInfo()
        info.setRole(userRole)
        info.setEmail(email)
        info.setPassword(password)
        return info

