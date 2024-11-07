import './StaffMain.css';
import React, { useState } from 'react';
import Profile from '../Profile/Profile';
import MainContence from '../Profile/MainContence';
import InsertTestResults from '../Results/InsertTestResults';


const StaffMain = () => {
  const [activeTab, setActiveTab] = useState('main');

  return (
    <div>
      {/* Tab Navigation */}
      <div className="stabs">
        <div
          className={`stab ${activeTab === 'profile' ? 'active' : ''}`}
          onClick={() => setActiveTab('profile')}
        >
          Profile
        </div>
        <div
          className={`stab ${activeTab === 'input' ? 'active' : ''}`}
          onClick={() => setActiveTab('input')}
        >
          Input Exam Results 
        </div>
      </div>

      {/* Render Tab Content */}
      <div className="stab-content">
        {activeTab === 'main' && <MainContence />}
        {activeTab === 'profile' && <Profile />}
        {activeTab === 'input' && <InsertTestResults />}
      </div>
    </div>
  );
};

export default StaffMain;

