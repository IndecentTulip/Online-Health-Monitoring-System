
import './Main.css';
import { useNavigate } from 'react-router-dom';

const AdminMain = () => {
  const navigate = useNavigate();

  const handleRedirect = () => {
    navigate('/signin'); // Adjust the path as needed
  };

  return (
    <div>
      AdminMain
    </div>
  );
};

export default AdminMain;
