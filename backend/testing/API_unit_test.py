from locust import HttpUser, task, between

class AppTestUser(HttpUser):
    host = "http://127.0.0.1:5000"
    wait_time = between(1, 3)

    @task
    def login_pat(self):
        user_data = {
            "userType": "patient",
            "email": "Jojo.g@outlook.com",
            "password": "******"
        }
        response = self.client.post("/login", json=user_data)
        if response.status_code == 200:
            print("[ OK ] Login patient test")
        else:
            print(f"[FAILED] Login patient test {response.status_code}")
    
    @task
    def login_work(self):
        user_data = {
            "userType": "worker",
            "email": "Karen.Smith@jlabemail.com",
            "password": "******"
        }
        response = self.client.post("/login", json=user_data)
        if response.status_code == 200:
            print("[ OK ] Login worker test")
        else:
            print(f"[FAILED] Login worker test {response.status_code}")
    
    @task
    def login_fail(self):
        user_data = {
            "userType": "worker",  # Remove random choice
            "email": "user@example.com",
            "password": "password123"
        }
        response = self.client.post("/login", json=user_data)
        if response.status_code == 200:
            print("[FAILED] Login fail test")
        else:
            print(f"[ OK ] Login fail test")
    
    @task
    def register(self):
        patient_data = {
            "patientName": "John Doe",
            "email": "john.doe@example.com",
            "phoneNumber": "1234567890",
            "dob": "1990-01-01",
            "docID": 21004,
            "password": "password123"
        }
        response = self.client.post("/register", json=patient_data)
        if response.status_code == 200:
            print("[ OK ] Registration")
        else:
            print(f"[FAILED] Registration {response.status_code}")
    
    @task
    def get_patient_profile(self):
        patient_id = 10031
        response = self.client.get(f"/profile/patient/view?patient_id={patient_id}")
        if response.status_code == 200:
            print("[ OK ] Patient profile fetched")
        else:
            print(f"[FAILED] Patient profile fetched {response.status_code}")
    
    @task
    def get_doctors(self):
        response = self.client.get("/register")
        if response.status_code == 200:
            print("[ OK ] Doctors fetched")
        else:
            print(f"[FAILED] Doctors fetched {response.status_code}")

    @task
    def post_exam(self):
        exam_data = {
            "examType": "Blood",
            "patientId": 10036,
            "doctorId": 21004,
            "testTypes": ["Blood Test Iron",],
            "content": "unit test"
        }
        response = self.client.post("/exam/new", json=exam_data)
        if response.status_code == 200:
            print("[ OK ] Exam prescribed")
            self.stop()
        else:
            print(f"[FAILED] Exam prescribed {response.status_code}")


