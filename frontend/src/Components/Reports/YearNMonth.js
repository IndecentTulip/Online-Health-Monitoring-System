import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './YearNMonth.css';

const SumReport = ({ userId }) => {
  const [reports, setreports] = useState([]);
  const [currentReport, setCurrentReport] = useState({
  monthoryear: 'test',
  sreportid: 1,
  summarydate:'hello',
  timeperiod:'today',
  workersid:'99',  
  });
  const [reportContent, setReportContent] = useState([{
    abnormalexams:	5,
    healthid:	10031,
    noofexams:	5
  }]);
  const [newReport, setNewReport] = useState({
    year: 0,
    month: 0
  });
  const [error, setError] = useState('');

  // Function to fetch reports and patients data from the backend
  const fetchReports = async () => {
    try {
      const Response = await axios.get('http://localhost:5000//yearreports/fetch');
      setreports(Response.data);
      setError("SUCCESS!")

    } catch (err) {

      setError('Failed to fetch reports and patients');
    }
  };

  // Fetch data when the component mounts
  useEffect(() => {
    fetchReports();
  }, []);

  const handleViewReport = async (input) => {
    setCurrentReport(input)
    fetchReportContent(input.sreportid)
    setError('working')
  }

  const handleCreateReport = async () => {
      const newData = {
        month: newReport.month,
        year: newReport.year,
        userID: userId
      };

      const Response = await axios.post('http://localhost:5000/yearreports/new', newData)
     
      fetchReports()

  }
  const fetchReportContent = async (input) => {
    try{
      const Response = await axios.get('http://localhost:5000/yearreports/fetchcontent', {
        params: {ReportID: input}
      });
      
      setReportContent(Response.data)

      
    } catch (err) {
      setError('oops')
    }
  }
  const handleDeleteReport = async (ReportId) => {
    try {
      const response = await axios.delete('http://localhost:5000/yearreports/delete', {
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
    
    <div className="sumreport-container">
      <h2>Manage Summary Reports</h2>
      {error && <p style={{ color: 'red' }}>{error}</p>} {/* Display error if it exists */}
     
      <div className="report-sections-container"></div>
      <div className="report-box add-report-section">
      <h3>Add Report</h3>
      <div className="form-group">
          <input
            type="number"
            value={newReport.year}
            onChange={(e) => setNewReport({ ...newReport, year: e.target.value })}
            placeholder="year"
            required
          />
      </div>

      <div className="form-group">
          <select
            value={newReport.month}
            onChange={(e) => setNewReport({ ...newReport, month: e.target.value })}
            required
          >
            <option value ="0">Whole Year</option>
            <option value="1">January</option>
            <option value="2">February</option>
            <option value="3">March</option>
            <option value="4">April</option>
            <option value="5">May</option>
            <option value="6">June</option>
            <option value="7">July</option>
            <option value="8">August</option>
            <option value="9">September</option>
            <option value="10">October</option>
            <option value="11">November</option>
            <option value="12">December</option>
            </select>
            </div>
          <button onClick={() => handleCreateReport()}>
            Generate Report
          </button>
          <p>{newReport.month}, {newReport.year}</p>


        <div className="report-box current-report-section">
      <h3>Current Report</h3>
      <p> Report ID: {currentReport.sreportid} 
        Report Type: {currentReport.monthoryear} 
        Date Generated: {currentReport.summarydate} 
        Time Period: {currentReport.timeperiod}</p>
   

      {reportContent.length > 0 ? (
            reportContent.map((Entry)  => (
              <li key={Entry.healthid}>
                <p>Patient ID: {Entry.healthid} 
                  No. of Tests: {Entry.noofexams} 
                  No of Abnormal Tests: {Entry.abnormalexams}  
                  {(Entry.abnormalexams/(Entry.noofexams  + 0.0000000001) * 100).toFixed(1)}% Abnormal</p>
                

              </li>
            ))
      
          ) : (
          
            <p>No entries available</p>
          )}
          </div>

          <div className="existing-reports-section">
        <h3>Existing reports</h3>
        <ul>
          {reports.length > 0 ? (
            reports.map((Report) => (
              <li key={Report.sreportid}>
                <p>Report ID: {Report.sreportid} 
                  Type: {Report.monthoryear} </p>

                <button onClick={() => handleDeleteReport(Report.sreportid)}>Delete Report</button>
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

export default SumReport;

