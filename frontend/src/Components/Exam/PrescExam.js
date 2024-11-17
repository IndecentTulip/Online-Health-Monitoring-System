import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './PrescExam.css';

const PrescExam = ({ userId }) => {
  const [patients, setPatients] = useState([]);
  const [patientId, setPatientId] = useState('');
  const [testTypes, setTestTypes] = useState([]);
  const [selectedTestTypes, setSelectedTestTypes] = useState([]);
  const [examTypeByTestType, setExamTypeByTestType] = useState({});
  const [content, setContent] = useState('');
  const [error, setError] = useState(null);
  const [confirmationMessage, setConfirmationMessage] = useState('');

  useEffect(() => {
    const fetchPatients = async () => {
      try {
        const response = await axios.get('http://localhost:5000/exam/doc', { params: { user_id: userId } });
        setPatients(response.data);
      } catch {
        setError('Failed to fetch patients');
      }
    };

    const fetchTestTypes = async () => {
      try {
        const response = await axios.get('http://localhost:5000/exam/fetch_test_types');
        const testTypeMap = {};
        response.data.forEach((test) => (testTypeMap[test.testtype] = test.examtype));
        setTestTypes(response.data);
        setExamTypeByTestType(testTypeMap);
      } catch {
        setError('Failed to fetch test types');
      }
    };

    if (userId) {
      fetchPatients();
      fetchTestTypes();
    }
  }, [userId]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!selectedTestTypes.length) {
      setError('At least one test type must be selected.');
      return;
    }
    try {
      for (let testType of selectedTestTypes) {
        const response = await axios.post('http://localhost:5000/exam/new', {
          patientId,
          content,
          examType: examTypeByTestType[testType],
          testTypes: [testType],
          doctorId: userId,
        });
        if (response.status !== 200) throw new Error();
      }
      setConfirmationMessage('Exam prescribed successfully!');
    } catch {
      setError('Error submitting the exam');
    }
  };

  return (
    <div className="presc-exam-container">
      <h2 className="presc-exam-header">Prescribe Exam</h2>
      {error && <div className="presc-exam-error">{error}</div>}
      {confirmationMessage && <div className="presc-exam-confirmation">{confirmationMessage}</div>}
      <form onSubmit={handleSubmit}>
        <div className="presc-exam-patient">
          <label>Select Patient:</label>
          <select name="patientId" value={patientId} onChange={(e) => setPatientId(e.target.value)} required>
            <option value="">Select a patient</option>
            {patients.map((patient) => (
              <option key={patient.id} value={patient.id}>
                {patient.name}
              </option>
            ))}
          </select>
        </div>
        <div className="presc-exam-test-type">
          <label>Select Test Types:</label>
          <ul className="test-type-list">
            {testTypes.map((test) => (
              <li key={test.testtype} className="test-type-item">
                <label>
                  <input
                    type="checkbox"
                    name="testTypes"
                    value={test.testtype}
                    onChange={(e) => {
                      setSelectedTestTypes((prev) =>
                        e.target.checked
                          ? [...prev, test.testtype]
                          : prev.filter((type) => type !== test.testtype)
                      );
                    }}
                  />
                  {test.testtype} (Associated Exam Type: {test.examtype})
                </label>
              </li>
            ))}
          </ul>
        </div>
        <div className="presc-exam-notes">
          <label>Exam Content (Notes):</label>
          <textarea
            name="content"
            value={content}
            onChange={(e) => setContent(e.target.value)}
            required
            placeholder="Enter exam instructions or notes"
          />
        </div>
        <button className="presc-exam-submit-btn" type="submit">
          Submit Exam
        </button>
      </form>
    </div>
  );
};

export default PrescExam;
