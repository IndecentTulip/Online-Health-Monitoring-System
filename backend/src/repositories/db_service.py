import psycopg2

class DBService:
    def __init__(self):
        self.credentials = self.read_credentials('./credentials.txt')
        self.user = self.credentials.get('user')
        self.password = self.credentials.get('password')

    def read_credentials(self, file_path):
        credentials = {}
        with open(file_path, 'r') as file:
            for line in file:
                line = line.strip()
                if line and '=' in line:
                    key, value = line.split('=', 1)
                    credentials[key] = value
        return credentials

    def get_db_connection(self):
        conn = psycopg2.connect(
            host='localhost',
            user=self.user,
            password=self.password, 
            dbname='jlabs'
        )
        return conn


