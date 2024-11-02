
import './Main.css';
import { useNavigate } from 'react-router-dom';

const DoctorMain = () => {
  const navigate = useNavigate();

  const handleRedirect = () => {
    navigate('/signin'); // Adjust the path as needed
  };

  return (
    <div>
      DoctorMain
    </div>
  );
};

export default DoctorMain;
