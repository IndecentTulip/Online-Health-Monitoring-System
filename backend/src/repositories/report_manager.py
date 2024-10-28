from enum import Enum

class ReportType(Enum):
    MONTHLY = "monthly"
    YEARLY = "yearly"
    PREDICTION = "prediction"

class ReportManager:
    def __init__(self, report_id: int, report_type: ReportType, date_created: str, content: str):
        self.report_id = report_id
        self.report_type = report_type
        self.date_created = date_created
        self.content = content

    def return_list_of_reports(self, email: str) -> list:
        """
        Returns a list of reports associated with the given email.
        """
        # Implementation for returning reports
        pass

    def generate_report(self):
        """
        Generates a new report.
        """
        # Implementation for generating a report
        pass

    def remove_report(self, report_id: int):
        """
        Removes a report by its ID.
        """
        # Implementation for removing a report
        pass

    def send_report(self, receiver_email: str):
        """
        Sends the report to the specified email address.
        """
        # Implementation for sending the report
        pass

    def download_report(self):
        """
        Downloads the report.
        """
        # Implementation for downloading the report
        pass

