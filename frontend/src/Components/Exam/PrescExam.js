import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './PrescExam.css';

const PrescExam = ({ userId }) => {

  const [patients, setPatients] = useState([]);
  const [patientId, setPatientId] = useState('');
  const [testTypes, setTestTypes] = useState([]);
  const [selectedTestTypes, setSelectedTestTypes] = useState([]);
  const [examTypeByTestType, setExamTypeByTestType] = useState({}); // Mapping of test types to exam types
  const [content, setContent] = useState('');
  const [error, setError] = useState(null);
  const [confirmationMessage, setConfirmationMessage] = useState(''); // Confirmation message

  // Fetch patients assigned to the doctor
  const fetchPatients = async () => {
    try {
      const response = await axios.get('http://localhost:5000/exam/doc', {
        params: { user_id: userId },
      });
      setPatients(response.data);
    } catch (err) {
      setError('Failed to fetch patients');
    }
  };

  // Fetch test types and their associated exam types
  const fetchTestTypes = async () => {
    try {
      const response = await axios.get('http://localhost:5000/exam/fetch_test_types');
      setTestTypes(response.data);

      // Generate mapping for test types to exam types
      const testTypeExamMap = {};
      response.data.forEach((test) => {
        testTypeExamMap[test.testtype] = test.examtype;
      });
      setExamTypeByTestType(testTypeExamMap);
    } catch (err) {
      setError('Failed to fetch test types');
    }
  };

  useEffect(() => {
    if (userId) {
      fetchPatients();
      fetchTestTypes();
    }
  }, [userId]);

  // Handle changes in form fields
  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;

    if (name === 'patientId') {
      setPatientId(value);
    } else if (name === 'content') {
      setContent(value);
    } else if (name === 'testTypes') {
      if (checked) {
        setSelectedTestTypes([...selectedTestTypes, value]);
      } else {
        setSelectedTestTypes(selectedTestTypes.filter((test) => test !== value));
      }
    }
  };

  // Handle form submission
  const handleSubmit = async (e) => {
    e.preventDefault();

    if (selectedTestTypes.length === 0) {
      setError('At least one test type must be selected.');
      return;
    }

    try {
      // Loop through selected test types and send separate requests for each
      for (let testType of selectedTestTypes) {
        const examType = examTypeByTestType[testType];

        // Prepare exam data for each test type
        const examData = {
          patientId,
          content,
          examType: examType,  // Corresponding exam type based on test type
          testTypes: [testType],  // Only send the selected test type
          doctorId: userId,
        };

        const response = await axios.post('http://localhost:5000/exam/new', examData);
        if (response.status === 200) {
          setConfirmationMessage('Exam prescribed successfully!');
        } else {
          setError('Failed to create exam');
          return;
        }
      }

    } catch (err) {
      setError('Error submitting the exam');
    }
  };

  return (
    <div className="presc-exam">
      <h2>Prescribe Exam</h2>
      {error && <div style={{ color: 'red' }}>{error}</div>}
      {confirmationMessage && <div style={{ color: 'green' }}>{confirmationMessage}</div>}

      <form onSubmit={handleSubmit}>
        <div className = "patient-id">
          <label className= "SelectPatient">Select Patient:</label>
          <select name="patientId" value={patientId} onChange={handleChange} required>
            <option value="">Select a patient</option>
            {patients.map((patient) => (
              <option key={patient.id} value={patient.id}>
                {patient.name}
              </option>
            ))}
          </select>
        </div>

        <div className = "test-type">
          <label>Select Test Types:</label>
          {testTypes.map((test) => (
            <div key={test.testtype}>
              <label>
                <input
                  type="checkbox"
                  name="testTypes"
                  value={test.testtype}
                  onChange={handleChange}
                />
                {test.testtype} (Associated Exam Type: {test.examtype})
              </label>
            </div>
          ))}
        </div>

        <div className = "exam-content">
          <label classNmae = "Notes">Exam Content (Notes):</label>
          <textarea
            name="content"
            value={content}
            onChange={handleChange}
            required
            placeholder="Enter exam instructions or notes"
          />
        </div>

        <button type="submit">Submit Exam</button>
      </form>
    </div>
  );
};

export default PrescExam;

