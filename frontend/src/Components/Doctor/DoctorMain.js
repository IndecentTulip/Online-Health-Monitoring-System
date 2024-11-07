import './DoctorMain.css';
import React, { useState } from 'react';
import Profile from '../Profile/Profile';
import MainContence from '../Profile/MainContence';
import TestResultsDoctor from '../Results/TestResultsDoctor';
import PrescExam from '../Exam/PrescExam';
import Monitor from '../Monitor/Monitor';


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
          className={`dtab ${activeTab === 'prescexam' ? 'active' : ''}`}
          onClick={() => setActiveTab('prescexam')}
        >
          Prescribe Exam
        </div>
        <div
          className={`dtab ${activeTab === 'monitor' ? 'active' : ''}`}
          onClick={() => setActiveTab('monitor')}
        >
          Manage Smart Monitor
        </div>

      </div>

      {/* Render Tab Content */}
      <div className="dtab-content">
        {activeTab === 'main' && <MainContence />}
        {activeTab === 'profile' && <Profile />}
        {activeTab === 'test' && <TestResultsDoctor />}
        {activeTab === 'prescexam' && <PrescExam />}
        {activeTab === 'monitor' && <Monitor />}
      </div>
    </div>
  );
};

export default DoctorMain;

