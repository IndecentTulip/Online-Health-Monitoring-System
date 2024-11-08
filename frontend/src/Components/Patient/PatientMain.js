import './PatientMain.css';
import React, { useState } from 'react';
import { useLocation } from 'react-router-dom';
import TestResultsPatient from '../Results/TestResultsPatient';
import Profile from '../Profile/Profile';
import MainContence from '../Profile/MainContence';

const PatientMain = () => {
  const [activeTab, setActiveTab] = useState('main');
  const location = useLocation();
  const userId = location.state?.id;
  console.log("id:", userId)


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
        {activeTab === 'main' && <MainContence userId={userId} />}
        {activeTab === 'profile' && <Profile userId={userId} />}
        {activeTab === 'test' && <TestResultsPatient userId={userId}  />}
      </div>
    </div>
  );
};

export default PatientMain;

