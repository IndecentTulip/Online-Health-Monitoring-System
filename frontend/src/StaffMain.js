import './StaffMain.css';
import React, { useState } from 'react';
import TestResultsPatient from './TestResultsPatient';
import Profile from './Profile';
import MainContence from './MainContence';

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
          className={`stab ${activeTab === 'test' ? 'active' : ''}`}
          onClick={() => setActiveTab('test')}
        >
          Test Results
        </div>
        <div
          className={`stab ${activeTab === 'main' ? 'active' : ''}`}
          onClick={() => setActiveTab('main')}
        >
          Main Content
        </div>
      </div>

      {/* Render Tab Content */}
      <div className="stab-content">
        {activeTab === 'profile' && <Profile />}
        {activeTab === 'test' && <TestResultsPatient />}
        {activeTab === 'main' && <MainContence />}
      </div>
    </div>
  );
};

export default StaffMain;

