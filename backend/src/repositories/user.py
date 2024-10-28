class User:
    def __init__(self, user_id: int, phone_number: int, user_name: str, email: str, password: str):
        self.user_id = user_id
        self.phone_number = phone_number
        self.user_name = user_name
        self.email = email
        self._password = password  # Private attribute
        self.patient = None  # Placeholder for Patient object
        self.worker = None  # Placeholder for Worker object

    def modify_account_info(self, email: str):
        """
        Modifies the user's account information based on the provided email.
        """
        # Implementation for modifying account info
        pass

    def return_user_record(self, email: str):
        """
        Returns the user's record based on the provided email.
        """
        # Implementation for returning user record
        pass

    def delete_account(self, user_id: int):
        """
        Deletes the user's account by user ID.
        """
        # Implementation for deleting the account
        pass

    def _notify(self, message: str, email: str):
        """
        Notifies the user via the provided email with a message.
        """
        # Implementation for sending a notification
        pass

