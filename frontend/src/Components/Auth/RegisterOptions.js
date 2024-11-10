import { useNavigate } from 'react-router-dom';
import './RegisterOptions.css'; // if we want to add styles

const RegisterOptions = () => {
  const navigate = useNavigate();

  const handleEmployeeRegistration = () => {
    navigate('/register/employee');
  };

  const handlePatientRegistration = () => {
    navigate('/register/patient');
  };

  return (
    <div>
      <button onClick={handleEmployeeRegistration}>Employee Registration</button>
      <button onClick={handlePatientRegistration}>Patient Registration</button>
    </div>
  );
};

export default RegisterOptions;