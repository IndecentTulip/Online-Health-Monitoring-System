import './DoctorMain.css';
import React, { useState } from 'react';
import TestResultsPatient from './TestResultsPatient';
import Profile from './Profile';
import MainContence from './MainContence';

const DoctorMain = () => {
  const [activeTab, setActiveTab] = useState('main');

  return (
    <div>
      {/* Tab Navigation */}
      <div className="dtabs">
        <div
          className={`dtab ${activeTab === 'profile' ? 'active' : ''}`}
          onClick={() => setActiveTab('profile')}
        >
          Profile
        </div>
        <div
          className={`dtab ${activeTab === 'test' ? 'active' : ''}`}
          onClick={() => setActiveTab('test')}
        >
          Test Results
        </div>
        <div
          className={`dtab ${activeTab === 'main' ? 'active' : ''}`}
          onClick={() => setActiveTab('main')}
        >
          Main Content
        </div>
      </div>

      {/* Render Tab Content */}
      <div className="dtab-content">
        {activeTab === 'profile' && <Profile />}
        {activeTab === 'test' && <TestResultsPatient />}
        {activeTab === 'main' && <MainContence />}
      </div>
    </div>
  );
};

export default DoctorMain;

