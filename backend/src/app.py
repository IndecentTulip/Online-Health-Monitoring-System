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

    conformation = system.log_in(userType, email, password)
    if (conformation):
        return jsonify()



if __name__ == '__main__':
    app.run(debug=True)

