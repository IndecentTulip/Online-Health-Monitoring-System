
import './Main.css';
import { useNavigate } from 'react-router-dom';

const StaffMain = () => {
  const navigate = useNavigate();

  const handleRedirect = () => {
    navigate('/signin'); // Adjust the path as needed
  };

  return (
    <div>
      StaffMain
    </div>
  );
};

export default StaffMain;
