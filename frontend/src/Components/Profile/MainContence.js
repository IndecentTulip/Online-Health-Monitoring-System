import React from 'react';
import './MainContence.css'; // Importing the CSS file for styling

const MainContence = ({ userId }) => {
  return (
    <div className="main-content-container">
      <h2 className="title">Welcome to Your Dashboard</h2>
      <p className="default-message">
        This is the default content page. You'll move from here quickly once you choose something from the tabs above.
      </p>
      <div className="content-placeholder">
        <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.</p>
      </div>
    </div>
  );
};

export default MainContence;

