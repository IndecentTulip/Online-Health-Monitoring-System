import React, { useState, useEffect } from 'react';
import axios from 'axios';

const Prediction = ({ userId }) => {
  const [reports, setReports] = useState([]);
  const [patients, setPatients] = useState([]);
  const [exams, setExams] = useState([]);
  const [newReport, setNewReport] = useState({
    workersid: '',
    healthid: '',
    pdate: '',
    examtype: ''  // Add exam type to the report data
  });
  const [error, setError] = useState('');

  // Fetch all prediction reports, patients, and exams on component mount
  useEffect(() => {
    const fetchData = async () => {
      try {
        // Fetch prediction reports
        const reportResponse = await axios.get('http://localhost:5000/predict/fetch');
        setReports(reportResponse.data);

        // Fetch patients assigned to the doctor
        const patientResponse = await axios.get('http://localhost:5000/predict/doc');
        setPatients(patientResponse.data);

        // Fetch exam types
        const examResponse = await axios.get('http://localhost:5000/predict/exam/fetch');
        setExams(examResponse.data);
      } catch (err) {
        setError('Failed to fetch data');
      }
    };

    fetchData();
  }, []);

  // Handle creating a new prediction report
  const handleCreateReport = async () => {
    try {
      // Send POST request to create a new report
      const response = await axios.post('http://localhost:5000/predict/new', newReport);

      if (response.status === 201) {
        setReports([...reports, response.data.report]);
        setNewReport({ workersid: '', healthid: '', pdate: '', examtype: '' });
      }
    } catch (err) {
      setError('Failed to create prediction report');
    }
  };

  return (
    <div>
      <h2>Prediction Reports</h2>
      {error && <p style={{ color: 'red' }}>{error}</p>}

      <h3>Prediction Reports</h3>
      <ul>
{/*
        {reports.length > 0 ? (
          reports.map((report) => (
            <li key={report.preportid}>
              <p>Report ID: {report.preportid}</p>
              <p>Doctor ID: {report.workersid}</p>
              <p>Patient ID: {report.healthid}</p>
              <p>Date: {report.pdate}</p>
              <p>Exam Type: {report.examtype}</p>
            </li>
          ))
        ) : (
          <p>No prediction reports available</p>
        )}
*/}
      </ul>

      <h3>Create New Prediction Report</h3>
      <div>
        <label>Doctor:</label>
        <select
          value={newReport.workersid}
          onChange={(e) => setNewReport({ ...newReport, workersid: e.target.value })}
        >
          <option value="">Select Doctor</option>
{/*          {patients.map((patient) => (
            <option key={patient.healthid} value={patient.workersid}>
              {patient.worker_name}
            </option>
          ))}
*/}
        </select>

        <label>Patient:</label>
        <select
          value={newReport.healthid}
          onChange={(e) => setNewReport({ ...newReport, healthid: e.target.value })}
        >
          <option value="">Select Patient</option>
{/*          {patients.map((patient) => (
            <option key={patient.healthid} value={patient.healthid}>
              {patient.patientname}
            </option>
          ))}
*/}
        </select>

        <label>Report Date:</label>
        <input
          type="date"
          value={newReport.pdate}
          onChange={(e) => setNewReport({ ...newReport, pdate: e.target.value })}
        />

        <label>Exam Type:</label>
        <select
          value={newReport.examtype}
          onChange={(e) => setNewReport({ ...newReport, examtype: e.target.value })}
        >
          <option value="">Select Exam Type</option>
{/*          {exams.map((exam) => (
            <option key={exam.examtype} value={exam.examtype}>
              {exam.examtype}
            </option>
          ))}
*/}
        </select>

        <button onClick={handleCreateReport}>Create Report</button>
      </div>
    </div>
  );
};

export default Prediction;

