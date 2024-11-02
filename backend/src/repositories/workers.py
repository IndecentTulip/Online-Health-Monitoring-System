from repositories.user import User, Role

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

