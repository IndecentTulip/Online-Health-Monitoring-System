import './Register.css';
import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

const Register = () => {
  const navigate = useNavigate();
  const [error, setError] = useState('');
  const [doctors_list, setDList] = useState([]);
  const [patientName, setPName] = useState('');
  const [email, setEmail] = useState('');
  const [phoneNumber, setPhone] = useState('');
  const [dob, setDOB] = useState('');
  const [docID, setDocID] = useState('');
  const [password, setPassword] = useState('');

  // Fetch the doctors list from the backend
  useEffect(() => {
    const fetchDoctors = async () => {
      try {
        const response = await axios.get('http://localhost:5000/register');
        setDList(response.data);
      } catch (err) {
        setError('Request of the doctors failed.');
      }
    };

    fetchDoctors();
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();

    // Validate the phone number
    if (phoneNumber.length !== 10) {
      setError('Phone number must be exactly 10 digits long.');
      return; // Prevent form submission
    }

    // Validate password length
    if (password.length < 6) {
      setError('Password must be at least 6 characters long.');
      return;
    }

    try {
      // Send the plain password directly (no hashing)
      const response = await axios.post('http://localhost:5000/register', {
        patientName,
        email,
        phoneNumber,
        dob,
        docID,
        password // Send the plain password here
      });

      console.log('Registration successful:', response.data);
      if (response.data.confirm === "OK"){
        navigate('/');
      } else if (response.data.confirm === "ERROR") {
        setError('Registration failed. Account with the same email already exists.');
      } else {
        setError('Registration failed. Something went wrong');
      }
    } catch (err) {
      setError('Registration failed. Please check your input and try again.');
    }
  };

  return (
    <div className="register-page">
      <div className="form-container">
        <h2>Patient Registration Form</h2>
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label>Name</label>
            <input
              type="text"
              value={patientName}
              onChange={(e) => setPName(e.target.value)}
              placeholder="Enter your name"
              required
            />
          </div>
          <div className="form-group">
            <label>Email</label>
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="Enter your email"
              required
            />
          </div>
          <div className="form-group">
            <label>Phone Number</label>
            <input
              type="tel"
              value={phoneNumber}
              onChange={(e) => setPhone(e.target.value)}
              placeholder="Enter your phone number"
              required
            />
          </div>
          <div className="form-group">
            <label>Date of Birth</label>
            <input
              type="date"
              value={dob}
              onChange={(e) => setDOB(e.target.value)}
              required
            />
          </div>
          <div className="form-group">
            <label>Assign a Doctor</label>
            <select onChange={(e) => setDocID(e.target.value)} required>
              <option value="">Select a Doctor</option>
              {Array.isArray(doctors_list) && doctors_list.map((doctor, index) => (
                <option key={index} value={doctor.id}>{doctor.email}</option>
              ))}
            </select>
          </div>
          <div className="form-group">
            <label>Password</label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="Enter your password"
              required
            />
          </div>
          <button type="submit" className="submit-button">Submit</button>
        </form>
        {error && <p className="error-message">{error}</p>}
      </div>
    </div>
  );
};

export default Register;