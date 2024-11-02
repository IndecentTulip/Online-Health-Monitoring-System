from flask import Flask, request, jsonify
from flask_cors import CORS
from system import System

app = Flask(__name__)
CORS(app)

# Create an instance of the System class
system = System()

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



if __name__ == '__main__':
    app.run(debug=True)

