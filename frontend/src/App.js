import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Main from './Main';
import SignIn from './SignIn';
import LogIn from './LogIn'
import Register from './Register'

const App = () => {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Main />} />
        <Route path="/signin" element={<SignIn />} />
        <Route path="/login" element={<LogIn />} />
        <Route path="/register" element={<Register />} />
      </Routes>
    </Router>
  );
};

export default App;

