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
    def setDoctorId(self, id: int):
        self.id = id
    def setPhone(self, phone: int):
        self.phone = phone
    def setImage(self, image: str):
        self.image = image
    def setUserType(self, user_type: str):
        self.user_type = user_type






class User:

    def __init__(self, user_id: int, phone_number: int, user_name: str, email: str, password: str):
        self.user_id = user_id
        self.phone_number = phone_number
        self.user_name = user_name
        self.email = email
        self._password = password  # Private attribute
        self.patient = None  # Placeholder for Patient object
        self.worker = None  # Placeholder for Worker object

    def modify_account_info(self, id: int):
        """
        Modifies the user's account information based on the provided email.
        """
        # Implementation for modifying account info

        #connect to the database first.
        db= DBService()
        conn = db.get_db_connection()
        cursor = conn.cursor()

        # use ID instead of email
        modifyPatient = """update patient set healthid = %d, 
        patientname = %s, email = %s, DOB = %s, doctorid = %d, patientpassword = %s, phonenumber = %s 
        where email = %s"""

        #commit the change
        cursor.execute(modifyPatient)

        # use ID instead of email
        modifyworkers = """update workers set workersid = %d, workersname = %s, email = %s, 
        phonenumber = %s, ima ge = %s, usertype = %s, staffpassword = %s 
        where email = %s"""

          #commit the change
        cursor.execute(modifyworkers)
        
   

    def _notify(self, message: str, email: str):
        """
        Notifies the user via the provided email with a message.
        """
        # Implementation for sending a notification
        pass


