import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './ManageAcc.css';

const ManageAcc = ({ userId }) => {
  const [workers, setWorkers] = useState([]);
  const [patients, setPatients] = useState([]);
  const [newWorker, setNewWorker] = useState({
    worker_name: '',
    worker_email: '',
    worker_role: 'Staff',
    worker_phone: '',
    worker_password: '',
  });
  const [error, setError] = useState('');

  // Fetch workers and patients data
  const fetchWorkersAndPatients = async () => {
    try {
      const workerResponse = await axios.get('http://localhost:5000/accounts/workers/every/fetch');
      setWorkers(workerResponse.data);

      const patientResponse = await axios.get('http://localhost:5000/accounts/patient/every/fetch');
      setPatients(patientResponse.data);
    } catch (err) {
      setError('Failed to fetch workers and patients');
    }
  };

  useEffect(() => {
    fetchWorkersAndPatients();
  }, []);

  const handleAddWorker = async (e) => {
    e.preventDefault();

    if (newWorker.worker_phone.length !== 10) {
      setError('Phone number must be exactly 10 digits long.');
      return;
    }
    if (newWorker.worker_password.length < 6) {
      setError('Password must be at least 6 characters long.');
      return;
    }

    try {
      const response = await axios.post('http://localhost:5000/accounts/workers/add', newWorker);

      if (response.status === 201) {
        fetchWorkersAndPatients();
        setNewWorker({
          worker_name: '',
          worker_email: '',
          worker_role: 'Staff',
          worker_phone: '',
          worker_password: '',
        });
        setError(''); // Clear errors
      }
    } catch (err) {
      setError('Failed to add worker: ' + (err.response?.data?.error || 'Unknown error'));
    }
  };

  const handleDeleteWorker = async (workerId) => {
    try {
      const response = await axios.delete('http://localhost:5000/accounts/workers/del', {
        data: { worker_id: workerId },
      });

      if (response.status === 200) {
        fetchWorkersAndPatients();
      }
    } catch (err) {
      setError('Failed to delete worker');
    }
  };

  const handleDeletePatient = async (patientId) => {
    try {
      const response = await axios.delete('http://localhost:5000/accounts/patient/del', {
        data: { patient_id: patientId },
      });

      if (response.status === 200) {
        fetchWorkersAndPatients();
      }
    } catch (err) {
      setError('Failed to delete patient');
    }
  };

  return (
    <div className="manage-accounts-container">
      <h2>Manage Accounts</h2>
      {error && <p className="manage-accounts-error">{error}</p>}

      <div className="add-worker-form">
        <h3>Add Worker</h3>
        <form onSubmit={handleAddWorker}>
          <input
            type="text"
            value={newWorker.worker_name}
            onChange={(e) => setNewWorker({ ...newWorker, worker_name: e.target.value })}
            placeholder="Worker Name"
            required
          />
          <input
            type="email"
            value={newWorker.worker_email}
            onChange={(e) => setNewWorker({ ...newWorker, worker_email: e.target.value })}
            placeholder="Worker Email"
            required
          />
          <input
            type="tel"
            value={newWorker.worker_phone}
            onChange={(e) => setNewWorker({ ...newWorker, worker_phone: e.target.value })}
            placeholder="Phone Number"
            required
          />
          <select
            value={newWorker.worker_role}
            onChange={(e) => setNewWorker({ ...newWorker, worker_role: e.target.value })}
            required
          >
            <option value="Staff">Staff</option>
            <option value="Doctor">Doctor</option>
          </select>
          <input
            type="password"
            value={newWorker.worker_password}
            onChange={(e) => setNewWorker({ ...newWorker, worker_password: e.target.value })}
            placeholder="Password"
            required
          />
          <button type="submit">Add Worker?</button>
        </form>
      </div>

      <div className="delete-workers-section box">
        <h3>Delete Workers</h3>
        <div className="delete-workers-container">
          {workers.length > 0 ? (
            workers.map((worker) => (
              <div key={worker.workerid} className="delete-item">
                <p><strong>Name:</strong> {worker.worker_name}</p>
                <p><strong>Email:</strong> {worker.worker_email}</p>
                <p><strong>Role:</strong> {worker.worker_role}</p>
                <button onClick={() => handleDeleteWorker(worker.workerid)}>Delete Worker?</button>
              </div>
            ))
          ) : (
            <p>No workers available</p>
          )}
        </div>
      </div>

      <div className="delete-patients-section box">
        <h3>Delete Patients</h3>
        <div className="delete-patients-container">
          {patients.length > 0 ? (
            patients.map((patient) => (
              <div key={patient.healthid} className="delete-item">
                <p><strong>Name:</strong> {patient.patient_name}</p>
                <p><strong>Email:</strong> {patient.patient_email}</p>
                <button onClick={() => handleDeletePatient(patient.healthid)}>Delete Patient?</button>
              </div>
            ))
          ) : (
            <p>No patients available</p>
          )}
        </div>
      </div>
    </div>
  );
};

export default ManageAcc;
