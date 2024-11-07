import './SignIn.css';
import { useNavigate } from 'react-router-dom';

const SignIn = () => {
  const navigate = useNavigate();

  const handleRedirectToLogin = (userType) => {
    navigate(`/login?type=${userType}`); // Adjust the path as needed
  };

  const handleRedirectToRegister = () => {
    navigate('/register'); // Adjust the path as needed
  };

  return (
    <div>
      <button onClick={() => handleRedirectToLogin('patient')}>Patient</button>
      <button onClick={() => handleRedirectToLogin('worker')}>Worker</button>
      <button onClick={handleRedirectToRegister}>Don't have an account</button>
    </div>
  );
};

export default SignIn;

