import React from 'react';

const Dashboard = ({ user }) => {
    return (
        <div>
            <h1>Welcome, {user.username}!</h1>
            {/* Display additional information here */}
        </div>
    );
};

export default Dashboard;

