import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './Monitor.css'

const Monitor = ({ userId }) => {
  const [monitors, setMonitors] = useState([]);  // List of monitors
  const [examItems, setExamItems] = useState([]);  // List of exam types for dropdown
  const [newExamType, setNewExamType] = useState('');  // New exam type for creating a monitor
  const [newSmartStatus, setNewSmartStatus] = useState('');  // New smart status for creating a monitor
  const [selectedMonitor, setSelectedMonitor] = useState(null);  // Monitor to be updated
  const [patients, setPatients] = useState([]);  // List of patients for selecting healthid
  const [error, setError] = useState(null);  // Error handling
  const [successMessage, setSuccessMessage] = useState('');  // Success message

  // Fetch monitors
  const fetchMonitors = async () => {
    try {
      const response = await axios.get('http://localhost:5000/monitor/fetch');
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
      const response = await axios.get('http://localhost:5000/exam/fetch');
      setExamItems(response.data);  // Store the fetched exam items in state
    } catch (err) {
      setError('Failed to load exam items');
    }
  };

  // Handle adding a new monitor
  const handleAddMonitor = async (e) => {
    e.preventDefault();
    try {
      const monitorData = {
        examtype: newExamType,
        smartstatus: newSmartStatus,
        healthid: selectedMonitor ? selectedMonitor.healthid : null,  // Assuming we select patient from dropdown
      };
      await axios.post('http://localhost:5000/monitor/new', monitorData);
      setSuccessMessage('Monitor added successfully!');
      setNewExamType('');
      setNewSmartStatus('');
      setSelectedMonitor(null);
      fetchMonitors();  // Refresh the monitor list
    } catch (err) {
      setError('Failed to add monitor');
    }
  };

  // Handle deleting a monitor
  const handleDeleteMonitor = async (monitorId) => {
    try {
      await axios.delete('http://localhost:5000/monitor/del', {
        data: { monitor_id: monitorId },
      });
      setSuccessMessage('Monitor deleted successfully!');
      fetchMonitors();  // Refresh the monitor list
    } catch (err) {
      setError('Failed to delete monitor');
    }
  };

  // Handle updating a monitor
  const handleUpdateMonitor = async (e) => {
    e.preventDefault();
    try {
      await axios.patch('http://localhost:5000/monitor/update', {
        monitorid: selectedMonitor.monitorid,
        examtype: newExamType,
        smartstatus: newSmartStatus,
        healthid: selectedMonitor.healthid,
      });
      setSuccessMessage('Monitor updated successfully!');
      setNewExamType('');
      setNewSmartStatus('');
      setSelectedMonitor(null);
      fetchMonitors();  // Refresh the monitor list
    } catch (err) {
      setError('Failed to update monitor');
    }
  };

  // Fetch monitors, patients, and exam items on component mount
  useEffect(() => {
    fetchMonitors();
    fetchPatients();  // Assuming the user has access to their patients
    fetchExamItems();  // Fetch available exam items for the dropdown
  }, []);

  return (
    <div>
      <h2>Smart Monitors</h2>

      {/* Error and Success messages */}
      {error && <div style={{ color: 'red' }}>{error}</div>}
      {successMessage && <div style={{ color: 'green' }}>{successMessage}</div>}

      {/* Form to add or update monitor */}
      <form onSubmit={selectedMonitor ? handleUpdateMonitor : handleAddMonitor}>
        <div>
          <label>
            Exam Type:
            <select
              value={newExamType}
              onChange={(e) => setNewExamType(e.target.value)}
              required
            >
              <option value="">Select Exam Type</option>
              {examItems.map((item, index) => (
                <option key={index} value={item.examtype}>
                  {item.examtype}
                </option>
              ))}
            </select>
          </label>
        </div>
        <div>
          <label>
            Smart Status:
            <select
              value={newSmartStatus}
              onChange={(e) => setNewSmartStatus(e.target.value)}
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
            Patient:
            <select
              onChange={(e) => setSelectedMonitor({ ...selectedMonitor, healthid: e.target.value })}
              value={selectedMonitor ? selectedMonitor.healthid : ''}
              required
            >
              <option value="">Select Patient</option>
              {patients.map((patient) => (
                <option key={patient.healthid} value={patient.healthid}>
                  {patient.name} (ID: {patient.healthid})
                </option>
              ))}
            </select>
          </label>
        </div>
        <button type="submit">{selectedMonitor ? 'Update Monitor' : 'Add Monitor'}</button>
      </form>

      {/* List of monitors */}
      <h3>Monitors List</h3>
      {monitors.length === 0 ? (
        <p>No monitors available</p>
      ) : (
        <ul>
          {monitors.map((monitor) => (
            <li key={monitor.monitorid}>
              <p><strong>Monitor ID:</strong> {monitor.monitorid}</p>
              <p><strong>Exam Type:</strong> {monitor.examtype}</p>
              <p><strong>Status:</strong> {monitor.smartstatus}</p>
              <p><strong>Patient ID:</strong> {monitor.healthid}</p>
              <button onClick={() => setSelectedMonitor(monitor)}>Update</button>
              <button onClick={() => handleDeleteMonitor(monitor.monitorid)}>Delete</button>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default Monitor;

