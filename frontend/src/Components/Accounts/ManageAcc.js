import React, { useState, useEffect } from 'react';
import axios from 'axios';

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

  // Function to fetch workers and patients data from the backend
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

  // Fetch data when the component mounts
  useEffect(() => {
    fetchWorkersAndPatients();
  }, []);

  const handleAddWorker = async (e) => {
    e.preventDefault();

    // Validate the phone number
    if (newWorker.worker_phone.length !== 10) {
      setError('Phone number must be exactly 10 digits long.');
      return;
    }

    // Validate password length
    if (newWorker.worker_password.length < 6) {
      setError('Password must be at least 6 characters long.');
      return;
    }

    try {
      const workerData = {
        worker_name: newWorker.worker_name,
        worker_email: newWorker.worker_email,
        worker_role: newWorker.worker_role,
        worker_phone: newWorker.worker_phone,
        worker_password: newWorker.worker_password, // Send plain password here
      };

      // Send the POST request to add the worker
      const response = await axios.post('http://localhost:5000/accounts/workers/add', workerData);

      if (response.status === 201) {
        fetchWorkersAndPatients(); // Refetch workers after successful addition
        setNewWorker({
          worker_name: '',
          worker_email: '',
          worker_role: 'Staff',
          worker_phone: '',
          worker_password: '',
        });
        setError(''); // Clear any previous error
      }
    } catch (err) {
      setError('Failed to add worker: ' + (err.response ? err.response.data.error : 'Unknown error'));
    }
  };

  const handleDeleteWorker = async (workerId) => {
    try {
      const response = await axios.delete('http://localhost:5000/accounts/workers/del', {
        data: { worker_id: workerId },
      });

      if (response.status === 200) {
        fetchWorkersAndPatients(); // Refetch workers after deletion
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
        fetchWorkersAndPatients(); // Refetch patients after deletion
      }
    } catch (err) {
      setError('Failed to delete patient');
    }
  };

  return (
    <div>
      <h2>Manage Accounts</h2>
      {error && <p style={{ color: 'red' }}>{error}</p>} {/* Display error if it exists */}

      <div>
        <h3>Workers</h3>
        <ul>
          {workers.length > 0 ? (
            workers.map((worker) => (
              <li key={worker.workerid}>
                <p>{worker.worker_name}</p>
                <p>{worker.worker_email}</p>
                <p>{worker.worker_role}</p>
                <button onClick={() => handleDeleteWorker(worker.workerid)}>Delete Worker</button>
              </li>
            ))
          ) : (
            <p>No workers available</p>
          )}
        </ul>

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
          <button type="submit">Add Worker</button>
        </form>
      </div>

      <div>
        <h3>Patients</h3>
        <ul>
          {patients.length > 0 ? (
            patients.map((patient) => (
              <li key={patient.healthid}>
                <p>{patient.patient_name}</p>
                <p>{patient.patient_email}</p>
                <button onClick={() => handleDeletePatient(patient.healthid)}>Delete Patient</button>
              </li>
            ))
          ) : (
            <p>No patients available</p>
          )}
        </ul>
      </div>
    </div>
  );
};

export default ManageAcc;

