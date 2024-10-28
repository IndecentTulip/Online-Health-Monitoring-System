
from typing import List

class System:
    def __init__(self):
        self.permission_manager = PermissionManager()
        self.session_manager = SessionManager()
        self.monitors_list: List[Monitor] = []
        self.report_list: List[Report] = []
        self.exams_list: List[Exam] = []
        self.results_list: List[Result] = []

    def register(self):
        pass

    def manage_accounts(self):
        pass

    def create_worker_account(self):
        pass

    def delete_worker_account(self):
        pass

    def log_in(self, email: str, password: str):
        pass

    def token_required(self, f):
        pass

    def modify_account(self, user_type: str, ui_input: List[str]):
        pass

    def view_exam(self):
        pass

    def prescribe_exam(self, doctor: Doctor, patient: Patient):
        pass

    def view_results(self):
        pass

    def create_results(self, staff: Staff, patient: Patient):
        pass

    def delete_results(self, result_id: int):
        pass

    def filter_results(self, results: List[Result], result_type: str):
        pass

    def create_reports(self, admin: Admin):
        pass

    def delete_report(self, report_id: int):
        pass

    def create_smart_monitor(self, doctor: Doctor, options: List[str]):
        pass

    def change_smart_monitor(self, doctor: Doctor, options: List[str]):
        pass

    def delete_smart_monitor(self, monitor_id: int):
        pass

    def logout(self, email: str):
        pass

