import React, { useEffect, useState } from 'react';
import axios from 'axios';

const InsertTestResults = ({ userId }) => {
  const [exams, setExams] = useState([]);
  const [selectedExam, setSelectedExam] = useState('');
  const [testTypes, setTestTypes] = useState([]);
  const [newResult, setNewResult] = useState('');
  const [error, setError] = useState(null);
  const [successMessage, setSuccessMessage] = useState(null);
  const [loading, setLoading] = useState(false);

  // Fetch available exams for the user
  const fetchExams = async () => {
    try {
      const response = await axios.get('http://localhost:5000/results/exams/fetch');
      setExams(response.data);
    } catch (err) {
      setError('Failed to fetch exams');
    }
  };

  useEffect(() => {
    if (userId) {
      fetchExams();  // Fetch exams on component mount
    }
  }, [userId]);

  const handleInputChange = (e) => {
    setNewResult(e.target.value);
  };

  const handleExamChange = async (e) => {
    const examId = e.target.value;
    setSelectedExam(examId);

    // Fetch associated test types for the selected exam
    try {
      const response = await axios.get(`http://localhost:5000/results/testtypes/${examId}`);
      setTestTypes(response.data);
    } catch (err) {
      setError('Failed to fetch test types for selected exam');
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setSuccessMessage(null);
    setError(null);

    try {
      await axios.post('http://localhost:5000/results/new', {
        user_id: userId,
        exam_id: selectedExam,
        result_data: newResult,
      });

      setSuccessMessage('Result added successfully!');
      setNewResult('');
    } catch (err) {
      setError('Failed to insert result');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <h2>Insert Test Results</h2>

      {/* Display success or error messages */}
      {successMessage && <div style={{ color: 'green' }}>{successMessage}</div>}
      {error && <div style={{ color: 'red' }}>{error}</div>}

      {/* Form to add new test result */}
      <form onSubmit={handleSubmit}>
        <div>
          <label>
            <strong>Select Exam:</strong>
            <select
              value={selectedExam}
              onChange={handleExamChange}
              required
            >
              <option value="">Select an exam</option>
              {exams.map((exam) => (
                <option key={exam.examid} value={exam.examid}>
                  {exam.examtype} - {exam.patient_name} ({exam.patient_email})
                </option>
              ))}
            </select>
          </label>
        </div>

        <div>
          <label>
            <strong>Test Result:</strong>
            <input
              type="number"
              value={newResult}
              onChange={handleInputChange}
              placeholder="Enter test result"
              required
            />
          </label>
        </div>

        <button type="submit" disabled={loading}>
          {loading ? 'Submitting...' : 'Add Result'}
        </button>
      </form>
    </div>
  );
};

export default InsertTestResults;

