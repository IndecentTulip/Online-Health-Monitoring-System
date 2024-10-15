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


