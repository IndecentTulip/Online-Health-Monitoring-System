// App.js
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Main from './Main';
import SignIn from './Components/Auth/SignIn';
import LogIn from './Components/Auth/LogIn';
import Register from './Components/Auth/Register';
import PatientMain from './Components/Patient/PatientMain';
import DoctorMain from './Components/Doctor/DoctorMain';
import StaffMain from './Components/Staff/StaffMain';
import AdminMain from './Components/Admin/AdminMain';
import { RoleProvider, useRole } from './Utils/RoleContext'; // Import your context


// TODO CHNAGE(USE) THIS BEFORE SUBMISSION
const roleRoutes = {
//  Patient: [
//    { path: '/patient/main', component: PatientMain },
//  ],
//  Doctor: [
//    { path: '/doctor/main', component: DoctorMain },
//  ],
//  Staff: [
//    { path: '/staff/main', component: StaffMain },
//  ],
//  Administrator: [
//    { path: '/administrator/main', component: AdminMain },
//  ],
};

const PrivateRoute = ({ children, allowedRoles }) => {
  const { role } = useRole();
  return allowedRoles.includes(role) ? children : <Navigate to="/" />;
};

const App = () => {
  return (
    <RoleProvider> {/* RoleProvider only exist for me to set a role and then be able to use it to check perm for routes */}
      <Router>
        <Routes>
          <Route path="/" element={<Main />} />
          <Route path="/signin" element={<SignIn />} />
          <Route path="/register" element={<Register />} />
          <Route path="/login" element={<LogIn />} />
          
          <Route path="/patient/main" element={<PatientMain />} />
          <Route path="/doctor/main" element={<DoctorMain />} />
          <Route path="/staff/main" element={<StaffMain />} />
          <Route path="/administrator/main" element={<AdminMain />} />


          {/* Use the role context in routes */}
          {Object.entries(roleRoutes).map(([role, routes]) => (
            routes.map(({ path, component: Component }) => (
              <Route 
                key={path} 
                path={path} 
                element={
                  <PrivateRoute allowedRoles={[role]}>
                    <Component />
                  </PrivateRoute>
                } 
              />
            ))
          ))}
        </Routes>
      </Router>
    </RoleProvider>
  );
};

export default App;

