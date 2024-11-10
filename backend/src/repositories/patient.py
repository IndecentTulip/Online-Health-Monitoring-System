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

    @staticmethod
    def give_list_of_pending():
        """
        Returns a list of patients with pending status.
        """
        db = DBService()
        conn = db.get_db_connection()
        cursor = conn.cursor()
    
        findPending = """SELECT healthid, patientname, email, status 
                         FROM patient WHERE status = FALSE"""
    
        cursor.execute(findPending)
        result = cursor.fetchall()
    
        cursor.close()
        conn.close()
    
        return result
    
    @staticmethod
    def approve_patient(patient_id: int):
        """
        Approves a patient by updating their status to TRUE based on their healthid.
        """
        db = DBService()
        conn = db.get_db_connection()
        cursor = conn.cursor()
    
        approve = """UPDATE patient SET status = TRUE WHERE healthid = %s"""
        cursor.execute(approve, (patient_id,))
    
        conn.commit()
        cursor.close()
        conn.close()

    @staticmethod
    def get_user_record(email: str, password: str) -> UserInfo:
        # Modify the query to directly select healthid and status without COUNT
        fetchPat = """SELECT healthid, status FROM patient WHERE email = %s AND patientpassword = %s"""
    
        intID = 0
        patientStatus = None
    
        db = DBService()
        conn = db.get_db_connection()
    
        cursor = conn.cursor()
        cursor.execute(fetchPat, (email, password))
        fetch = cursor.fetchone()
    
        if fetch:
            intID = fetch[0]
            patientStatus = fetch[1]  # The patient's status field
    
        cursor.close()
        del cursor
    
        info = UserInfo()
        info.setEmail(email)
        info.setId(intID)
        info.setPassword(password)
    
        if patientStatus is False:  # If the patient is not approved
            info.setRole(Role.NONE)  # Set the role to NONE or another indication of not approved
            return info  # We can return None or a specific error message here if status is False.
    
        # Assuming user is approved
        userRole = Role.PAT if patientStatus is True else Role.NONE
        info.setRole(userRole)
        return info        # Assuming user is approved


    @staticmethod
    def get_user_record_profile(id: int) -> UserInfo:
        # Database query to fetch patient information
        query = """
        SELECT healthid, patientname, email, dob, status, doctorid, phonenumber
        FROM patient
        WHERE healthid = %s;
        """
        
        db = DBService()
        conn = db.get_db_connection()
        cursor = conn.cursor()

        cursor.execute(query, (id,))
        result = cursor.fetchone()

        cursor.close()
        conn.close()

        patient_info = UserInfo()

        if result:
            # Create and return a UserInfo object
            patient_info.setId(result[0])
            patient_info.setName(result[1])
            patient_info.setEmail(result[2])
            patient_info.setDob(result[3])
            patient_info.setStatus(result[4])
            patient_info.setDoctorId(result[5])
            patient_info.setPhone(result[6])

            return patient_info
        else:
            return patient_info


    @staticmethod
    def update_user_record_profile(id: int, data: dict):
        # Database query to update patient information
        update_query = """
        UPDATE patient
        SET patientname = %s, email = %s, phonenumber = %s
        WHERE healthid = %s;
        """
    
        db = DBService()
        conn = db.get_db_connection()
        cursor = conn.cursor()
    
        # Assuming we are only updating the name, email, and phone for simplicity
        cursor.execute(update_query, (data.get('name'), data.get('email'), data.get('phone'), id))
        
        conn.commit()
        cursor.close()
        conn.close()
    
        # Fetch the updated patient to return
        return Patient.get_user_record_profile(id)


