from collections import namedtuple
from contextlib import nullcontext
from os import walk
from repositories.db_service import DBService

from repositories import user
from repositories.exam import Exam
from repositories.patient import Patient;
from typing import List

from flask import Flask, request, jsonify
from repositories.results import Results
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

        if user_info is None:  # If the patient is not approved
            return jsonify({
                'error': 'Your account is not approved yet. Please contact support.'
            }), 403  # 403 Forbidden: The patient is not approved.

        if user_info.user_type.value != "Error":
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


    def view_patient(self, id: int):
        try:
            # Get the patient record from the Patient class
            patient = Patient.get_user_record_profile(id)
    
            if patient:
                # Return the formatted response in JSON format
                return jsonify({
                    'id': patient.id,
                    'name': patient.name,
                    'email': patient.email,
                    'dob': patient.dob,
                    'status': patient.status,
                    'doctor_id': patient.id,
                    'phone': patient.phone,
                })
            else:
                return jsonify({'error': 'Patient not found'}), 404
    
        except Exception as e:
            return jsonify({'error': f'Something went wrong: {str(e)}'}), 500


    def update_patient_profile(self, id: int, data: dict):
        try:
            # Assuming `Patient` has a method to update profile
            updated_patient = Patient.update_user_record_profile(id, data)
    
            if updated_patient:
                return updated_patient
            else:
                return None
        except Exception as e:
            raise Exception(f"Error updating patient profile: {str(e)}")

    def view_all_patients(self):
        try:
            # Fetch list of pending patients from Patient class
            patients = Patient.give_list_of_pending()
            
            if patients:
                # Format the patient data for frontend
                patient_list = [{
                    'healthid': patient[0],  # Patient ID from the DB
                    'patientname': patient[1],
                    'email': patient[2],
                    'status': patient[3]
                } for patient in patients]
                
                return jsonify(patient_list)
            else:
                return jsonify({'message': 'No pending patients found'}), 404
        except Exception as e:
            return jsonify({'error': f'Something went wrong: {str(e)}'}), 500
    
    def update_patient_account_status(self, patient_id: int):
        try:
            # Approve the patient by updating the status to True
            Patient.approve_patient(patient_id)
            return jsonify({'message': 'Patient approved successfully'}), 200
        except Exception as e:
            return jsonify({'error': f'Something went wrong: {str(e)}'}), 500

    def view_worker(self, id: int):
        try:
            # Get worker record from Worker class
            worker = Worker.get_user_record_profile(id)
    
            if worker:
                # Return the worker data as JSON
                return jsonify({
                    'id': worker.id,
                    'name': worker.name,
                    'email': worker.email,
                    'phone': worker.phone,
                    'image': worker.image,  # You may choose to encode the image
                    'user_type': worker.user_type
                })
            else:
                return jsonify({'error': 'Worker not found'}), 404
        except Exception as e:
            return jsonify({'error': f'Something went wrong: {str(e)}'}), 500
    
    def update_worker_account(self, id: int, data: dict):
        try:
            # Update the worker's information through the Worker class
            updated_worker = Worker.update_user_record_profile(id, data)
    
            if updated_worker:
                return jsonify({
                    'message': 'Worker profile updated successfully',

                    'worker': {
                        'id': updated_worker.id,
                        'name': updated_worker.name,
                        'email': updated_worker.email,
                        'phone': updated_worker.phone,
                        'user_type': updated_worker.user_type
                    }
                }), 200
            else:
                return jsonify({'error': 'Worker not found'}), 404
        except Exception as e:
            return jsonify({'error': f'Something went wrong: {str(e)}'}), 500


    # Fetch all workers
    def view_every_worker(self):
        try:
            workers = Worker.get_user_record_account()  # Fetch all workers
            return workers
        except Exception as e:
            raise Exception(f"Error fetching workers: {str(e)}")

    # Fetch all patients
    def view_every_patient(self):
        try:
            patients = Patient.get_user_record_account()  # Fetch all patients
            return patients
        except Exception as e:
            raise Exception(f"Error fetching patients: {str(e)}")

    # Add a new worker account
    def create_worker_account(self, worker_name, worker_email, worker_role, worker_phone, worker_password):
        try:
            Worker.create_worker(worker_name, worker_email, worker_role, worker_phone, worker_password)  # Pass the data to Worker class
        except Exception as e:
            raise Exception(f"Error creating worker: {str(e)}")

    # Delete a worker account
    def delete_worker_account(self, worker_id):
        try:
            Worker.delete_account(worker_id)  # Call Worker method to delete the account
        except Exception as e:
            raise Exception(f"Error deleting worker: {str(e)}")

    # Delete a patient account
    def delete_patient_account(self, patient_id):
        try:
            Patient.delete_account(patient_id)  # Call Patient method to delete the account
        except Exception as e:
            raise Exception(f"Error deleting patient: {str(e)}")

    def get_exam_types(self):
        try:
            exam_types = Exam.fetch_exam_types()
            return exam_types
        except Exception as e:
            raise Exception(f'Error fetching exam types: {str(e)}')

    def get_test_types(self):
        try:
            # Fetch test types and their associated exam types
            test_types = Exam.return_test_types_with_examtype()
            return test_types
        except Exception as e:
            raise Exception(f'Error fetching test types: {str(e)}')
    
    def prescribe_exam(self, data):
        try:
            exam_id = Exam.prescribe_exam(data)
            return exam_id
        except Exception as e:
            raise Exception(f'Error prescribing exam: {str(e)}')
  
    def doctors_patients(self, user_id):
        try:
            patients = Worker.get_doctors_patients(user_id)
            return patients
        except Exception as e:
            raise Exception(f'Error fetching patients: {str(e)}')


    def get_all_exams(self):
        try:
            exams = Exam.fetch_exams_with_patient_info()  # Fetch exams with patient info
            return exams
        except Exception as e:
            raise Exception(f"Error fetching exams: {str(e)}")

    def get_test_types_for_exam(self, exam_id):
        try:
            test_types = Exam.fetch_test_types(exam_id)  # Fetch test types associated with the selected exam
            return test_types
        except Exception as e:
            raise Exception(f"Error fetching test types for exam {exam_id}: {str(e)}")


    def create_results(self, user_id, exam_id, result_data):
        db = DBService()
        conn = db.get_db_connection()
        cursor = conn.cursor()
    
        # Get associated test types for the selected exam
        cursor.execute("""
            SELECT testtype FROM presecribedTest WHERE examId = %s
        """, (exam_id,))
        test_types = cursor.fetchall()
    
        # Loop through each test type and insert the result data
        for test_type in test_types:
            # Assume `result_data` contains results for each test type, possibly in an array or dictionary format
            test_result = result_data.get(test_type[0])
    
            if test_result is not None:  # Only insert if there's a result for this test type
                cursor.execute("""
                    INSERT INTO testresults (examid, testtype, results, resultdate)
                    VALUES (%s, %s, %s, CURRENT_DATE)
                """, (exam_id, test_type[0], test_result))
    
        conn.commit()
        cursor.close()
        conn.close()


    def view_all_results(self):
        try:
            return Results.return_list_of_results()
        except Exception as e:
            raise Exception(f"Error fetching results for user  {str(e)}")
    
    def delete_results(self, result_id):
        try:
            Results.remove_result(result_id)
        except Exception as e:
            raise Exception(f"Error deleting result with ID {result_id}: {str(e)}")
       
   
    def view_year_n_month_reports(self):
        return jsonify({
            'temp': 'temp'
        })
    
    def create_year_n_month_reports(self):
        return jsonify({
            'temp': 'temp'
        })

    def view_predict_reports(self):
        return jsonify({
            'temp': 'temp'
        })
    
    def create_predict_reports(self):
    #def create_reports(self, admin: Worker):
        return jsonify({
            'temp': 'temp'
        })

#
#    def delete_report(self):
#    #def delete_report(self, report_id: int):
#        return jsonify({
#            'temp': 'temp'
#        })

    def view_smart_monitor(self):
        return jsonify({
            'temp': 'temp'
        })

    def create_smart_monitor(self):
    #def create_smart_monitor(self, doctor: Worker, options: List[str]):
        return jsonify({
            'temp': 'temp'
        })
 
    
    def change_smart_monitor(self):
    #def change_smart_monitor(self, doctor: Worker, options: List[str]):
        return jsonify({
            'temp': 'temp'
        })
 
    def delete_smart_monitor(self):
    #def delete_smart_monitor(self, monitor_id: int):
         return jsonify({
            'temp': 'temp'
        })
    

