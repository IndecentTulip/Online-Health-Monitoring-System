import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './TestResultsDoctor.css';

const TestResultsDoctor = ({ userId }) => {
  const [results, setResults] = useState([]);
  const [examItems, setExamItems] = useState([]);
  const [patientList, setPatientList] = useState([]);  // New state to store patients list
  const [newSearch, setNewSearch] = useState({
    date: "",
    test_type: "test",
    pat_name: "name",
    patient_ID: 0,
    search_type: 0,
  });
  const [error, setError] = useState('');

  const fetchPatients = async () => {
    try {
      const response = await axios.get('http://localhost:5000/accounts/patient/every/fetch');
      setPatientList(response.data);  // Store the patient data
    } catch (err) {
      setError('Failed to load patients');
    }
  };

  const fetchExamItems = async () => {
    try {
      const response = await axios.get('http://localhost:5000/exam/fetch_test_types');
      setExamItems(response.data);  // Store the fetched exam items in state
    } catch (err) {
      setError('Failed to load exam items');
    }
  };

  const handleSearchResults = async (input) => {
    setNewSearch({...newSearch, search_type: input});
    console.log(newSearch.pat_name)
    const response = await axios.get('http://localhost:5000/results/search', {
      params: {
        test_type: newSearch.test_type,
        pat_name: newSearch.pat_name,
        patient_ID: newSearch.patient_ID,
        search_type: input,
        date: newSearch.date
      }
    });
    setResults(response.data);
  };

  useEffect(() => {
    fetchExamItems();
    fetchPatients(); // Fetch the list of patients on component mount
  }, []);

  return (
    <div>
      <h3>Manage Summary Results</h3>
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
        Patient:
        <select onChange={(e) => setNewSearch({ ...newSearch, pat_name: e.target.value })}>
          <option value="">Select Patient</option>
          {Array.isArray(patientList) && patientList.map((patient, index) => (
            <option key={index} value={patient.patient_name}>
              {patient.patient_name}
            </option>
          ))}
        </select>
      </label>

      <label>
        Test Type:
        <select onChange={(e) => setNewSearch({ ...newSearch, test_type: e.target.value })}>
          <option value="">Select Test Type</option>
          {examItems.map((item, index) => (
            <option key={index} value={item.testtype}>
              {item.testtype}
            </option>
          ))}
        </select>
      </label>

      <div className="button-group">
        <button onClick={() => handleSearchResults(3)}>Search By Name</button>
        <button onClick={() => handleSearchResults(4)}>Search By Name and Date</button>
        <button onClick={() => handleSearchResults(5)}>Search By Name and Exam Item</button>
        <button onClick={() => handleSearchResults(6)}>Search By Abnormal Results</button>
      </div>

      <div className="box-container">
        <h3>Current Values</h3>
        <p>{newSearch.date} {newSearch.pat_name} {newSearch.patient_ID} {newSearch.test_type} Search Type:{newSearch.search_type}</p>
        <ul>
          {results.length > 0 ? (
            results.map((result) => (
              <li key={result.result_id}>
                <p>Result ID: {result.result_id} Test Type: {result.test_name} Result: {result.results} Exam ID: {result.exam_id}</p>
              </li>
            ))
          ) : (
            <p>No results available</p>
          )}
        </ul>
      </div>
    </div>
  );
};

export default TestResultsDoctor;

