
import './Main.css';
import { useNavigate } from 'react-router-dom';

const PatientMain = () => {
  const navigate = useNavigate();

  const handleRedirect = () => {
    navigate('/signin'); // Adjust the path as needed
  };


  return (
    <div>
      PatientMain
    </div>
  );
};

export default PatientMain;
