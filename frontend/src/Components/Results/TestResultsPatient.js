import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './TestResultsPatient.css';

const TestResultsPatient = ({ userId }) => {
  const [results, setResults] = useState([]);
  const [examItems, setExamItems] = useState([]);
  const [newSearch, setNewSearch] = useState({
    date: "1111-11-11",
    test_type: "test",
    pat_name: "name",
    patient_ID: userId,
    search_type: 0,
  });
  const [error, setError] = useState('');
 const handleSearchResults = async (input) => {

  setNewSearch({...newSearch, search_type: input})
  const response = await axios.get('http://localhost:5000/results/search', {
    params: {test_type: newSearch.test_type,
      pat_name: newSearch.pat_name,
      patient_ID: newSearch.patient_ID,
      search_type: input,
      date: newSearch.date
    }
  })
  setResults(response.data)
 }
  const fetchExamItems = async () => {
    try {
      const response = await axios.get('http://localhost:5000/exam/fetch_test_types');
      setExamItems(response.data);  // Store the fetched exam items in state
    } catch (err) {
      setError('Failed to load exam items');
    }
  };
  // Function to fetch results and patients data from the backend


  // Fetch data when the component mounts
  useEffect(() => {
    fetchExamItems(); 
  }, []);



  return (
    
    <div classname ="container">

      <h2>Manage Summary results</h2>
      {error && <p style={{ color: 'red' }}>{error}</p>} {/* Display error if it exists */}
      
      <h3>Search Test Results</h3>
        

<label>
            Exam Date:
            <input
              type="date"
              name="exam_date"
              value={newSearch.date}
              onChange={(e) => setNewSearch({ ...newSearch, date: e.target.value })}
            />
          </label>
            <label>
          Test Type:
          <select
            onChange={(e) => setNewSearch({...newSearch, test_type: e.target.value})}
          >
            <option value="">Select Test Type</option>
            {examItems.map((item, index) => (
              <option key={index} value={item.testtype}>
                {item.testtype}
              </option>
            ))}
          </select>
        </label>
        <button onClick={() =>  handleSearchResults(0)}>Seach By Exam Date</button>
        <button onClick={() =>  handleSearchResults(1)}>Seach By Exam Item</button>
        <button onClick={() => handleSearchResults(2)}>Seach By Abnormal Results</button>
      <h3>Current Values</h3>
      <p>{newSearch.date} {newSearch.pat_name} {newSearch.patient_ID} {newSearch.test_type} Search Type:{newSearch.search_type}</p>
      <ul>
          {results.length > 0 ? (
            results.map((result) => (
              <li key={result.result_id}>
                <p>result ID: {result.result_id} Test Type:{result.test_name} Result: {result.results} ExamID: {result.exam_id}</p>

              </li>
            ))
          ) : (
            <p>No results available</p>
          )}
        </ul>


</div>

  );
};

export default TestResultsPatient;

