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

    if (phoneNumber.length !== 10) {
      setError('Phone number must be exactly 10 digits long.');
      return;
    }

    if (password.length < 6) {
      setError('Password must be at least 6 characters long.');
      return;
    }

    try {
      const response = await axios.post('http://localhost:5000/register', {
        patientName,
        email,
        phoneNumber,
        dob,
        docID,
        password
      });

      if (response.data.confirm === "OK") {
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
            <label>First Name</label>
            <input
              type="text"
              value={patientName}
              onChange={(e) => setPName(e.target.value)}
              placeholder="Enter your first name"
              required
            />
          </div>
          <div className="form-group">
            <label>Last Name</label>
            <input
              type="text"
              placeholder="Enter your last name"
              required
            />
          </div>
          <div className="form-group">
            <label>Health Card Number</label>
            <input
              type="text"
              placeholder="Enter your health card number"
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
            <label>Date of Birth (YYYY-MM-DD)</label>
            <input
              type="date"
              value={dob}
              onChange={(e) => setDOB(e.target.value)}
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
            <label>Message</label>
            <textarea placeholder="Enter your message here"></textarea>
          </div>
          <div className="form-group">
            <button type="submit" className="submit-button">Submit Now</button>
          </div>
        </form>
        {error && <p className="error-message">{error}</p>}
      </div>
    </div>
  );
};

export default Register;
