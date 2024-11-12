import React, { useState, useEffect } from 'react';
import axios from 'axios';

const YearNMonth = ({ userId }) => {
  const [reports, setReports] = useState([]);
  const [patients, setPatients] = useState([]);
  const [newReport, setNewReport] = useState({
    workersid: '',
    monthoryear: 'month', // default to 'month'
    summarydate: '',
    timeperiod: '',
  });
  const [error, setError] = useState('');

  // Fetch year/month reports and patients assigned to the doctor
  useEffect(() => {
    const fetchData = async () => {
      try {
        // Fetch year/month reports
        const reportResponse = await axios.get('http://localhost:5000/yearreports/fetch');
        setReports(reportResponse.data);

      } catch (err) {
        setError('Failed to fetch data');
      }
    };

    fetchData();
  }, []);

  // Handle creating a new year/month report
  const handleCreateReport = async () => {
    try {
      const response = await axios.post('http://localhost:5000/yearreports/new', newReport);
      if (response.status === 201) {
        setReports([...reports, response.data.report]);
        setNewReport({ workersid: '', monthoryear: 'month', summarydate: '', timeperiod: '' });
      }
    } catch (err) {
      setError('Failed to create year/month report');
    }
  };

  return (
    <div>
      <h2>Year and Month Reports</h2>
      {error && <p style={{ color: 'red' }}>{error}</p>}

      <h3>Year/Month Reports</h3>
      <ul>
{/*
        {reports.length > 0 ? (
          reports.map((report) => (
            <li key={report.sreportid}>
              <p>Report ID: {report.sreportid}</p>
              <p>Doctor ID: {report.workersid}</p>
              <p>Month/Year: {report.monthoryear}</p>
              <p>Summary Date: {report.summarydate}</p>
              <p>Time Period: {report.timeperiod}</p>
            </li>
          ))
        ) : (
          <p>No year/month reports available</p>
        )}
*/}
      </ul>

      <h3>Create New Year/Month Report</h3>
      <div>
        <label>Doctor:</label>
        <select
          value={newReport.workersid}
          onChange={(e) => setNewReport({ ...newReport, workersid: e.target.value })}
        >
          <option value="">Select Doctor</option>
{/*
          {patients.map((patient) => (
            <option key={patient.healthid} value={patient.workersid}>
              {patient.worker_name}
            </option>
          ))}
*/}
        </select>

        <label>Month or Year:</label>
        <select
          value={newReport.monthoryear}
          onChange={(e) => setNewReport({ ...newReport, monthoryear: e.target.value })}
        >
          <option value="month">Month</option>
          <option value="year">Year</option>
        </select>

        <label>Summary Date:</label>
        <input
          type="date"
          value={newReport.summarydate}
          onChange={(e) => setNewReport({ ...newReport, summarydate: e.target.value })}
        />

        <label>Time Period:</label>
        <input
          type="text"
          value={newReport.timeperiod}
          onChange={(e) => setNewReport({ ...newReport, timeperiod: e.target.value })}
        />

        <button onClick={handleCreateReport}>Create Report</button>
      </div>
    </div>
  );
};

export default YearNMonth;

