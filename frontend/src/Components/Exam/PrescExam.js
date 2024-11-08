import { useNavigate } from 'react-router-dom';
import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './PrescExam.css';  // Assuming this file contains CSS for the form

const PrescExam = ({ userId }) => {
  const navigate = useNavigate();

  const [patients, setPatients] = useState([]);  // List of patients for the doctor
  const [patientId, setPatientId] = useState('');  // Selected patient ID
  const [content, setContent] = useState('');  // Content (e.g., exam notes)
  const [error, setError] = useState(null);  // Error handling

  // Fetch the list of patients assigned to the doctor
  const fetchPatients = async () => {
    try {
      const response = await axios.get('http://localhost:5000/exam/doc', {
        params: { user_id: userId },
      });

      // Assuming response.data is an array of patient objects {id, name}
      if (Array.isArray(response.data)) {
        setPatients(response.data);  // Store the fetched patients in the state
      } else {
        setError('Invalid data format for patients');
      }
    } catch (err) {
      setError('Failed to fetch patients');
    }
  };

  // Handle form field changes
  const handleChange = (e) => {
    const { name, value } = e.target;
    if (name === 'patientId') {
      setPatientId(value);  // Set selected patient ID
    } else if (name === 'content') {
      setContent(value);  // Set exam content
    }
  };

  // Submit the form to create a new exam
  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const examData = { patientId, content };
      const response = await axios.post('http://localhost:5000/exam/new', examData);
      if (response.status === 200) {
        // Redirect to another page (e.g., exam details page or dashboard)
        navigate('/exams');
      } else {
        setError('Failed to create exam');
      }
    } catch (err) {
      setError('Error submitting the exam');
    }
  };

  // Fetch patients on component mount
  useEffect(() => {
    if (userId) {
      fetchPatients();  // Fetch the patients when the component mounts
    }
  }, [userId]);

  return (
    <div className="presc-exam">
      <h2>Prescribe Exam</h2>

      {/* Display error if exists */}
      {error && <div style={{ color: 'red' }}>{error}</div>}

      {/* Exam prescription form */}
      <form onSubmit={handleSubmit}>
        <div>
          <label>
            Select Patient:
            <select
              name="patientId"
              value={patientId}
              onChange={handleChange}
              required
            >
              <option value="">Select a patient</option>
              {patients.map((patient) => (
                <option key={patient.id} value={patient.id}>
                  {patient.name}
                </option>
              ))}
            </select>
          </label>
        </div>

        <div>
          <label>
            Exam Content (Notes):
            <textarea
              name="content"
              value={content}
              onChange={handleChange}
              required
              placeholder="Enter exam instructions or notes"
            />
          </label>
        </div>

        <button type="submit">Submit Exam</button>
      </form>
    </div>
  );
};

export default PrescExam;

