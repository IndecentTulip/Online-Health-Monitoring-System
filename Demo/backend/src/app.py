from flask import Flask, request, jsonify
from flask_cors import CORS
import psycopg2

app = Flask(__name__)
CORS(app)

def read_credentials(file_path):
    credentials = {}
    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            if line and '=' in line:  # Ensure the line is not empty and contains '='
                key, value = line.split('=', 1)  # Split only on the first '='
                credentials[key] = value
    return credentials


# Read credentials from the file
credentials = read_credentials('./Demo/backend/src/credentials.txt')
user = credentials.get('user')
password = credentials.get('password')

# Connect to PostgreSQL database
def get_db_connection():
    conn = psycopg2.connect(
        host='localhost',
        user=user,
        password=password, 
        dbname='jlabs'
    )
    return conn

# this will be used by front end
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data['username']
    password = data['password']

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM users WHERE username = %s AND password = %s', (username, password))
    user = cur.fetchone()
    cur.close()
    conn.close()

    if user:
        return jsonify({'user': {'username': username}})
    return jsonify({'error': 'Invalid credentials'}), 401

if __name__ == '__main__':
    app.run(debug=True)

