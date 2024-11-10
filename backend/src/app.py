from os import stat
from flask import Flask, request, jsonify
from flask_cors import CORS
from system import System

app = Flask(__name__)
CORS(app)

# Create an instance of the System class
system = System()

# <><><><><><><> AUTH <><><><><><><><><>

# Used by Components/Auth/Login


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

# View patient profile
@app.route('/profile/patient/view', methods=['GET'])
def get_patient_profile():
    patient_id = request.args.get('patient_id')
    if not patient_id:
        return jsonify({'error': 'Patient ID is required'}), 400

    patient = system.view_patient(patient_id)
    
    if patient:
        return patient
        #return jsonify({'temp': 'Not implemented'}), 404
    else:
        return jsonify({'error': 'Patient not found'}), 404

@app.route('/profile/patient/edit', methods=['PATCH'])
def patch_patient_profile():
    patient_id = request.args.get('patient_id')
    if not patient_id:
        return jsonify({'error': 'Patient ID is required'}), 400

    # Get the updated data from the request
    updated_data = request.json
    if not updated_data:
        return jsonify({'error': 'No data provided for update'}), 400

    # Call the system to modify the patient account with the provided data
    try:
        #system.modify_patient_account(patient_id, updated_data)
        system.modify_patient_account(patient_id)
        return jsonify({'message': 'Patient profile updated successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

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
        system.modify_worker_account(worker_id)
        return jsonify({'message': 'Worker profile updated successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# <><><><><><><> PROFILE <><><><><><><><><>

# <><><><><><><> ACCOUNT <><><><><><><><><>

# Fetch all workers (No filtering on the backend)
@app.route('/accounts/workers/fetch', methods=['GET'])
def get_workers():
    workers = system.view_all_workers()  # Assuming this method returns a list of workers
    return workers
    #return jsonify({'temp': 'Not implemented'}), 404

# Fetch all patients (No filtering on the backend)
@app.route('/accounts/patient/fetch', methods=['GET'])
def get_patients():
    patients = system.view_all_patients()  # Assuming this method returns a list of patients
    return patients
    #return jsonify({'temp': 'Not implemented'}), 404

# Add a new worker (POST request)
@app.route('/accounts/workers/add', methods=['POST'])
def add_workers():
    data = request.get_json()
    worker_name = data.get('worker_name')
    worker_email = data.get('worker_email')
    worker_role = data.get('worker_role')
    
    if not worker_name or not worker_email or not worker_role:
        return jsonify({'error': 'Worker data is incomplete'}), 400

    #system.add_worker(worker_name, worker_email, worker_role)  # Add worker to the system
    return jsonify({'message': 'Worker added successfully'}), 201

# Delete a patient (DELETE request)
@app.route('/accounts/patient/del', methods=['DELETE'])
def delete_patients():
    data = request.get_json()
    patient_id = data.get('patient_id')
    
    if not patient_id:
        return jsonify({'error': 'Patient ID is required'}), 400

    system.create_worker_account(patient_id)  # Assuming this method exists
    return jsonify({'message': 'Patient deleted successfully'}), 200

# Delete a worker (DELETE request)
@app.route('/accounts/workers/del', methods=['DELETE'])
def delete_workers():
    data = request.get_json()
    worker_id = data.get('worker_id')
    
    if not worker_id:
        return jsonify({'error': 'Worker ID is required'}), 400

    #system.delete_worker_account(worker_id)  # Assuming this method exists
    system.delete_worker_account()  # Assuming this method exists
    return jsonify({'message': 'Worker deleted successfully'}), 200
@app.route('/accounts/workers/update', methods=['PATCH'])
def patch_workers():
    id =0
    system.modify_worker_account(id)
    return jsonify({'temp': 'Not implemented'}), 404

@app.route('/accounts/patient/update', methods=['PATCH'])
def patch_patients():
    id =0
    system.modify_patient_account(id)
    return jsonify({'temp': 'Not implemented'}), 404


# <><><><><><><> ACCOUNT <><><><><><><><><>

# <><><><><><><> EXAMS <><><><><><><><><>

# display Exams
@app.route('/exam/fetch', methods=['GET'])
def get_exams_1():
    system.view_exam()
    # THIS SHIT WILL RETURN NOT ONLY EXAM TYPES
    # BUT ALSO BLOOD TEST TYPES
    return jsonify({'temp': 'Not implemented'}), 404

# add Exams
@app.route('/exam/new', methods=['POST'])
def post_exams():
    system.prescribe_exam()
    return jsonify({'temp': 'Not implemented'}), 404

# get Patients of the Doctor (IS NEEDED TO ADD EXAM) 
@app.route('/exam/doc', methods=['GET'])
def get_pat_for_doc_1():
    system.doctors_patients()
    return jsonify({'temp': 'Not implemented'}), 404

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

# Add new test results for a specific user
@app.route('/results/new', methods=['POST'])
def post_result():
    user_id = request.json.get('user_id')
    result_data = request.json.get('result_data')  # The test results to be inserted

    if not user_id or not result_data:
        return jsonify({'error': 'User ID and result data are required'}), 400

    try:
        #system.create_results(user_id, result_data)  # Insert the new result in the system
        system.create_results()  # Insert the new result in the system
        return jsonify({'message': 'Result inserted successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/results/fetch', methods=['GET'])
def get_results():
    # will return different
    results = system.view_all_results()
    if results:
        #return results
        return jsonify({'temp': 'Not implemented'}), 404
    else:
        return jsonify({'error': 'No results found for this user'}), 404

# delete Results
@app.route('/results/del', methods=['DELETE'])
def delete_result():
    system.delete_results()
    return jsonify({'temp': 'Not implemented'}), 404

# <><><><><><><> RESULTS <><><><><><><><><>

# <><><><><><><> REPORTS <><><><><><><><><>

# Fetch year and month reports
@app.route('/yearreports/fetch', methods=['GET'])
def get_yearreports():
    reports = system.view_year_n_month_reports()  # Assuming this method fetches the reports from DB
    return reports
    #return jsonify({'temp': 'Not implemented'}), 404

# Add new year and month report
@app.route('/yearreports/new', methods=['POST'])
def post_yearreport():
    data = request.get_json()
    workersid = data.get('workersid')
    monthoryear = data.get('monthoryear')
    summarydate = data.get('summarydate')
    timeperiod = data.get('timeperiod')
    
    if not workersid or not monthoryear or not summarydate or not timeperiod:
        return jsonify({'error': 'Missing data'}), 400

    #system.create_year_n_month_reports(workersid, monthoryear, summarydate, timeperiod)  # Assuming this method exists
    system.create_year_n_month_reports()  # Assuming this method exists
    return jsonify({'message': 'Year and month report created successfully'}), 201

# Get patients for a doctor (used for selecting patients for reports)
@app.route('/predict/doc', methods=['GET'])
def get_pat_for_doc_3():
    patients = system.doctors_patients()  # Assuming this method returns a list of patients assigned to the doctor
    return patients
    #return jsonify({'temp': 'Not implemented'}), 404

@app.route('/predict/fetch', methods=['GET'])
def get_predict():
    reports = system.view_predict_reports()  # Assuming this returns a list of prediction reports
    return reports
    #return jsonify({'temp': 'Not implemented'}), 404

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
    patients = system.doctors_patients()  # Assuming this method fetches patients for the doctor
    return  patients
    #return jsonify({'temp': 'Not implemented'}), 404

# Fetch all exam types
@app.route('/predict/exam/fetch', methods=['GET'])
def get_exams():
    exams = system.view_exam()  # Assuming this method returns exam types
    return exams
    #return jsonify({'temp': 'Not implemented'}), 404

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

