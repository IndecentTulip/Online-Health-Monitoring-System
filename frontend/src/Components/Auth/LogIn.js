import './LogIn.css';
import React, { useState } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import axios from 'axios';
import { useRole } from '../../Utils/RoleContext';

const Login = () => {
  const { setRole } = useRole();
  const navigate = useNavigate();
  const location = useLocation();
  const queryParams = new URLSearchParams(location.search);
  const userType = queryParams.get('type');

  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post('http://localhost:5000/login', {
        userType,
        email,
        password,
      });

      setError(''); // Clear any previous errors

      const { user_type, routeTo, id } = response.data.login;

      if (user_type === "Error") {
        setError('Your account is not approved yet. Please contact support.');
        return; // Exit early if the account is not approved
      }

      let route = routeTo;
      setRole(route);
      navigate(`/${route.toLowerCase()}/main`, { state: { id } });

    } catch (err) {
      if (err.response && err.response.data.error) {
        // Handle error messages returned from the backend
        setError(err.response.data.error);
      } else {
        setError('Login failed. Please check your credentials and try again.');
      }
    }
  };

  return (
    <div className="login-page">
      <div className="quote-container">
        <div className="quote-open">“</div>
        <div className="login-container">
          <h1>{userType === 'patient' ? 'Patient Login' : 'Worker Login'}</h1>
          <form onSubmit={handleSubmit}>
            <input
              type="text"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="Email"
              id="email-field"
              required
            />
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="Password"
              id="password-field"
              required
            />
            <a href="#" className="forgot-password">
              Forgot Password?
            </a>
            <button type="submit" id="submit-button">
              Login
            </button>
          </form>
          {error && <p style={{ color: 'red' }}>{error}</p>}
        </div>
        <div className="quote-close">”</div>
      </div>
    </div>
  );
};

export default Login;
