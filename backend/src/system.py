from collections import namedtuple
from contextlib import nullcontext
from os import walk

from repositories import user
from repositories.patient import Patient;
from typing import List

from flask import Flask, request, jsonify
from repositories.session_manager import SessionManager
from repositories.workers import Worker
from repositories.user import UserInfo
from datetime import datetime

class System:
    # def __init__(self):
        # self.permission_manager = PermissionManager()
        # self.session_manager = SessionManager()
        # self.monitors_list: List[Monitor] = []
        # self.report_list: List[Report] = []
        # self.exams_list: List[Exam] = []
        # self.results_list: List[Result] = []

    def create_patient_account(self,patientName: str, email: str, phoneNumber: str, dob: str, docID: int, password: str):

        date_object = datetime.strptime(dob, "%Y-%m-%d").date()
        newPatient = Patient(patientName, email, phoneNumber, date_object, docID, password)
        status = newPatient.create_patient()

        return jsonify({
                'confirm': status.name
            })

    def log_in(self, userType: str, email: str, password: str):
        if userType == "patient":  # Patient
            user_info = Patient.get_user_record(email, password)
        elif userType == "worker":  # Worker
            user_info = Worker.get_user_record(email, password)
        else:
            return jsonify({
                'error': 'Invalid user type'
            }), 400  # Return an error response for invalid user type

        if user_info and user_info.user_type.value != "Error":
            return jsonify({
                'login': {
                    'routeTo': user_info.user_type.value,
                    'email': user_info.email,
                    'id': user_info.id,
                }
            })
        return None 

            # NOT IN USE
            #token = SessionManager.generate_token(user_info.email)
            #SessionManager.create_session(token, user_info.email, user_info.user_type.value)
            # NOT IN USE

    # NOT IN USE

    #def token_required(self, token: str):
    #    user_info: UserInfo
    #    user_info = SessionManager.decode_token(token)
    #    if (user_info.user_type.value == "Administrator" and
    #      user_info.user_type.value == "Staff" and
    #      user_info.user_type.value == "Doctor"):
    #        Worker.get_user_record(user_info.email, user_info.password)
    #        # return conformation
    #    elif (user_info.user_type.value == "Patient"):
    #        Patient.get_user_record(user_info.email, user_info.password)
    #        # return conformation
    #    else:
    #        return "error"

    # NOT IN USE

    def get_doc_list_form(self):
        result = Worker.get_doctors_list()

        doctor_list = [{
            'id': info.id,
            'email': info.email,
        } for info in result]

        return jsonify(doctor_list)

    def view_patient(self, id:int):
        out = Patient.get_user_record_profile(id)

        # ...
        return jsonify({
            ""
        })

    def view_worker(self, id:int):
        out = Worker.get_user_record_profile(id)

        # ...
        return jsonify({
            ""
        })

    def create_worker_account(self):
        return jsonify({
            ""
        })
            
    def modify_patient_account(self):
        return jsonify({
            ""
        })

    def modify_worker_account(self):
        return jsonify({
            ""
        })

    def delete_worker_account(self):
        return jsonify({
            ""
        })

    def delete_patient_account(self):
        return jsonify({
            ""
        })

    def view_exam(self):
        return jsonify({
            ""
        })

    def prescribe_exam(self):
        return jsonify({
            ""
        })
    
    def view_results(self):
        return jsonify({
            ""
        })

    def create_results(self):
    #def create_results(self, staff: Worker, patient: Patient):
        return jsonify({
            ""
        })
    
    def delete_results(self):
    # def delete_results(self, result_id: int):
        return jsonify({
            ""
        })
    
    def view_reports(self):
        return jsonify({
            ""
        })
    
    def create_reports(self):
    #def create_reports(self, admin: Worker):
        return jsonify({
            ""
        })

    def delete_report(self):
    #def delete_report(self, report_id: int):
        return jsonify({
            ""
        })

    def view_smart_monitor(self):
        return jsonify({
            ""
        })

    def create_smart_monitor(self):
    #def create_smart_monitor(self, doctor: Worker, options: List[str]):
        return jsonify({
            ""
        })
 
    
    def change_smart_monitor(self):
    #def change_smart_monitor(self, doctor: Worker, options: List[str]):
        return jsonify({
            ""
        })
 
    def delete_smart_monitor(self):
    #def delete_smart_monitor(self, monitor_id: int):
         return jsonify({
            ""
        })
    

