import React, { useState, useEffect } from 'react';
import axios from 'axios';

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
    year: '',
    month: '',

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
    setError('work dammit')
  }

  const handleCreateReport = async () => {

      const Response = await axios.post('http://localhost:5000/yearreports/new')
    

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
    <div>
      <h2>Manage Summary Reports</h2>
      {error && <p style={{ color: 'red' }}>{error}</p>} {/* Display error if it exists */}
      <h3>Add Report</h3>
        <form onSubmit={handleCreateReport()}>
          <input
            type="number"
            value={newReport.year}
            onChange={(e) => setNewReport({ ...newReport, year: e.target.value })}
            placeholder="year"
            required
          />

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
          <button type="submit">Generate Report</button>
        </form>
      <p>{currentReport.monthoryear}, {currentReport.sreportid}, {currentReport.summarydate}, {currentReport.timeperiod}</p>
      {reportContent.length > 0 ? (
            reportContent.map((Entry) => (
              <li key={Entry.healthid}>
                <p>{Entry.healthid}, {Entry.noofexams}, {Entry.abnormalexams}</p>


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
              <li key={Report.sreportid}>
                <p>{Report.sreportid}, {Report.monthoryear}, </p>

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
  );
};

export default SumReport;

