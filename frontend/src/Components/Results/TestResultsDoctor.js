import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './TestResultsDoctor.css';

const TestResultsDoctor = ({ userId }) => {
  const [results, setResults] = useState([]); // All fetched results
  const [filteredResults, setFilteredResults] = useState([]); // Filtered results to display
  const [examItems, setExamItems] = useState([]); // Holds the unique exam items for filtering
  const [filters, setFilters] = useState({
    patient_name: '',
    exam_date: '',
    exam_item: '',
    abnormal: false,
  });
  const [error, setError] = useState(null);

  // Fetch all results for the doctor from the backend
  const fetchResults = async () => {
    try {
      const response = await axios.get('http://localhost:5000/results/doctor/fetch', {
        params: { user_id: userId },
      });
      const fetchedResults = response.data;
      setResults(fetchedResults); // Store all results in state
      setFilteredResults(fetchedResults); // Set initial filtered results to all fetched results
    } catch (err) {
      setError('Failed to fetch results');
    }
  };

  // Fetch the exam items for the dropdown filter
  const fetchExamItems = async () => {
    try {
      const response = await axios.get('http://localhost:5000/exam/fetch');
      setExamItems(response.data); // Store the exam items for filtering
    } catch (err) {
      setError('Failed to load exam items');
    }
  };

  // Handle filter change
  const handleFilterChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFilters((prevFilters) => {
      const updatedFilters = {
        ...prevFilters,
        [name]: type === 'checkbox' ? checked : value,
      };
      filterResults(updatedFilters); // Re-filter the results when filters change
      return updatedFilters;
    });
  };

  // Filter results based on the current filter state
  const filterResults = (filters) => {
    const { patient_name, exam_date, exam_item, abnormal } = filters;

    // Only filter if 'results' is an array
    if (Array.isArray(results)) {
      const filtered = results.filter((result) => {
        const isPatientNameMatch = patient_name
          ? result.patient_name.toLowerCase().includes(patient_name.toLowerCase())
          : true;
        const isExamDateMatch = exam_date ? result.exam_date === exam_date : true;
        const isExamItemMatch = exam_item ? result.exam_item === exam_item : true;
        const isAbnormalMatch = abnormal ? result.abnormal === abnormal : true;

        return (
          isPatientNameMatch &&
          isExamDateMatch &&
          isExamItemMatch &&
          isAbnormalMatch
        );
      });

      setFilteredResults(filtered); // Update the filtered results
    }
  };

  // Fetch data on mount
  useEffect(() => {
    if (userId) {
      fetchResults(); // Fetch results once
      fetchExamItems(); // Fetch exam items for filtering
    }
  }, [userId]);

  return (
    <div className="form-container">
      <h2>Test Results for Doctor</h2>

      {/* Error display */}
      {error && <div style={{ color: 'red' }}>{error}</div>}

      {/* Filter Form */}
      <form>
      <div className="form">
           <label>
            Patient Name:
            <input
              type="text"
              name="patient_name"
              value={filters.patient_name}
              onChange={handleFilterChange}
            />
          </label>
        </div>

        <div className="form">
          <label>
            Exam Date:
            <input
              type="date"
              name="exam_date"
              value={filters.exam_date}
              onChange={handleFilterChange}
            />
          </label>
        </div>

        <div className="form">
          <label>
            Exam Item:
            <select
              name="exam_item"
              value={filters.exam_item}
              onChange={handleFilterChange}
            >
              <option value="">Select Exam Item</option>
              {examItems.map((item, index) => (
                <option key={index} value={item}>
                  {item}
                </option>
              ))}
            </select>
          </label>
        </div>
        <div className="form">
          <label>
            Show Only Abnormal Results:
            <input
              type="checkbox"
              name="abnormal"
              checked={filters.abnormal}
              onChange={handleFilterChange}
            />
          </label>
        </div>
      </form>

      {/* Display Results */}
      <h3>Test Results:</h3>
      {filteredResults.length === 0 ? (
        <p>No results found</p>
      ) : (
        <ul>
          {filteredResults.map((result, index) => (
            <li key={index}>
              <p><strong>Patient Name:</strong> {result.patient_name}</p>
              <p><strong>Exam Item:</strong> {result.exam_item}</p>
              <p><strong>Date:</strong> {result.exam_date}</p>
              <p><strong>Result:</strong> {result.result_value}</p>
              <p><strong>Abnormal:</strong> {result.abnormal ? 'Yes' : 'No'}</p>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default TestResultsDoctor;

