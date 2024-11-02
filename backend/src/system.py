from collections import namedtuple
from contextlib import nullcontext

from repositories import user
from repositories.patient import Patient;
from typing import List

from repositories.session_manager import SessionManager
from repositories.workers import Worker
from repositories.user import UserInfo

class System:
    # def __init__(self):
        # self.permission_manager = PermissionManager()
        # self.session_manager = SessionManager()
        # self.monitors_list: List[Monitor] = []
        # self.report_list: List[Report] = []
        # self.exams_list: List[Exam] = []
        # self.results_list: List[Result] = []

    def register(self):
        pass

    def manage_accounts(self):
        pass

    def create_worker_account(self):
        pass

    def delete_worker_account(self):
        pass

    def log_in(self, type: int, email: str, password: str):
        user_info: UserInfo
        if type == 1: # patient
            user_info = Patient.get_user_record(email, password)
        elif type == 0: # worker
            user_info = Worker.get_user_record(email, password)
        else:
            return "error"

        if (user_info.user_type.value != "Error"):

            token = SessionManager.generate_token(user_info.email)
            SessionManager.create_session(token, user_info.email, user_info.user_type.value)

    def token_required(self, token: str):
        user_info: UserInfo
        user_info = SessionManager.decode_token(token)
        if (user_info.user_type.value == "Administrator" and
          user_info.user_type.value == "Staff" and
          user_info.user_type.value == "Doctor"):
            Worker.get_user_record(user_info.email, user_info.password)
            # return conformation
        elif (user_info.user_type.value == "Patient"):
            Patient.get_user_record(user_info.email, user_info.password)
            # return conformation
        else:
            return "error"

            

    def modify_account(self, user_type: str, ui_input: List[str]):
        pass

    def view_exam(self):
        pass

        #    def prescribe_exam(self, doctor: Doctor, patient: Patient):
        #        pass
        #
        #    def view_results(self):
        #        pass
        #
        #    def create_results(self, staff: Staff, patient: Patient):
        #        pass
        #
        #    def delete_results(self, result_id: int):
        #        pass
        #
        #    def filter_results(self, results: List[Result], result_type: str):
        #        pass
        #
        #    def create_reports(self, admin: Admin):
        #        pass
        #
        #    def delete_report(self, report_id: int):
        #        pass
        #
        #    def create_smart_monitor(self, doctor: Doctor, options: List[str]):
        #        pass
        #
        #    def change_smart_monitor(self, doctor: Doctor, options: List[str]):
        #        pass
        #
        #    def delete_smart_monitor(self, monitor_id: int):
        #        pass
        #

