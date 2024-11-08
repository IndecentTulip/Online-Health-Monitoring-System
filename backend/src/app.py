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
        
        response = system.register(patientName, email, phoneNumber, dob, docID, password)
        
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
@app.route('/profile/patient', methods=['GET'])
def get_patient_profile():
    patient_id = request.args.get('id')  # Extract patient ID from query string
    if not patient_id:
        return jsonify({'error': 'Patient ID is required'}), 400

    patient = system.view_patient(patient_id)
    
    if patient:
        return jsonify(patient)
    else:
        return jsonify({'error': 'Patient not found'}), 404

# view worker profile
@app.route('/profile/worker', methods=['GET'])
def get_worker_profile():
    worker_id = request.args.get('id')  # Extract worker ID from query string
    if not worker_id:
        return jsonify({'error': 'Worker ID is required'}), 400

    worker = system.view_worker(worker_id)

    if worker:
        return jsonify(worker)
    else:
        return jsonify({'error': 'Worker not found'}), 404

# <><><><><><><> EXAMS <><><><><><><><><>

# display Exams
@app.route('/exam/fetch', methods=['GET'])
def get_exams():
    pass

# add Exams
@app.route('/exam/new', methods=['POST'])
def post_exams():
    pass

# <><><><><><><> EXAMS <><><><><><><><><>

# <><><><><><><> RESULTS <><><><><><><><><>

# display Results 
@app.route('/results/fetch', methods=['GET'])
def get_results():
    pass

# add Results
@app.route('/results/new', methods=['POST'])
def post_result():
    pass

# delete Results
@app.route('/results/del', methods=['DELETE'])
def delete_result():
    pass

# <><><><><><><> RESULTS <><><><><><><><><>

# <><><><><><><> REPORTS <><><><><><><><><>

# display Reports
@app.route('/reports/fetch', methods=['GET'])
def get_reports():
    pass

# add Reports
@app.route('/reports/new', methods=['POST'])
def post_report():
    pass

# <><><><><><><> REPORTS <><><><><><><><><>

# <><><><><><><> MONITOR <><><><><><><><><>

# display Monitor
@app.route('/monitor/fetch', methods=['GET'])
def get_monitors():
    pass

# add Monitor
@app.route('/monitor/new', methods=['POST'])
def post_monitor():
    pass

# delete Monitor
@app.route('/monitor/del', methods=['DELETE'])
def delete_monitor():
    pass

# edit Monitor
@app.route('/monitor/update', methods=['PATCH'])
def patch_monitor():
    pass


# <><><><><><><> MONITOR <><><><><><><><><>


if __name__ == '__main__':
    app.run(debug=True)

