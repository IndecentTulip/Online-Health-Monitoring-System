import React, { useState, useEffect } from 'react';
import axios from 'axios';

const ManageAcc = ({ userId }) => {
  const [workers, setWorkers] = useState([]);
  const [patients, setPatients] = useState([]);
  const [newWorker, setNewWorker] = useState({
    worker_name: '',
    worker_email: '',
    worker_role: '',
  });
  const [error, setError] = useState('');

  // Fetch workers and patients on component mount
  useEffect(() => {
    const fetchWorkersAndPatients = async () => {
      try {
        const workerResponse = await axios.get('http://localhost:5000/accounts/workers/fetch');
        setWorkers(workerResponse.data);

        const patientResponse = await axios.get('http://localhost:5000/accounts/patient/fetch');
        setPatients(patientResponse.data);
      } catch (err) {
        setError('Failed to fetch workers and patients');
      }
    };

    fetchWorkersAndPatients();
  }, []);

  // Handle adding a new worker
  const handleAddWorker = async () => {
    try {
      const response = await axios.post('http://localhost:5000/accounts/workers/add', {
        worker_name: newWorker.worker_name,
        worker_email: newWorker.worker_email,
        worker_role: newWorker.worker_role,
      });

      if (response.status === 201) {
        setWorkers([...workers, response.data.worker]);
        setNewWorker({ worker_name: '', worker_email: '', worker_role: '' });
      }
    } catch (err) {
      setError('Failed to add worker');
    }
  };

  // Handle deleting a worker
  const handleDeleteWorker = async (workerId) => {
    try {
      const response = await axios.delete('http://localhost:5000/accounts/workers/del', {
        data: { worker_id: workerId },
      });

      if (response.status === 200) {
        setWorkers(workers.filter(worker => worker.workerid !== workerId));
      }
    } catch (err) {
      setError('Failed to delete worker');
    }
  };

  // Handle deleting a patient
  const handleDeletePatient = async (patientId) => {
    try {
      const response = await axios.delete('http://localhost:5000/accounts/patient/del', {
        data: { patient_id: patientId },
      });

      if (response.status === 200) {
        setPatients(patients.filter(patient => patient.healthid !== patientId));
      }
    } catch (err) {
      setError('Failed to delete patient');
    }
  };

  return (
    <div>
      <h2>Manage Accounts</h2>
      {error && <p style={{ color: 'red' }}>{error}</p>}

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
        <input
          type="text"
          value={newWorker.worker_name}
          onChange={(e) => setNewWorker({ ...newWorker, worker_name: e.target.value })}
          placeholder="Worker Name"
        />
        <input
          type="email"
          value={newWorker.worker_email}
          onChange={(e) => setNewWorker({ ...newWorker, worker_email: e.target.value })}
          placeholder="Worker Email"
        />
        <input
          type="text"
          value={newWorker.worker_role}
          onChange={(e) => setNewWorker({ ...newWorker, worker_role: e.target.value })}
          placeholder="Worker Role"
        />
        <button onClick={handleAddWorker}>Add Worker</button>
      </div>

      <div>
        <h3>Patients</h3>
        <ul>
          {patients.length > 0 ? (
            patients.map((patient) => (
              <li key={patient.healthid}>
                <p>{patient.patientname}</p>
                <p>{patient.email}</p>
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

