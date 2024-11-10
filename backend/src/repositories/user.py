from enum import Enum
from repositories.db_service import DBService

class Status(Enum):
    OK = "OK"
    ERROR = "ERROR"

class Role(Enum):
    ADMIN = "Administrator"
    STAF = "Staff"
    DOC = "Doctor"
    PAT = "Patient"
    NONE = "Error"

class UserInfo:
    #def __init__(self, user_type: Role, email: str, password: str, id: int):
    #    self.user_type = user_type
    #    self.email = email 
    #    # WE might not need the password
    #    self.password = password
    #    self.id = id 
    def setName(self, name: str):
        self.name = name
    def setRole(self, user_type: Role):
        self.user_type = user_type
    def setEmail(self, email: str):
        self.email = email 
    def setPassword(self, password: str):
        self.password = password
    def setId(self, id: int):
        self.id = id
    def setDob(self, dob: str):
        self.dob = dob
    def setStatus(self, status: bool):
        self.status = status
    def setDoctorId(self, doctor_id: int):
        self.doctor_id = doctor_id
    def setPhone(self, phone: int):
        self.phone = phone





class User:

    def __init__(self, user_id: int, phone_number: int, user_name: str, email: str, password: str):
        self.user_id = user_id
        self.phone_number = phone_number
        self.user_name = user_name
        self.email = email
        self._password = password  # Private attribute
        self.patient = None  # Placeholder for Patient object
        self.worker = None  # Placeholder for Worker object

    @staticmethod
    def get_user_record(email: str, password: str) -> UserInfo:
        # ...
        # SQL
        info = ("""select * from users""")
        db= DBService()
        conn = db.get_db_connection()
        cursor = conn.cursor()
        cursor.execute()
        # ... 
        info = UserInfo()
        return info

    def modify_account_info(self, email: str):
        """
        Modifies the user's account information based on the provided email.
        """
        # Implementation for modifying account info

        #connect to the database first.
        db= DBService()
        conn = db.get_db_connection()
        cursor = conn.cursor()

        # if modifying patient info
        modifyPatient = """update patient set healthid = %d, 
        patientname = %s, email = %s, DOB = %s, doctorid = %d, patientpassword = %s, phonenumber = %s 
        where email = %s"""

        #commit the change
        cursor.execute(modifyPatient)
        cursor.commit(modifyPatient)
        
        #if modifying workers info
        modifyworkers = """update workers set workersid = %d, workersname = %s, email = %s, 
        phonenumber = %s, ima ge = %s, usertype = %s, staffpassword = %s 
        where email = %s"""

          #commit the change
        cursor.execute(modifyworkers)
        cursor.commit(modifyworkers)
        
        pass

    def return_user_record(self, email: str):
        """
        Returns the user's record based on the provided email.
        """
        # Implementation for returning user record

        userRecord = """select * from users where email = %s"""

         #connect to the database 
        db= DBService()
        conn = db.get_db_connection()
        cursor = conn.cursor()
        cursor.execute()
        return userRecord
    
        pass

    def delete_account(self, user_id: int, accType: str):
        """
        Deletes the user's account by user ID.
        """
        # Implementation for deleting the account
        if accType == "Patient":
            delete = "DELETE FROM patient WHERE healthid = %s"
        if accType == "Worker":
            delete = "DELETE FROM workers WHERE workersid = %s"
        db = DBService()
        conn = db.get_db_connection()
        cursor = conn.cursor()

        cursor.execute(delete, (user_id))

        cursor.close()
        conn.close() 
    

    def _notify(self, message: str, email: str):
        """
        Notifies the user via the provided email with a message.
        """
        # Implementation for sending a notification
        pass


