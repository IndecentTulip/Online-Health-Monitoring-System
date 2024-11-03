import './Register.css'
import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';


const Register = () => {
  const navigate = useNavigate();
  const [error, setError] = useState('');
  const [doctors_list, setDList] = useState([]);

// INSERT INTO patient (healthID, patientName, email, phoneNumber, DOB, status, doctorID, patientPassword)
  const [patientName, setPName] = useState('');
  const [email, setEmail] = useState('');
  const [phoneNumber, setPhone] = useState('');
  const [dob, setDOB] = useState('');
  const status = false;
  // set DocID based on the email
  const [docID, setDocID] = useState('');
  const [password, setPassword] = useState('');


  useEffect(() => {
    const fetchDoctors = async () => {
      try {
        const response = await axios.get('http://localhost:5000/register');
        console.log(response.data)
        setDList(response.data);
      } catch (err) {
        setError('Request of the doctors failed.');
      }
    };

    fetchDoctors();
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post('http://localhost:5000/register', {
        patientName,
        email,
        phoneNumber,
        dob,
        status,
        docID,
        password
      });
    } catch (err) {
      setError('Registration failed. Please check your input and try again.');
    }
  };


// INSERT INTO patient (healthID, patientName, email, phoneNumber, DOB, status, doctorID, patientPassword)
  return (
     <form onSubmit={handleSubmit}>
        <input
          type="text"
          value={patientName}
          onChange={(e) => setPName(e.target.value)}
          placeholder="name"
          required
        />
        <input
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          placeholder="Email"
          required
        />
        <input
          type="tel"
          value={phoneNumber}
          onChange={(e) => setPhone(e.target.value)}
          placeholder="phone number"
          required
        />
        <input
          type="date"
          value={dob}
          onChange={(e) => setDOB(e.target.value)}
          placeholder="YYYY-MM-DD"
          required
        />
        <select onChange={(e) => setDocID(e.target.value)} required>
          <option value="">Select a Doctor</option>
          {Array.isArray(doctors_list) && doctors_list.map((doctor, index) => (
          <option key={index} value={doctor.id}>{doctor.email}</option>
          ))}
        </select>
        <input
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          placeholder="password"
          required
        />




       <button type="submit">submit</button>
     </form>

  );

};

export default Register;

