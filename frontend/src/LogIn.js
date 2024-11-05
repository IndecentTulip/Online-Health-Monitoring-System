import './LogIn.css';
import React, { useState } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import axios from 'axios';
import { useRole } from './RoleContext';

// TODO: Store user email and Type somewhere
// TODO: use userType to RESTRIC going into urls reserved to other userTypes

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
      setError(''); 
      let route = response.data.login.routeTo;
      console.log(route);
      //setRoutePerm(route);
      setRole(route);
      navigate(`/${route.toLowerCase()}/main`);
    } catch (err) {
      setError('Login failed. Please check your credentials and try again.');
    }
  };




  return (
    <div>
      <h1>{userType === 'patient' ? 'Patient Login' : 'Worker Login'}</h1>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          placeholder="Email"
          required
        />
        <input
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          placeholder="Password"
          required
        />
        <button type="submit">Login</button>
      </form>
      {error && <p style={{ color: 'red' }}>{error}</p>} {/* Display error if it exists */}
    </div>
  );
};

export default Login;

