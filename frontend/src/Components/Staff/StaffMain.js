import './StaffMain.css';
import React, { useState } from 'react';
import { useLocation } from 'react-router-dom';
import Profile from '../Profile/Profile';
import MainContence from '../Profile/MainContence';
import InsertTestResults from '../Results/InsertTestResults';
import UpdateTestResults from '../Results/UpdateTestResults';

const StaffMain = () => {
  const [activeTab, setActiveTab] = useState('main');
  const location = useLocation();
  const userId = location.state?.id;
  console.log("id:", userId)



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
        <div
          className={`stab ${activeTab === 'update' ? 'active' : ''}`}
          onClick={() => setActiveTab('update')}
        >
          Update Exam Results 
        </div>
      </div>

      {/* Render Tab Content */}
      <div className="stab-content">
        {activeTab === 'main' && <MainContence userId={userId} />}
        {activeTab === 'profile' && <Profile userId={userId} />}
        {activeTab === 'input' && <InsertTestResults userId={userId} />}
        {activeTab === 'update' && <UpdateTestResults userId={userId} />}
      </div>
    </div>
  );
};

export default StaffMain;

