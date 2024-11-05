
import './Main.css';
import { useNavigate } from 'react-router-dom';

const AdminMain = () => {
  const navigate = useNavigate();

  const handleRedirectAccountManagment = () => {
    navigate('/administrator/accmanagment'); // Adjust the path as needed
  }  
  const test = () => {
    navigate('/patient/main'); // Adjust the path as needed
  };
;

  return (
    <div>
      AdminMain
      <button onClick={handleRedirectAccountManagment}>Manage Accounts</button>
      <button onClick={test}>test</button>
    </div>
  );
};

export default AdminMain;
