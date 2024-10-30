class Patient:
    def __init__(self, health_id: int, name: str, email: str, phone_number: int, dob: str):
        self.health_id = health_id
        self.name = name
        self.email = email
        self.phone_number = phone_number
        self._dob = dob  # Private attribute
        self._status = False  # Private attribute, default to pending (False)

    def create_patient_instance(self) -> 'Patient':
        """
        Creates and returns a new instance of Patient.
        """
        # Implementation for creating a new Patient instance
        return Patient(0, "", "", 0, "")  # Placeholder, replace with actual logic

    def create_patient(self, patient: 'Patient'):
        """
        Creates a new patient record.
        """
        # Implementation for creating a patient
        pass

    def give_list_of_pending(self) -> list:
        """
        Returns a list of patients with pending status.
        """
        # Implementation for returning a list of pending patients
        pass

    def approve_patient(self, email: str):
        """
        Approves a patient based on their email.
        """
        # Implementation for approving a patient
        pass

