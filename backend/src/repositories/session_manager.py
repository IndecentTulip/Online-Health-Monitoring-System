from repositories.user import User, Role
from repositories.user import UserInfo


class SessionManager:
    def __init__(self):
        self.sessions = []  # Heterogeneous array to hold session data

    @staticmethod
    def generate_token(email: str) -> str:
        """
        Generates a session token for the given email.
        """
        # Implementation for generating a token
        pass

    @staticmethod
    def create_session( token: str, email: str, user_type: str):
        """
        Creates a new session for a user (Worker or Patient).
        """
        # Implementation for creating a session
        pass

    @staticmethod
    def decode_token(token: str) -> UserInfo:
        """
        Decodes a session token to retrieve session information.
        """
        # Implementation for decoding the token
        pass

