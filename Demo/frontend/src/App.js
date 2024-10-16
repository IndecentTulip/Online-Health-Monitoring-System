import React, { useState } from 'react';
import Login from './Login';
import Dashboard from './Dashboard';

const App = () => {
    const [user, setUser] = useState(null);

    return (
        <div>
            {!user ? <Login setUser={setUser} /> : <Dashboard user={user} />}
        </div>
    );
};

export default App;


//import React, { useState } from 'react';
//import { BrowserRouter as Router, Route, Switch, Redirect } from 'react-router-dom';
//import Login from './Login';
//import Dashboard from './Dashboard';
//import Settings from './Settings'; // Another example component
//import NotFound from './NotFound'; // 404 page or fallback component
//
//const App = () => {
//    const [user, setUser] = useState(null);
//
//    return (
//        <Router>
//            <div>
//                <Switch>
//                    <Route path="/login">
//                        {user ? <Redirect to="/dashboard" /> : <Login setUser={setUser} />}
//                    </Route>
//                    <Route path="/dashboard">
//                        {user ? <Dashboard user={user} /> : <Redirect to="/login" />}
//                    </Route>
//                    <Route path="/settings">
//                        {user ? <Settings user={user} /> : <Redirect to="/login" />}
//                    </Route>
//                    <Route path="*">
//                        <NotFound />
//                    </Route>
//                </Switch>
//            </div>
//        </Router>
//    );
//};
//
//export default App;

