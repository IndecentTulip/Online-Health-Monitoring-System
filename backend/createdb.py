import psycopg2

def read_credentials(file_path):
    credentials = {}
    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            if line and '=' in line:
                key, value = line.split('=', 1)
                credentials[key] = value
    return credentials

# Read credentials from the file
credentials = read_credentials('./backend/src/credentials.txt')
user = credentials.get('user')
password = credentials.get('password')

def get_db_connection(dbname):
    return psycopg2.connect(
        host='localhost',
        user=user,
        password=password, 
        dbname=dbname
    )

def execute_sql_file(conn, file_path):
    with open(file_path, 'r') as file:
        sql = file.read()
    with conn.cursor() as cur:
        cur.execute(sql)
    conn.commit()

def create_database():
    # Connect to the default database to create a new one
    conn = psycopg2.connect(
        host='localhost',
        user=user,
        password=password,
        dbname='postgres'  # Connect to the default database
    )

    conn.autocommit = True  # Enable autocommit mode

    with conn.cursor() as cur:
        cur.execute("DROP DATABASE IF EXISTS jlabs;")
        cur.execute("CREATE DATABASE jlabs WITH ENCODING 'utf8';")
    
    conn.close()

# Create the database
create_database()

    # Run schema.sql on the 'jlabs' database
conn = get_db_connection('jlabs')
execute_sql_file(conn, './database/schema.sql')
conn.close()

# Run seed.sql on the 'jlabs' database
conn = get_db_connection('jlabs')
execute_sql_file(conn, './database/seed.sql')
conn.close()

# Run test.sql on the 'jlabs' database
conn = get_db_connection('jlabs')
execute_sql_file(conn, './database/test.sql')
conn.close()


