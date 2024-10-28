from flask import Flask
from flask_cors import CORS
from system import System

app = Flask(__name__)
CORS(app)

# Create an instance of the System class
system = System()

@app.route('/login', methods=['POST'])
def login():
    return "test"

if __name__ == '__main__':
    app.run(debug=True)

