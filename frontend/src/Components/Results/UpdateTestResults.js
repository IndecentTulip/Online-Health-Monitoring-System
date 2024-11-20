import React, { useEffect, useState } from 'react';
import axios from 'axios';
import './InsertTestResults.css';

const UpdateTestResults = ({ userId }) => {
  const [exams, setExams] = useState([]);
  const [selectedExam, setSelectedExam] = useState('');
  const [testTypes, setTestTypes] = useState([]);
  const [results, setResults] = useState({});
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

  const handleExamChange = async (e) => {
    const examId = e.target.value;
    setSelectedExam(examId);

    // Fetch associated test types for the selected exam
    try {
      const response = await axios.get(`http://localhost:5000/results/existtesttypes/${examId}`);
      setTestTypes(response.data);
      setResults({}); // Reset the results when a new exam is selected
    } catch (err) {
      setError('Failed to fetch test types for selected exam');
    }
  };
  const refreshExam = async () => {

    // Fetch associated test types for the selected exam
    try {
      const response = await axios.get(`http://localhost:5000/results/existtesttypes/${selectedExam}`);
      setTestTypes(response.data);
      setResults({}); // Reset the results when a new exam is selected
    } catch (err) {
      setError('Failed to fetch test types for selected exam');
    }
  };
  const handleResultChange = (testType, e) => {
    setResults({
      ...results,
      [testType]: e.target.value,
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setSuccessMessage(null);
    setError(null);

    // Ensure all results are entered
    if (Object.keys(results).length !== testTypes.length) {
      setError('Please provide results for all test types.');
      setLoading(false);
      return;
    }

    try {
      await axios.patch('http://localhost:5000/results/update', {
        user_id: userId,
        exam_id: selectedExam,
        result_data: results,
      });
      
      setSuccessMessage('Results added successfully!');
      refreshExam();

      //setResults({}); // Clear the results after successful submission
    } catch (err) {
      setError('Failed to insert results');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container">
      <h2>Update Test Results</h2>

      {/* Display success or error messages */}
      {successMessage && <div style={{ color: 'green' }}>{successMessage}</div>}
      {error && <div style={{ color: 'red' }}>{error}</div>}

      {/* Form to add new test results */}
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

        {/* Input for each test type */}
        {testTypes.length > 0 && (
          <>
            <h3>Test Results</h3>
            {testTypes.map((testType) => (
              <div key={testType}>
                <label>
                  <strong>{testType} Result:</strong>
                  <input
                    type="number"
                    value={results[testType] || ''}
                    onChange={(e) => handleResultChange(testType, e)}
                    placeholder={`Enter result for ${testType}`}
                    required
                  />
                </label>
              </div>
            ))}
          </>
        )}

        <button type="submit" disabled={loading}>
          {loading ? 'Submitting...' : 'Add Results'}
        </button>
      </form>
    </div>
  );
};

export default UpdateTestResults;

