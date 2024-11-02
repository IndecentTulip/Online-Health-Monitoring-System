from repositories.user import User, Role, UserInfo
from repositories.db_service import DBService

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
        checkWork = """SELECT COUNT(usertype) FROM workers WHERE email = %s AND staffpassword = %s"""
        fetchWork = """SELECT usertype FROM workers WHERE email = %s AND staffpassword = %s"""
        strRole = ""
        
        db = DBService()
        conn = db.get_db_connection()

        cursor = conn.cursor()
        cursor.execute(checkWork, (email, password))
        check = cursor.fetchone()
        if check is None:
            userRole = Role.NONE
        else:  
            cursor.execute(fetchWork, (email, password))
            strRole = cursor.fetchone()

            if check is not None:
                strRole = strRole[0]
        
        cursor.close()
        del cursor

        for role in Role:
            if role.value == strRole:
                return UserInfo(role, email, password)

        return UserInfo(Role.NONE, "", "")

