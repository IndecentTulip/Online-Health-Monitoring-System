import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './Prediction.css';

const Prediction = ({ userId }) => {
  const [reports, setreports] = useState([]);
  const [patient_list, setPList] = useState([]);
  const [patient, setPatient] = useState([]);
  const [currentReport, setCurrentReport] = useState({
  preportid: 1,
  workersid: 2,
  healthid: 3,
  pdate: "a day"
  });
  const [reportContent, setReportContent] = useState([{
    preportid:	5,
    testtype:	'fake test',
    concernvalue:	5
  }]);
  const [newReport, setNewReport] = useState({
    year: 0,
    patient: 'dummy'
  });
  const [error, setError] = useState('');

  // Function to fetch reports and patients data from the backend
  const fetchReports = async () => {
    
      const Response = await axios.get('http://localhost:5000/predict/fetch');
      setreports(Response.data);
      setError("SUCCESS!")
      try {
    } catch (err) {

      setError('Failed to fetch reports and patients');
    }
  };

  // Fetch data when the component mounts
  useEffect(() => {
    fetchReports();
  }, []);
  useEffect(() => {
    const fetchPatients = async () => {
      try {
        const response = await axios.get('http://localhost:5000/accounts/patient/every/fetch');
        setPList(response.data);
      } catch (err) {
        setError('Request of the patients failed.');
      }
    };

    fetchPatients();
  }, []);

  const handleViewReport = async (input) => {
    setCurrentReport(input)
    fetchReportContent(input.preportid)
    setError('working')
  }

  const handleCreateReport = async (M) => {
      const newData = {
        userID: newReport.patient,
        year: newReport.year,
        AdminID: userId
      };

      const Response = await axios.post('http://localhost:5000/predict/new', newData)
     
      fetchReports()

  }
  const fetchReportContent = async (input) => {
    try{
      const Response = await axios.get('http://localhost:5000/predict/fetchcontent', {
        params: {ReportID: input}
      });
      
      setReportContent(Response.data)

      
    } catch (err) {
      setError('oops')
    }
  }
  const handleDeleteReport = async (ReportId) => {
    try {
      const response = await axios.delete('http://localhost:5000/predict/delete', {
        data: { ReportId: ReportId},
      });

      if (response.status === 200) {
        fetchReports(); // Refetch workers after deletion
        setError('Hmmmm')
      }
    } catch (err) {
      setError('Failed to delete Report');
    }
  };



  return (
    <div className="prediction">
      <h2>Manage Prediction Reports</h2>
      {error && <p style={{ color: 'red' }}>{error}</p>} {/* Display error if it exists */}
      <h3>Add new Report</h3>
      <p>Normally you cannot select year, and it must be december to generate reports.</p>
      <p> For demonstration purposes, these restrictions are not present.</p>
        
          <input
            type="number"
            value={newReport.year}
            onChange={(e) => setNewReport({ ...newReport, year: e.target.value })}
            placeholder="year"
            required
          />

<select onChange={(e) => setNewReport({ ...newReport, patient: e.target.value })}>
        <option value="">Select a Patient</option>
        
        {Array.isArray(patient_list) && patient_list.map((patient, index) => (
          <option key={index} value={patient.healthid}>{patient.patient_name}</option>
          
        ))}
      </select>
          <button onClick={() => handleCreateReport()}>
            Generate Report
          </button>
          <p>{newReport.patient}, {newReport.year}</p>
        
      <p> Report ID: {currentReport.preportid} &nbsp;&nbsp;Prepared By: {currentReport.workersid}&nbsp;&nbsp; Date Generated: {currentReport.pdate}&nbsp;&nbsp; Patient: {currentReport.healthid}</p>
      <p>Concern Value represents likelihood of continued problems; lower is better.</p>
      {reportContent.length > 0 ? (
            reportContent.map((Entry)  => (
              <li key={Entry.healthid}>
                <p>Test Type: {Entry.testtype} &nbsp;&nbsp;&nbsp;Concern Value: {Entry.concernvalue}</p>


              </li>
            ))
          ) : (
            <p>No entries available</p>
          )}
      <div>
        <h3>Existing reports</h3>
        <ul>
          {reports.length > 0 ? (
            reports.map((Report) => (
              <li key={Report.preportid}>
                <p>{Report.preportid} {Report.healthid} {Report.pdate} </p>

                <button onClick={() => handleDeleteReport(Report.preportid)}>Delete Report</button>
                <button onClick={() => handleViewReport(Report)}>View Report</button>
              </li>
            ))
          ) : (
            <p>No reports available</p>
          )}
        </ul>

        
      </div>


    </div>
  );
};

export default Prediction;

