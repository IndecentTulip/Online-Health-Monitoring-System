import unittest
from unittest.mock import patch
from flask import Flask
from app import app  # Import your Flask app and System class
from system import System

class FlaskTestCase(unittest.TestCase):
    
    # Set up the test client
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
    
    # Test login route
    @patch.object(System, 'log_in')
    def test_post_login_success(self, mock_log_in):
        mock_log_in.return_value = {'message': 'Login successful'}
        response = self.app.post('/login', json={
            'userType': 'patient',
            'email': 'test@example.com',
            'password': 'password123'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('Login successful', response.json['message'])
    
    @patch.object(System, 'log_in')
    def test_post_login_missing_fields(self, mock_log_in):
        response = self.app.post('/login', json={})
        self.assertEqual(response.status_code, 400)
        self.assertIn('Missing required fields', response.json['error'])
    
    @patch.object(System, 'log_in')
    def test_post_login_invalid_user_type(self, mock_log_in):
        response = self.app.post('/login', json={
            'userType': 'invalid_type',
            'email': 'test@example.com',
            'password': 'password123'
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn('Invalid userType', response.json['error'])
    
    # Test register route for patient
    @patch.object(System, 'create_patient_account')
    def test_post_register_patient_success(self, mock_create_patient_account):
        mock_create_patient_account.return_value = {'message': 'Registration successful'}
        response = self.app.post('/register', json={
            'patientName': 'John Doe',
            'email': 'john.doe@example.com',
            'phoneNumber': '123456789',
            'dob': '1990-01-01',
            'docID': 21004,  # Doctor ID from your data
            'password': 'password123'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('Registration successful', response.json['message'])
    
    @patch.object(System, 'create_patient_account')
    def test_post_register_patient_missing_fields(self, mock_create_patient_account):
        response = self.app.post('/register', json={})
        self.assertEqual(response.status_code, 400)
        self.assertIn('Missing required fields', response.json['error'])
    
    # Test patient profile view
    @patch.object(System, 'view_patient')
    def test_get_patient_profile_success(self, mock_view_patient):
        # Simulate patient profile fetching
        mock_view_patient.return_value = {'patient_id': 10031, 'name': 'Bob Ricky'}
        response = self.app.get('/profile/patient/view?patient_id=10031')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['patient_id'], 10031)
    
    @patch.object(System, 'view_patient')
    def test_get_patient_profile_not_found(self, mock_view_patient):
        mock_view_patient.return_value = None
        response = self.app.get('/profile/patient/view?patient_id=999')
        self.assertEqual(response.status_code, 404)
        self.assertIn('Patient not found', response.json['error'])

    # Test delete patient route
    @patch.object(System, 'delete_patient_account')
    def test_delete_patient_success(self, mock_delete_patient_account):
        mock_delete_patient_account.return_value = True
        response = self.app.delete('/accounts/patient/del', json={'patient_id': 10031})
        self.assertEqual(response.status_code, 200)
        self.assertIn('Patient deleted successfully', response.json['message'])
    
    @patch.object(System, 'delete_patient_account')
    def test_delete_patient_missing_id(self, mock_delete_patient_account):
        response = self.app.delete('/accounts/patient/del', json={})
        self.assertEqual(response.status_code, 400)
        self.assertIn('Patient ID is required', response.json['error'])

    # Test exam fetch route
    @patch.object(System, 'get_exam_types')
    def test_get_exam_types_success(self, mock_get_exam_types):
        # Assume get_exam_types would return a list of exam types based on your data
        mock_get_exam_types.return_value = ['Blood', 'CT-Scan', 'Ultrasound']
        response = self.app.get('/exam/fetch_exam_types')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, ['Blood', 'CT-Scan', 'Ultrasound'])

    # Test creating new result
    @patch.object(System, 'create_results')
    def test_post_result_success(self, mock_create_results):
        # Simulate result creation for an exam
        mock_create_results.return_value = True
        response = self.app.post('/results/new', json={
            'user_id': 10031,  # Patient ID
            'exam_id': 33025,  # Exam ID from your data
            'result_data': {'test_type': 'Blood Test Iron', 'result': 4.0}
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('Results inserted successfully', response.json['message'])
    
    @patch.object(System, 'create_results')
    def test_post_result_missing_fields(self, mock_create_results):
        response = self.app.post('/results/new', json={})
        self.assertEqual(response.status_code, 400)
        self.assertIn('User ID, Exam ID, and result data are required', response.json['error'])


if __name__ == '__main__':
    unittest.main()

