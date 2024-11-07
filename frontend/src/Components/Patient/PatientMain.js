import './PatientMain.css';
import React, { useState } from 'react';
import TestResultsPatient from '../Results/TestResultsPatient';
import Profile from '../Profile/Profile';
import MainContence from '../Profile/MainContence';

const PatientMain = () => {
  const [activeTab, setActiveTab] = useState('main');

  return (
    <div>
      {/* Tab Navigation */}
      <div className="ptabs">
        <div
          className={`ptab ${activeTab === 'profile' ? 'active' : ''}`}
          onClick={() => setActiveTab('profile')}
        >
          Profile
        </div>
        <div
          className={`ptab ${activeTab === 'test' ? 'active' : ''}`}
          onClick={() => setActiveTab('test')}
        >
          Test Results
        </div>
      </div>

      {/* Render Tab Content */}
      <div className="ptab-content">
        {activeTab === 'profile' && <Profile />}
        {activeTab === 'test' && <TestResultsPatient />}
        {activeTab === 'main' && <MainContence />}
      </div>
    </div>
  );
};

export default PatientMain;

