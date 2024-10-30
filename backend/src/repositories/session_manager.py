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
        # Implementation for creating a session
        # TODO: figure out how session would be created, 
        #   Original idea was to create an object and put it into the stack of sessions on the server
        #   BUT there is also a way to implement in though storing sessions in a db, as a [email][token] table
        #   IN both cases there should be a timer/hearbit that will eventually remove the session, so it might require additional methods to be impl
        pass

    @staticmethod
    def decode_token(token: str) -> UserInfo:
        """
        Decodes a session token to retrieve session information.
        """
        # Implementation for decoding the token
        pass

