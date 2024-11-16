from datetime import datetime
from os import stat
from flask import Flask, request, jsonify
from flask_cors import CORS
from system import System
import json
from decimal import Decimal
import datetime

app = Flask(__name__)
CORS(app)

# Create an instance of the System class
system = System()

# <><><><><><><> AUTH <><><><><><><><><>

# Used by Components/Auth/Login
@app.route('/login', methods=['POST'])
def post_login():
    try:
        data = request.json
        if not data or not all(k in data for k in ['userType', 'email', 'password']):
            return jsonify({'error': 'Missing required fields'}), 400
        
        userType = data['userType']
        email = data['email']
        password = data['password']

        if userType not in ['patient', 'worker']:
            return jsonify({'error': 'Invalid userType. Must be "patient" or "worker".'}), 400

        response = system.log_in(userType, email, password)
        
        if response is None:
            return jsonify({'error': 'Your account is not approved yet. Please contact support.'}), 400  # Return an error response if None

        return response 

    except KeyError as e:
        return jsonify({'error': f'Missing key: {str(e)}'}), 400
    except Exception as e:
        return jsonify({'error': f'Something went wrong: {str(e)}'}), 500


# Used by Components/Auth/Register (to register a patient)
@app.route('/register', methods=['POST'])
# maybe move it to /accounts/patient/add instead of /register
def post_register():
    try:
        data = request.json
        required_fields = ['patientName', 'email', 'phoneNumber', 'dob', 'docID', 'password']
        
        # Check for missing fields
        if not data or not all(k in data for k in required_fields):
            return jsonify({'error': 'Missing required fields'}), 400

        patientName = data['patientName']
        email = data['email']
        phoneNumber = data['phoneNumber']
        dob = data['dob']
        docID = data['docID']
        password = data['password']
        
        response = system.create_patient_account(patientName, email, phoneNumber, dob, docID, password)
        
        if response is None:
            return jsonify({'error': 'Registration failed. Please check your details and try again.'}), 400
        
        return response

    except KeyError as e:
        return jsonify({'error': f'Missing key: {str(e)}'}), 400
    except Exception as e:
        return jsonify({'error': f'Something went wrong: {str(e)}'}), 500


# Used by Components/Auth/Register (to get doctors)
@app.route('/register', methods=['GET'])
def get_doctors():
    try:
        # Retrieve the doctor list
        doctors = system.get_doc_list_form()
        
        if not doctors:
            return jsonify({'error': 'No doctors found'}), 404
        
        return doctors

    except Exception as e:
        return jsonify({'error': f'Something went wrong: {str(e)}'}), 500

# <><><><><><><> AUTH <><><><><><><><><>


# <><><><><><><> PROFILE <><><><><><><><><>

# Route for viewing the patient profile
@app.route('/profile/patient/view', methods=['GET'])
def get_patient_profile():
    patient_id = request.args.get('patient_id')
    if not patient_id:
        return jsonify({'error': 'Patient ID is required'}), 400

    patient = system.view_patient(int(patient_id))
    
    if patient:
        return patient
    else:
        return jsonify({'error': 'Patient not found'}), 404

# Route for updating the patient profile
@app.route('/profile/patient/edit', methods=['PATCH'])
def edit_patient_profile():
    patient_id = request.args.get('patient_id')
    if not patient_id:
        return jsonify({'error': 'Patient ID is required'}), 400

    try:
        data = request.get_json()
        # Process the update logic (you can expand this to validate each field)
        patient = system.update_patient_profile(int(patient_id), data)

        if patient:
            return jsonify({'success': 'Patient profile updated successfully'}), 200
        else:
            return jsonify({'error': 'Patient not found'}), 404

    except Exception as e:
        return jsonify({'error': f'Something went wrong: {str(e)}'}), 500
# View worker profile
@app.route('/profile/worker/view', methods=['GET'])
def get_worker_profile():
    worker_id = request.args.get('worker_id')
    if not worker_id:
        return jsonify({'error': 'Worker ID is required'}), 400
    
    worker = system.view_worker(worker_id)
    
    if worker:
        return worker
        #return jsonify({'temp': 'Not implemented'}), 404
    else:
        return jsonify({'error': 'Worker not found'}), 404

@app.route('/profile/worker/edit', methods=['PATCH'])
def patch_worker_profile():
    worker_id = request.args.get('worker_id')
    if not worker_id:
        return jsonify({'error': 'Worker ID is required'}), 400

    # Get the updated data from the request
    updated_data = request.json
    if not updated_data:
        return jsonify({'error': 'No data provided for update'}), 400

    # Call the system to modify the worker account with the provided data
    try:
        #system.modify_worker_account(worker_id, updated_data)
        system.update_worker_account(worker_id, updated_data)
        return jsonify({'message': 'Worker profile updated successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# <><><><><><><> PROFILE <><><><><><><><><>

# <><><><><><><> ACCOUNT <><><><><><><><><>

@app.route('/accounts/workers/every/fetch', methods=['GET'])
def get_workers():
    try:
        workers = system.view_every_worker()
        # Check if workers data has the correct structure
        if not workers:
            return jsonify({'error': 'No workers found'}), 404
        return jsonify(workers), 200
    except Exception as e:
        return jsonify({'error': f'Something went wrong: {str(e)}'}), 500

@app.route('/accounts/patient/every/fetch', methods=['GET'])
def get_patients():
    try:
        patients = system.view_every_patient()  
        return jsonify(patients), 200
    except Exception as e:
        return jsonify({'error': f'Something went wrong: {str(e)}'}), 500

@app.route('/accounts/workers/add', methods=['POST'])
def add_worker():
    data = request.get_json()
    worker_name = data.get('worker_name')
    worker_email = data.get('worker_email')
    worker_role = data.get('worker_role')
    worker_phone = data.get('worker_phone')
    worker_password = data.get('worker_password')

    if not worker_name or not worker_email or not worker_role or not worker_phone or not worker_password:
        return jsonify({'error': 'Worker data is incomplete'}), 400

    try:
        system.create_worker_account(worker_name, worker_email, worker_role, worker_phone, worker_password)
        return jsonify({'message': 'Worker added successfully'}), 201
    except Exception as e:
        return jsonify({'error': f'Error creating worker: {str(e)}'}), 500

@app.route('/accounts/workers/del', methods=['DELETE'])
def delete_worker():
    data = request.get_json()
    worker_id = data.get('worker_id')

    if not worker_id:
        return jsonify({'error': 'Worker ID is required'}), 400

    try:
        system.delete_worker_account(worker_id)
        return jsonify({'message': 'Worker deleted successfully'}), 200
    except Exception as e:
        return jsonify({'error': f'Error deleting worker: {str(e)}'}), 500

@app.route('/accounts/patient/del', methods=['DELETE'])
def delete_patient():
    data = request.get_json()
    patient_id = data.get('patient_id')
    
    if not patient_id:
        return jsonify({'error': 'Patient ID is required'}), 400

    try:
        system.delete_patient_account(patient_id)
        return jsonify({'message': 'Patient deleted successfully'}), 200
    except Exception as e:
        return jsonify({'error': f'Error deleting patient: {str(e)}'}), 500# used to get list of pending
@app.route('/accounts/patient/fetch', methods=['GET'])
def get_patients_pending():
    try:
        patients = system.view_all_patients()  # Call the system to get all pending patients
        return patients
    except Exception as e:
        return jsonify({'error': f'Something went wrong: {str(e)}'}), 500

# uset for status
@app.route('/accounts/patient/update', methods=['PATCH'])
def patch_patients_status():
    patient_id = request.json.get('patient_id')  # Extract patient_id from the request body

    if not patient_id:
        return jsonify({'error': 'Patient ID is required'}), 400

    try:
        # Call the system to approve the patient
        system.update_patient_account_status(patient_id)
        return jsonify({'message': 'Patient account approved successfully'}), 200
    except Exception as e:
        return jsonify({'error': f'Something went wrong: {str(e)}'}), 500

# @app.route('/accounts/workers/update', methods=['PATCH'])
# def patch_workers():
#     id =0
#     system.update_worker_account(id, data)
#     return jsonify({'temp': 'Not implemented'}), 404

# <><><><><><><> ACCOUNT <><><><><><><><><>

# <><><><><><><> EXAMS <><><><><><><><><>

@app.route('/exam/fetch_exam_types', methods=['GET'])
def get_exam_types():
    try:
        exam_types = system.get_exam_types()  # Fetch the list of exam types from system
        return jsonify(exam_types), 200
    except Exception as e:
        return jsonify({'error': f'Something went wrong: {str(e)}'}), 500


@app.route('/exam/fetch_test_types', methods=['GET'])
def get_test_types():
    try:
        test_types = system.get_test_types()  # Fetch the list of test types (including blood tests) from system
        return jsonify(test_types), 200
    except Exception as e:
        return jsonify({'error': f'Something went wrong: {str(e)}'}), 500


@app.route('/exam/new', methods=['POST'])
def post_exams():
    try:
        data = request.json
        # Only one exam type should be passed at a time, process each exam type individually
        system.prescribe_exam(data)  # Pass the data to the system layer for processing
        return jsonify({'message': 'Exam prescribed successfully'}), 200
    except Exception as e:
        return jsonify({'error': f'Something went wrong: {str(e)}'}), 500

@app.route('/exam/doc', methods=['GET'])
def get_pat_for_doc_for_exam():
    user_id = request.args.get('user_id')
    if not user_id:
        return jsonify({'error': 'User ID is required'}), 400
    try:
        patients = system.doctors_patients(user_id)
        return jsonify(patients), 200
    except Exception as e:
        return jsonify({'error': f'Something went wrong: {str(e)}'}), 500
# <><><><><><><> EXAMS <><><><><><><><><>

# <><><><><><><> RESULTS <><><><><><><><><>

@app.route('/results/patient/fetch', methods=['GET'])
def get_results_patient():
    user_id = request.args.get('user_id')  # Get the user ID from query parameters
    if not user_id:
        return jsonify({'error': 'User ID is required'}), 400

    # will return different
    results = system.view_results(user_id, "Patient")
    if results:
        #return results
        return jsonify({'temp': 'Not implemented'}), 404
    else:
        return jsonify({'error': 'No results found for this user'}), 404

@app.route('/results/doctor/fetch', methods=['GET'])
def get_results_doctor():
    user_id = request.args.get('user_id')  # Get the user ID from query parameters
    if not user_id:
        return jsonify({'error': 'User ID is required'}), 400

    # will return different
    results = system.view_results(user_id, "Doctor")
    if results:
        #return results
        return jsonify({'temp': 'Not implemented'}), 404
    else:
        return jsonify({'error': 'No results found for this user'}), 404

# Fetch available exams for a user (to select an exam)
@app.route('/results/exams/fetch', methods=['GET'])
def get_exams_for_results():
    try:
        # Fetch all exams along with associated patient info
        exams = system.get_all_exams()
        if exams:
            return jsonify(exams), 200
        else:
            return jsonify({'error': 'No exams found for this user'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/results/testtypes/<int:exam_id>', methods=['GET'])
def get_test_types_for_exam(exam_id):
    try:
        test_types = system.get_test_types_for_exam(exam_id)
        return jsonify(test_types)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/results/new', methods=['POST'])
def post_result():
    user_id = request.json.get('user_id')
    exam_id = request.json.get('exam_id')  # Exam ID for the test
    result_data = request.json.get('result_data')  # The results data for each test type

    if not user_id or not exam_id or not result_data:
        return jsonify({'error': 'User ID, Exam ID, and result data are required'}), 400

    try:
        # Call the system to create results for the selected exam and test types
        system.create_results(user_id, exam_id, result_data)  # Insert the new results into the system
        return jsonify({'message': 'Results inserted successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/results/fetch', methods=['GET'])
def get_results():
    try:
        # Fetch all test results (no user_id needed)
        results = system.view_all_results()
        if results:
            return jsonify(results), 200
        else:
            return jsonify({'error': 'No results found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500@app.route('/results/del', methods=['DELETE'])

@app.route('/results/del', methods=['DELETE'])
def delete_result():
    result_id = request.json.get('result_id')
    
    if not result_id:
        return jsonify({'error': 'Result ID is required'}), 400

    try:
        # Delete the test result by its ID
        system.delete_results(result_id)
        return jsonify({'message': 'Test result deleted successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
# <><><><><><><> RESULTS <><><><><><><><><>

# <><><><><><><> REPORTS <><><><><><><><><>

# Fetch year and month reports
@app.route('/yearreports/fetch', methods=['GET'])
def get_yearreports():
    reports = system.view_year_n_month_reports()  # Assuming this method fetches the reports from DB
    #return reports
    return jsonify(reports)

@app.route('/yearreports/fetchcontent', methods=['GET'])
def get_yearreport_content():
    report_id = request.args.get('ReportID')
    reports = system.get_report_content(0, report_id)
    return jsonify(reports)

@app.route('/yearreports/delete', methods=['DELETE'])
def delete_report():
    
    report_id = request.json.get('ReportId')
    #try:
    system.delete_report(report_id, 0)
    return jsonify ({'message': 'Report deleted'}), 200
    #except Exception as e:
    #return jsonify ({'error': str(e)}), 500

# Add new year and month report
@app.route('/yearreports/new', methods=['POST'])
def post_yearreport():
    data = request.get_json()
    month = data.get('month')
    year = data.get('year')
    userID = data.get('userID')
    #year = request.json.get('Year')
    system.create_year_n_month_reports(year, month, userID)
    return jsonify({'message': 'report added'})


# Get patients for a doctor (used for selecting patients for reports)
@app.route('/predict/doc', methods=['GET'])
def get_pat_for_doc_for_predict():
    user_id = request.args.get('user_id')
    if not user_id:
        return jsonify({'error': 'User ID is required'}), 400
    try:
        patients = system.doctors_patients(user_id)
        return jsonify(patients), 200
    except Exception as e:
        return jsonify({'error': f'Something went wrong: {str(e)}'}), 500

@app.route('/predict/fetch', methods=['GET'])
def get_predict():
    reports = system.view_predict_reports()  # Assuming this method fetches the reports from DB
    #return reports
    return jsonify(reports)

@app.route('/predict/fetchcontent', methods=['GET'])
def get_predict_content():
    report_id = request.args.get('ReportID')
    reports = system.get_report_content(1, report_id)
    return jsonify(reports)
@app.route('/predict/delete', methods=['DELETE'])
def delete_predict_report():
    
    report_id = request.json.get('ReportId')
    system.delete_report(report_id, 1)
    return jsonify ({'message': 'Report deleted'}), 200
@app.route('/predict/new', methods=['POST'])
def post_predictreport():
    data = request.get_json()
    admin = data.get('AdminID')
    year = data.get('year')
    userID = data.get('userID')
    #year = request.json.get('Year')
    system.create_predict_reports(year, userID, admin)
    return jsonify({'message': 'report added'})

# Add a new prediction report
@app.route('/predict/new', methods=['POST'])
def post_predict():
    data = request.get_json()
    workersid = data.get('workersid')
    healthid = data.get('healthid')
    pdate = data.get('pdate')
    
    if not workersid or not healthid or not pdate:
        return jsonify({'error': 'Missing data'}), 400

    system.create_predict_reports()  # Assuming this method exists
    return jsonify({'message': 'Prediction report created successfully'}), 201

# Get patients for a doctor
@app.route('/predict/doc', methods=['GET'])
def get_pat_for_doc():
    id =0
    patients = system.doctors_patients(id)  # Assuming this method fetches patients for the doctor
    return  patients
    #return jsonify({'temp': 'Not implemented'}), 404

# Fetch all exam types
@app.route('/predict/exam/fetch', methods=['GET'])
def get_exams_for_predict():
    #exams = system.view_exam(
#return exams
    #return jsonify({'temp': 'Not implemented'}), 404
    pass

# <><><><><><><> REPORTS <><><><><><><><><>

# <><><><><><><> MONITOR <><><><><><><><><>

# display Monitor
@app.route('/monitor/fetch', methods=['GET'])
def get_monitors():
    system.view_smart_monitor()
    return jsonify({'temp': 'Not implemented'}), 404

# add Monitor
@app.route('/monitor/new', methods=['POST'])
def post_monitor():
    system.create_smart_monitor()
    return jsonify({'temp': 'Not implemented'}), 404

# delete Monitor
@app.route('/monitor/del', methods=['DELETE'])
def delete_monitor():
    system.delete_smart_monitor()
    return jsonify({'temp': 'Not implemented'}), 404

# edit Monitor
@app.route('/monitor/update', methods=['PATCH'])
def patch_monitor():
    system.change_smart_monitor()
    return jsonify({'temp': 'Not implemented'}), 404


# <><><><><><><> MONITOR <><><><><><><><><>


if __name__ == '__main__':
    app.run(debug=True)

