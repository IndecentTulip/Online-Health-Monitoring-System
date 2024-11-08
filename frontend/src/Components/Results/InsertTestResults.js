import React, { useEffect, useState } from 'react';
import axios from 'axios';

const InsertTestResults = ({ userId }) => {
  const [results, setResults] = useState([]);
  const [newResult, setNewResult] = useState('');
  const [error, setError] = useState(null);
  const [successMessage, setSuccessMessage] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleInputChange = (e) => {
    setNewResult(e.target.value);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setSuccessMessage(null);
    setError(null);

    try {
      await axios.post('http://localhost:5000/results/new', {
        user_id: userId,
        result_data: newResult,
      });
      setSuccessMessage('Result added successfully!');
      setNewResult(''); // Clear the input field after successful submission
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
            <strong>New Test Result:</strong>
            <input
              type="text"
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

