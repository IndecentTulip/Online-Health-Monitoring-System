from typing import List
from repositories.user import User, Role, UserInfo
from repositories.db_service import DBService

class Worker(User):

    def __init__(self, worker_id: int, image: int, name: str, email: str, phone_number: int, role: Role, password: str):
        self.worker_id = worker_id
        self.image = image
        self.name = name
        self.email = email
        self.phone_number = phone_number
        self.role = role
        self._password = password

    # Fetch all worker records
    @staticmethod
    def get_user_record_account():
        query = "SELECT * FROM workers;"
        
        db = DBService()
        conn = db.get_db_connection()
        cursor = conn.cursor()

        cursor.execute(query)
        rows = cursor.fetchall()

        workers = []
        for row in rows:
            workers.append({
                'workerid': row[0],
                'worker_name': row[1],
                'worker_email': row[2],
                'worker_role': row[6]
            })
        
        cursor.close()
        conn.close()

        return workers

    @staticmethod
    def create_worker(worker_name, worker_email, worker_role, worker_phone, worker_password):
        # Insert worker into the database with phone and password
        create_query = """
        INSERT INTO workers (workersname, email, usertype, phonenumber, staffpassword)
        VALUES (%s, %s, %s, %s, %s);
        """
        
        db = DBService()
        conn = db.get_db_connection()
        cursor = conn.cursor()
    
        # Use hashed password here (you should hash the password before storing it in the database)
        # If you're using bcrypt, you can do something like:
        # hashed_password = bcrypt.hashpw(worker_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
        cursor.execute(create_query, (worker_name, worker_email, worker_role, worker_phone, worker_password))
        conn.commit()  # Commit the transaction
        
        cursor.close()
        conn.close()

    # Delete a worker account
    @staticmethod
    def delete_account(worker_id):
        delete_query = "DELETE FROM workers WHERE workersid = %s;"
        
        db = DBService()
        conn = db.get_db_connection()
        cursor = conn.cursor()

        cursor.execute(delete_query, (worker_id,))
        conn.commit()  # Commit the transaction
        
        cursor.close()
        conn.close()


    def create_worker_instance(self):
        """
        Creates and returns a new instance of Worker.
        """
        # Implementation for creating a new Worker instance
        #return Worker(0, 0, "", "", 0, Role.STAF)  # Placeholder, replace with actual logic
    
    @staticmethod
    def get_user_record(email: str, password: str) -> UserInfo:
        checkWork = """SELECT COUNT(workersid) FROM workers WHERE email = %s AND staffpassword = %s"""
        fetchWork = """SELECT workersid, usertype FROM workers WHERE email = %s AND staffpassword = %s"""
        strRole = ""
        intID = 0;
        
        db = DBService()
        conn = db.get_db_connection()

        cursor = conn.cursor()
        cursor.execute(checkWork, (email, password))
        check = cursor.fetchone()
        if check is None:
            userRole = Role.NONE
        else:  
            cursor.execute(fetchWork, (email, password))
            fetch= cursor.fetchone()
            print(fetch)

            if fetch:
                intID = fetch[0]
                strRole = fetch[1]

        
        cursor.close()
        del cursor
        conn.close()

        for role in Role:
            if role.value == strRole:
                info = UserInfo()
                info.setRole(role)
                info.setEmail(email)
                info.setId(intID)
                info.setPassword(password)
                return info

        info = UserInfo()
        info.setRole(Role.NONE)
        return info



    @staticmethod
    def get_user_record_profile(id: int) -> UserInfo:
        # Query the database to retrieve worker's profile information
        query = """
        SELECT workersid, workersname, email, phonenumber, image, usertype 
        FROM workers
        WHERE workersid = %s;
        """
    
        db = DBService()
        conn = db.get_db_connection()
        cursor = conn.cursor()
    
        cursor.execute(query, (id,))
        result = cursor.fetchone()
    
        cursor.close()
        conn.close()

        worker_info = UserInfo()
    
        if result:
            # Return a UserInfo object for the worker
            worker_info.setId(result[0])
            worker_info.setName(result[1])
            worker_info.setEmail(result[2])
            worker_info.setPhone(result[3])
            worker_info.setImage(result[4])  # You can decide to return the image as base64 or URL
            worker_info.setUserType(result[5])
            return worker_info

        else:
            return worker_info
    
    @staticmethod
    def update_user_record_profile(data: dict) -> UserInfo:
        # Update worker profile in the database with provided data
        update_query = """
        UPDATE workers
        SET workersname = %s, email = %s, phonenumber = %s, image = %s
        WHERE workersid = %s
        RETURNING workersid, workersname, email, phonenumber, image, usertype;
        """
    
        db = DBService()
        conn = db.get_db_connection()
        cursor = conn.cursor()
    
        # Assuming the image is passed as a bytea type (e.g., as base64 string or a path)
        # {'email': 'Jayne.Samer@jlabemail.com', 'id': 21003, 'image': {}, 'name': 'Jayne Samer Test', 'phone': '7893217894', 'user_type': 'Staff'}
        cursor.execute(update_query, (
            data.get('name'),
            data.get('email'),
            data.get('phone'),
            data.get('image'),  # You can modify how you handle image (base64 or binary)
            data.get('id') 
        ))
    
        result = cursor.fetchone()
    
        conn.commit()
        cursor.close()
        conn.close()

        worker_info = UserInfo()
    
        if result:
            # Return updated worker profile data as a UserInfo object
            worker_info.setId(result[0])
            worker_info.setName(result[1])
            worker_info.setEmail(result[2])
            worker_info.setPhone(result[3])
            worker_info.setImage(result[4])
            worker_info.setUserType(result[5])
    
            return worker_info
        else:
            return worker_info


    @staticmethod
    def get_doctors_list() -> List:
        fetchEmailNId = """SELECT workersID, email FROM workers WHERE userType = 'Doctor';"""
        
        db = DBService()
        conn = db.get_db_connection()

        cursor = conn.cursor()
        cursor.execute(fetchEmailNId)
        doctors = cursor.fetchall()

        doctors_info_list = []

        if doctors:
            for doc in doctors:
                info = UserInfo()
                info.setId(doc[0])
                info.setEmail(doc[1])
                doctors_info_list.append(info)

        cursor.close()
        del cursor
        conn.close()

        return doctors_info_list

        
    @staticmethod
    def get_doctors_patients(user_id):
        db = DBService()
        conn = db.get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT patient.healthid, patient.patientname
            FROM patient
            WHERE patient.doctorid = %s
        """, (user_id,))

        patients = cursor.fetchall()
        
        # Map the results to a dictionary with healthid and name
        patients_list = [{'id': patient[0], 'name': patient[1]} for patient in patients]

        cursor.close()
        conn.close()
        return patients_list

