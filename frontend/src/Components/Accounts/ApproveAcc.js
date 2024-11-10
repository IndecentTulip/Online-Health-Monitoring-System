import React, { useState, useEffect } from 'react';
import axios from 'axios';

const ApproveAcc = () => {
  const [patients, setPatients] = useState([]);
  const [pendingPatients, setPendingPatients] = useState([]);
  const [error, setError] = useState('');

  // Fetch all patients on component mount
  useEffect(() => {
    const fetchPatients = async () => {
      try {
        const response = await axios.get('http://localhost:5000/accounts/patient/fetch');
        setPatients(response.data);
        
        // Filter patients by status (status = false means pending approval)
        const pending = response.data.filter(patient => !patient.status);
        setPendingPatients(pending);
      } catch (err) {
        setError('Failed to fetch patients');
      }
    };

    fetchPatients();
  }, []);

  // Handle patient approval (set status to true)
  const handleApprove = async (patientId) => {
    try {
      const response = await axios.patch('http://localhost:5000/accounts/patient/update', {
        patient_id: patientId,
      });

      if (response.status === 200) {
        // Remove the approved patient from the pending list (client-side update)
        setPendingPatients(prevPatients => prevPatients.filter(patient => patient.healthid !== patientId));
      }
    } catch (err) {
      setError('Failed to approve patient');
    }
  };

  return (
    <div>
      <h2>Approve Accounts</h2>
      {error && <p style={{ color: 'red' }}>{error}</p>}
      
      {pendingPatients.length > 0 ? (
        <ul>
          {pendingPatients.map((patient) => (
            <li key={patient.healthid}>
              <div>
                <p>{patient.patientname}</p>
                <p>{patient.email}</p>
                <button onClick={() => handleApprove(patient.healthid)}>
                  Approve Account
                </button>
              </div>
            </li>
          ))}
        </ul>
      ) : (
        <p>No pending patients</p>
      )}
    </div>
  );
};

export default ApproveAcc;

