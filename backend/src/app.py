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

# view patient profile
@app.route('/profile/patient/view', methods=['GET'])
def get_patient_profile():
    # GET PATIENT ID DEOM GET REQUEST
    patient_id =0
    if not patient_id:
        return jsonify({'error': 'Patient ID is required'}), 400

    patient = system.view_patient(patient_id)
    
    if patient:
        return patient
    else:
        return jsonify({'error': 'Patient not found'}), 404

@app.route('/profile/patient/edit', methods=['PATCH'])
def patch_patient_profile():
    system.modify_patient_account()
    return jsonify({''})


# view worker profile
@app.route('/profile/worker/view', methods=['GET'])
def get_worker_profile():
    print("I WAS CALLED")
    # GET PATIENT ID DEOM GET REQUEST
    worker_id = 0
    print(worker_id)
    if not worker_id:
        return jsonify({'error': 'Worker ID is required'}), 400

    worker = system.view_worker(worker_id)

    if worker:
        return worker
    else:
        return jsonify({'error': 'Worker not found'}), 404

@app.route('/profile/worker/edit', methods=['PATCH'])
def patch_worker_profile():
    system.modify_worker_account()
    return jsonify({''})


# <><><><><><><> EXAMS <><><><><><><><><>

# display Exams
@app.route('/exam/fetch', methods=['GET'])
def get_exams():
    system.view_exam()
    pass

# add Exams
@app.route('/exam/new', methods=['POST'])
def post_exams():
    system.prescribe_exam()
    pass

# <><><><><><><> EXAMS <><><><><><><><><>

# <><><><><><><> RESULTS <><><><><><><><><>

# display Results 
@app.route('/results/fetch', methods=['GET'])
def get_results():
    system.view_results()
    pass

# add Results
@app.route('/results/new', methods=['POST'])
def post_result():
    system.create_results()
    pass

# delete Results
@app.route('/results/del', methods=['DELETE'])
def delete_result():
    system.delete_results()
    pass

# <><><><><><><> RESULTS <><><><><><><><><>

# <><><><><><><> REPORTS <><><><><><><><><>

# display Reports
@app.route('/reports/fetch', methods=['GET'])
def get_reports():
    system.view_reports()
    pass

# add Reports
@app.route('/reports/new', methods=['POST'])
def post_report():
    system.create_reports()
    pass

# <><><><><><><> REPORTS <><><><><><><><><>

# <><><><><><><> MONITOR <><><><><><><><><>

# display Monitor
@app.route('/monitor/fetch', methods=['GET'])
def get_monitors():
    system.view_smart_monitor()
    pass

# add Monitor
@app.route('/monitor/new', methods=['POST'])
def post_monitor():
    system.create_smart_monitor()
    pass

# delete Monitor
@app.route('/monitor/del', methods=['DELETE'])
def delete_monitor():
    system.delete_smart_monitor()
    pass

# edit Monitor
@app.route('/monitor/update', methods=['PATCH'])
def patch_monitor():
    system.change_smart_monitor()
    pass


# <><><><><><><> MONITOR <><><><><><><><><>


if __name__ == '__main__':
    app.run(debug=True)

