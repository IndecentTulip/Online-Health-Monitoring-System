import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Main from './Main';
import SignIn from './SignIn';
import LogIn from './LogIn'
import Register from './Register'
import PatientMain from './PatientMain'
import DoctorMain from './DoctorMain'
import StaffMain from './StaffMain'
import AdminMain from './AdminMain'

const App = () => {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Main />} />
        <Route path="/signin" element={<SignIn />} />
        <Route path="/login" element={<LogIn />} />
        <Route path="/register" element={<Register />} />
        <Route path="/patientmain" element={<PatientMain />} />
        <Route path="/doctormain" element={<DoctorMain />} />
        <Route path="/staffmain" element={<StaffMain />} />
        <Route path="/administratormain" element={<AdminMain />} />
      </Routes>
    </Router>
  );
};

export default App;

