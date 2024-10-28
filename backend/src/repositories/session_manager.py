class SessionManager:
    def __init__(self):
        self.sessions = []  # Heterogeneous array to hold session data

    def generate_token(self, email: str) -> str:
        """
        Generates a session token for the given email.
        """
        # Implementation for generating a token
        pass

    def create_session(self, session_type: bool, user: 'Worker' or 'Patient'):
        """
        Creates a new session for a user (Worker or Patient).
        """
        # Implementation for creating a session
        pass

    def decode_token(self, token: str):
        """
        Decodes a session token to retrieve session information.
        """
        # Implementation for decoding the token
        pass

