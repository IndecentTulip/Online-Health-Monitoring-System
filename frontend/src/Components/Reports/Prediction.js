import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './Prediction.css';

const Prediction = ({ userId }) => {
  const [reports, setreports] = useState([]);
  const [patient_list, setPList] = useState([]);
  const [patient, setPatient] = useState([]);
  const [currentReport, setCurrentReport] = useState({
  });
  const [reportContent, setReportContent] = useState([{
    testtype:	'fake test',
  }]);
  const [newReport, setNewReport] = useState({
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
        pdate: newReport.pdate,
        AdminID: userId
      };
      console.log(newReport.pdate)
      try {
      const Response = await axios.post('http://localhost:5000/predict/new', newData)
     
      fetchReports()}
      catch (err) {
        setError("Couldn't create report")
      }

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
    <div className='predictioninner'>
      <h2>Manage Prediction Reports</h2>
      {error && <p style={{ color: 'red' }}></p>} {/* Display error if it exists */}
      <h3>Add new Report</h3>
      <p>Normally you cannot select prediction date, and it must be december to generate reports.</p>
      <p> For demonstration purposes, these restrictions are not present.</p>
        
          <input
            type="date"
            value={newReport.pdate}
            onChange={(e) => setNewReport({ ...newReport, pdate: e.target.value })}
            placeholder=""
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
                <p>Report ID:{Report.preportid} &nbsp;&nbsp;&nbsp; Patient Health ID: {Report.healthid} &nbsp;&nbsp;&nbsp; Date Report Generated:{Report.pdate} </p>

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
    </div>
  );
};

export default Prediction;

