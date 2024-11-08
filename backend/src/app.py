from os import stat
from flask import Flask, request, jsonify
from flask_cors import CORS
from system import System

app = Flask(__name__)
CORS(app)

# Create an instance of the System class
system = System()

# Used by Components/Auth/Login
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    userType = data['userType']
    # userType is ether "patient" or "worker"
    email = data['email']
    password = data['password']

    response = system.log_in(userType, email, password)

    if response is None:
        return jsonify({'error': 'Invalid login credentials'}), 400  # Return an error response if None

    return response 

# <><><><><><><> AUTH <><><><><><><><><>

# Used by Components/Auth/Register
# to register a patient
@app.route('/register', methods=['POST'])
def register():
    data = request.json
    patientName = data['patientName']
    email = data['email']
    phoneNumber = data['phoneNumber']
    dob = data['dob']
    docID = data['docID']
    password = data['password']
    print(patientName, docID, dob)
    response = system.register(patientName, email, phoneNumber, dob, docID, password)

    return response

# Used by Components/Auth/Register
# to get doctors that exist(because it is required by dabatabse)
@app.route('/register', methods=['GET'])
def getDoctors():
    return system.get_doc_list_form()


# <><><><><><><> AUTH <><><><><><><><><>


# <><><><><><><> COMMON <><><><><><><><><>


# <><><><><><><> COMMON <><><><><><><><><>

if __name__ == '__main__':
    app.run(debug=True)

