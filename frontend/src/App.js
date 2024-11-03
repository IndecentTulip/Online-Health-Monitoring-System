// App.js
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Main from './Main';
import SignIn from './SignIn';
import LogIn from './LogIn';
import Register from './Register';
import PatientMain from './PatientMain';
import DoctorMain from './DoctorMain';
import StaffMain from './StaffMain';
import AdminMain from './AdminMain';
import AccManage from './AccManage';
import { RoleProvider, useRole } from './RoleContext'; // Import your context

const roleRoutes = {
  Patient: [
    { path: '/patient/main', component: PatientMain },
  ],
  Doctor: [
    { path: '/doctor/main', component: DoctorMain },
  ],
  Staff: [
    { path: '/staff/main', component: StaffMain },
  ],
  Administrator: [
    { path: '/administrator/main', component: AdminMain },
    { path: '/administrator/accmanagment', component: AccManage },
  ],
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

