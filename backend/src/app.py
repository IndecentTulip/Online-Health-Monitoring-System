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
            return jsonify({'error': 'Invalid login credentials'}), 400  # Return an error response if None

        return response 

    except KeyError as e:
        return jsonify({'error': f'Missing key: {str(e)}'}), 400
    except Exception as e:
        return jsonify({'error': f'Something went wrong: {str(e)}'}), 500


# Used by Components/Auth/Register (to register a patient)
@app.route('/register', methods=['POST'])
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


# <><><><><><><> COMMON <><><><><><><><><>

# View patient profile
@app.route('/profile/patient/view', methods=['GET'])
def get_patient_profile():
    patient_id = request.args.get('patient_id')
    if not patient_id:
        return jsonify({'error': 'Patient ID is required'}), 400

    patient = system.view_patient(patient_id)
    
    if patient:
        return patient
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
        system.modify_patient_account()
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
        system.modify_worker_account()
        return jsonify({'message': 'Worker profile updated successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
# <><><><><><><> COMMON <><><><><><><><><>

# <><><><><><><> EXAMS <><><><><><><><><>

# display Exams
@app.route('/exam/fetch', methods=['GET'])
def get_exams():
    system.view_exam()
    return jsonify({'temp': 'Not implemented'}), 404

# add Exams
@app.route('/exam/new', methods=['POST'])
def post_exams():
    system.prescribe_exam()
    return jsonify({'temp': 'Not implemented'}), 404

# <><><><><><><> EXAMS <><><><><><><><><>

# <><><><><><><> RESULTS <><><><><><><><><>

# Fetch results for a specific user
@app.route('/results/fetch', methods=['GET'])
def get_results():
    user_id = request.args.get('user_id')  # Get the user ID from query parameters
    if not user_id:
        return jsonify({'error': 'User ID is required'}), 400

    #results = system.view_results(user_id)  # Retrieve results from the system
    results = system.view_results(user_id)
    if results:
        return results
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

# delete Results
@app.route('/results/del', methods=['DELETE'])
def delete_result():
    system.delete_results()
    return jsonify({'temp': 'Not implemented'}), 404

# <><><><><><><> RESULTS <><><><><><><><><>

# <><><><><><><> REPORTS <><><><><><><><><>

# display Reports
@app.route('/reports/fetch', methods=['GET'])
def get_reports():
    system.view_reports()
    return jsonify({'temp': 'Not implemented'}), 404

# add Reports
@app.route('/reports/new', methods=['POST'])
def post_report():
    system.create_reports()
    return jsonify({'temp': 'Not implemented'}), 404

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

