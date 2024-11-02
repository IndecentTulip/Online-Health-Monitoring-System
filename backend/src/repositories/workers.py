from repositories.user import User, Role, UserInfo
import db_service

class Worker(User):

    def __init__(self, worker_id: int, image: int, name: str, email: str, phone_number: int, role: Role):
        self.worker_id = worker_id
        self.image = image
        self.name = name
        self.email = email
        self.phone_number = phone_number
        self.role = role

    def create_worker(self, worker: 'Worker'):
        """
        Creates a new worker record.
        """
        # Implementation for creating a worker
        pass

    def create_worker_instance(self) -> 'Worker':
        """
        Creates and returns a new instance of Worker.
        """
        # Implementation for creating a new Worker instance
        return Worker(0, 0, "", "", 0, Role.STAF)  # Placeholder, replace with actual logic
    
    @staticmethod
    def get_user_record(email: str, password: str) -> UserInfo:
        # ...
        # SQL
        # ... 
       
        checkWork = """SELECT COUNT usertype FROM workers WHERE email = ? AND staffpassword = ?"""
        fetchWork = """SELECT usertype FROM workers WHERE email = ? AND staffpassword = ?"""
        
        conn = db_service.get_db_connection
        cursor = conn.cursor()
        cursor.execute(checkWork(email, password))
        check = cursor.fetchone()
        if check == 0:
            userRole = Role("Error")
        else:  
            cursor.execute(fetchWork(email, password))
            userRole = Role(cursor.fetchone())
        
        cursor.close()
        del cursor
        return UserInfo(userRole, email, password)

