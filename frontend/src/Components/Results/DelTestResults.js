import React, { useState, useEffect } from 'react';
import axios from 'axios';

const DelTestResults = () => {
  const [testResults, setTestResults] = useState([]);  // List of all test results
  const [error, setError] = useState(null);  // Error handling
  const [successMessage, setSuccessMessage] = useState('');  // Success message

  // Fetch test results
  const fetchTestResults = async () => {
    try {
      const response = await axios.get('http://localhost:5000/results/fetch');
      console.log(response.data)
      if (response.data && response.data.length > 0) {
        setTestResults(response.data);  // Store the fetched test results
      } else{
        setTestResults([])
      }
    } catch (err) {
      setError('Failed to fetch test results');
      setTestResults([])
    }
  };

  // Handle deleting a test result
  const handleDeleteTestResult = async (resultId) => {
    try {
      await axios.delete('http://localhost:5000/results/del', {
        data: { result_id: resultId },
      });
      setSuccessMessage('Test result deleted successfully!');
      fetchTestResults();  // Refresh the test results list
    } catch (err) {
      setError('Failed to delete test result');
    }
  };

  // Fetch test results on component mount
  useEffect(() => {
    fetchTestResults();
  }, []);

  return (
    <div>
      <h2>Delete Test Results</h2>

      {/* Error and Success messages */}
      {error && <div style={{ color: 'red' }}>{error}</div>}
      {successMessage && <div style={{ color: 'green' }}>{successMessage}</div>}

      {/* List of Test Results */}
      {testResults.length === 0 ? (
        <p>No test results available.</p>
      ) : (
        <ul>
          {testResults.map((result) => (
            <li key={result.result_id}>
              <p><strong>Test Name:</strong> {result.test_name}</p>
              <p><strong>Test Date:</strong> {new Date(result.test_date).toLocaleDateString()}</p>
              <p><strong>Result ID:</strong> {result.result_id}</p>
              <p><strong>Result:</strong> {result.results}</p>
              <button onClick={() => handleDeleteTestResult(result.result_id)}>
                Delete Test Result
              </button>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default DelTestResults;

