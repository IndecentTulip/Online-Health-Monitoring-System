from flask import Flask, request, jsonify
from flask_cors import CORS
import psycopg2

app = Flask(__name__)
CORS(app)

# Connect to PostgreSQL database
def get_db_connection():
    conn = psycopg2.connect(
        host='localhost',
        user='root',
        password='good_day',
        dbname='jlabs'
    )
    return conn

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

