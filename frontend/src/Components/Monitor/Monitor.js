import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './Monitor.css'

const Monitor = ({ userId }) => {
  const [monitors, setMonitors] = useState([]);  // List of monitors
  const [examItems, setExamItems] = useState([]);  // List of exam types for dropdown
  const [newExamType, setNewExamType] = useState('');  // New exam type for creating a monitor
  const [newSmartStatus, setNewSmartStatus] = useState('');  // New smart status for creating a monitor
  const [selectedMonitor, setSelectedMonitor] = useState({
    monitorid: 0,
    workersid: userId,
    testtype: 'fake',
    smartstatus: 'null',
    healthid: 66
    });  // Monitor to be updated
  const [patients, setPatients] = useState([]);  // List of patients for selecting healthid
  const [error, setError] = useState(null);  // Error handling
  const [successMessage, setSuccessMessage] = useState('');  // Success message

  // Fetch monitors
  const fetchMonitors = async () => {
    try {
      const response = await axios.get('http://localhost:5000/monitor/fetch', {
        params: {userId: userId}})
      setMonitors(response.data);  // Store the fetched monitors in state
    } catch (err) {
      setError('Failed to fetch monitors');
    }
  };

  // Fetch patients (assuming a 'GET /exam/doc' or similar endpoint)
  const fetchPatients = async () => {
    try {
      const response = await axios.get('http://localhost:5000/exam/doc', {
        params: { user_id: userId },
      });
      setPatients(response.data);  // Store the fetched patients for health ID
    } catch (err) {
      setError('Failed to fetch patients');
    }
  };

  // Fetch available exam items for the dropdown
  const fetchExamItems = async () => {
    try {
      const response = await axios.get('http://localhost:5000/exam/fetch_test_types');
      setExamItems(response.data);  // Store the fetched exam items in state
    } catch (err) {
      setError('Failed to load exam items');
    }
  };

  // Handle adding a new monitor
  const handleAddMonitor = async () => {

    try {
      const monitorData = {
        testtype: selectedMonitor.testtype,
        smartstatus: selectedMonitor.smartstatus,
        healthid: selectedMonitor.healthid,
        workersid: selectedMonitor.workersid  
      };
      await axios.post('http://localhost:5000/monitor/new', monitorData);
      setSuccessMessage('Monitor added successfully!');

      fetchMonitors();  // Refresh the monitor list
    } catch (err) {
      setError('Failed to add monitor');
    }
  };

  // Handle deleting a monitor
  const handleDeleteMonitor = async (monitorId) => {
    
      await axios.delete('http://localhost:5000/monitor/del', {
        data: { monitorId: monitorId},
      });
      setSuccessMessage('Monitor deleted successfully!');
      fetchMonitors();  // Refresh the monitor list
    
  };

  // Handle updating a monitor
  const handleUpdateMonitor = async () => {
   try{
      var monitorData = {
        testtype: selectedMonitor.testtype,
        smartstatus: selectedMonitor.smartstatus,
        healthid: selectedMonitor.healthid, 
        monitorid: selectedMonitor.monitorid
      }
    }
    catch {
      setSuccessMessage('error?')
    }
    try {
      await axios.patch('http://localhost:5000/monitor/update', monitorData);
      
      setSuccessMessage('Monitor updated successfully!');
      fetchMonitors();  // Refresh the monitor list
    }
     catch (err) {
      setError('Failed to update monitor');
    }
  }

  // Fetch monitors, patients, and exam items on component mount
  useEffect(() => {
    fetchMonitors();
    fetchPatients();  // Assuming the user has access to their patients
    fetchExamItems();  // Fetch available exam items for the dropdown
  }, []);

 return (
  <div className="monitor-page">
    <h2>Smart Monitors</h2>

    {/* Error and Success messages */}
    {error && <div className="error-message">{error}</div>}
    {successMessage && <div className="success-message">{successMessage}</div>}

    {/* Form to add or update monitor */}
    <div className="monitor-form">
      <p>{selectedMonitor.monitorid} {selectedMonitor.workersid} {selectedMonitor.testtype} {selectedMonitor.smartstatus} {selectedMonitor.healthid}</p>
      <div>
        <label>
          Test Type:
          <select
            onChange={(e) => setSelectedMonitor({ ...selectedMonitor, testtype: e.target.value })}
          >
            <option value="">Select Test Type</option>
            {examItems.map((item, index) => (
              <option key={index} value={item.testtype}>
                {item.testtype}
              </option>
            ))}
          </select>
        </label>
      </div>
      <div>
        <label>
          Patient:
          <select
            onChange={(e) => setSelectedMonitor({ ...selectedMonitor, healthid: e.target.value })}
            value={selectedMonitor ? selectedMonitor.healthid : ''}
            required
          >
            <option value="">Select Patient</option>
            {patients.map((patient) => (
              <option key={patient.id} value={patient.id}>
                {patient.name}
              </option>
            ))}
          </select>
        </label>
      </div>
      <div>
        <label>
          Smart Status:
          <select
            onChange={(e) => setSelectedMonitor({ ...selectedMonitor, smartstatus: e.target.value })}
            required
          >
            <option value="">Select Status</option>
            <option value="sent">Sent</option>
            <option value="not sent">Not Sent</option>
          </select>
        </label>
      </div>
      <div>
        <label>
          Monitor:
          <select
            onChange={(e) => setSelectedMonitor({ ...selectedMonitor, monitorid: e.target.value })}
            value={selectedMonitor ? selectedMonitor.monitorid : ''}
            required
          >
            <option value="">Select Monitor</option>
            {monitors.map((monitor) => (
              <option key={monitor.monitorid} value={monitor.monitorid}>
                {monitor.monitorid}
              </option>
            ))}
          </select>
        </label>
      </div>
      <button onClick={() => handleAddMonitor()}>
        Create Monitor
      </button>
      <button onClick={() => handleUpdateMonitor()}>
        Update Monitor
      </button>
    </div>

    {/* List of monitors */}
    <h3>Monitors List</h3>
    <ul className="monitors-list">
      {monitors.length === 0 ? (
        <p>No monitors available</p>
      ) : (
        monitors.map((monitor) => (
          <li key={monitor.monitorid}>
            <p><strong>Monitor ID:</strong> {monitor.monitorid}</p>
            <p><strong>Exam Type:</strong> {monitor.testtype}</p>
            <p><strong>Status:</strong> {monitor.smartstatus}</p>
            <p><strong>Patient ID:</strong> {monitor.healthid}</p>
            <button onClick={() => handleDeleteMonitor(monitor.monitorid)}>Delete</button>
          </li>
        ))
      )}
    </ul>
  </div>
);
};

export default Monitor;

