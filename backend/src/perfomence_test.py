from locust import HttpUser, task, between
import random
import json

print("YES, IT'S OK IF SOMETHING IS FAILING(it works as intended) WE ARE TESTING PERFOMENCE")

class AppTestUser(HttpUser):
    # Set a wait time between tasks (in seconds)
    host = "http://127.0.0.1:5000"
    wait_time = between(1, 3)

    @task(2)
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

    @task(2)
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

    # YES THIS TEST MUST FAIL
    @task(2)
    def login_fail(self):
        user_data = {
            "userType": random.choice(['patient', 'worker']),
            "email": "user@example.com",
            "password": "password123"
        }
        response = self.client.post("/login", json=user_data)
        if response.status_code == 200:
            print("[FAILED] Login fail test")
        else:
            print(f"[ OK ] Login fail test")


    # WILL START FAILING AFTER THE FIST TIME
    @task(1)
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
            print("[ OK ] Registration ")
        else:
            print(f"[FAILED] Registration {response.status_code}")

    @task(1)
    def get_patient_profile(self):
        patient_id = 10031
        response = self.client.get(f"/profile/patient/view?patient_id={patient_id}")
        if response.status_code == 200:
            print("[ OK ] Patient profile fetche")
        else:
            print(f"[FAILED] Patient profile fetche {response.status_code}")

    @task(1)
    def get_worker_profile(self):
        worker_id = 21001
        response = self.client.get(f"/profile/worker/view?worker_id={worker_id}")
        if response.status_code == 200:
            print("[ OK ] Worker profile fetche")
        else:
            print(f"[FAILED] Worker profile fetche {response.status_code}")


    @task(1)
    def get_doctors(self):
        response = self.client.get("/register")
        if response.status_code == 200:
            print("[ OK ] Doctors fetched ")
        else:
            print(f"[FAILED] Doctors fetched  {response.status_code}")


    # WILL START FAILING AFTER THE FIST TIME
    @task(1)
    def post_exam(self):
        exam_data = {
            "examType": "Blood",
            "patientId": 10036,
            "testTypes": ["Blood Test Iron"]
        }
        response = self.client.post("/exam/new", json=exam_data)
        if response.status_code == 200:
            print("[ OK ] Exam prescribed ")
        else:
            print(f"[FAILED] Exam prescribed  {response.status_code}")


