import './LogIn.css'

import { useLocation } from 'react-router-dom';

const Login = () => {
  const location = useLocation();
  const queryParams = new URLSearchParams(location.search);
  const userType = queryParams.get('type');

  return (
    <div>
      <h1>{userType === 'patient' ? 'Patient Login' : 'Worker Login'}</h1>
      {/* Add your login form here */}
    </div>
  );
};

export default Login;
