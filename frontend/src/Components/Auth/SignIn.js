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
    <div className="sign-in-page">
      <div className="sign-in-container">
        <div className="left-section">
          <div className="decorative-circle"></div>
          <div className="main-title">GET IN TOUCH</div>
          <div className="main-subtitle">Tell us Your Problem</div>
          <button className="register-button" onClick={handleRedirectToRegister}>
            Register Today
          </button>
        </div>

        <div className="right-section">
          <button className="login-button" onClick={() => handleRedirectToLogin('patient')}>
            Patient Login
          </button>
          <button className="login-button" onClick={() => handleRedirectToLogin('worker')}>
            Staff Login
          </button>
        </div>
      </div>
    </div>
  );
};

export default SignIn;
