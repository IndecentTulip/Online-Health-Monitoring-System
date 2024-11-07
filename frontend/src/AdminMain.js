import './AdminMain.css';
import React, { useState } from 'react';
import TestResultsPatient from './TestResultsPatient';
import Profile from './Profile';
import MainContence from './MainContence';

const AdminMain = () => {
  const [activeTab, setActiveTab] = useState('main');

  return (
    <div>
      {/* Tab Navigation */}
      <div className="atabs">
        <div
          className={`atab ${activeTab === 'profile' ? 'active' : ''}`}
          onClick={() => setActiveTab('profile')}
        >
          Profile
        </div>

        {/* Manage Reports Dropdown */}
        <div className="atab-dropdown">
          <div
            className={`atab ${activeTab === 'reports' ? 'active' : ''}`}
            onClick={() => setActiveTab('reports')}
          >
            Manage Reports
          </div>
          <div className="dropdown-content">
            <div onClick={() => setActiveTab('prediction')}>Prediction Report</div>
            <div onClick={() => setActiveTab('yearly')}>Yearly/Monthly Report</div>
          </div>
        </div>

        {/* Manage Accounts Dropdown */}
        <div className="atab-dropdown">
          <div
            className={`atab ${activeTab === 'accounts' ? 'active' : ''}`}
            onClick={() => setActiveTab('accounts')}
          >
            Manage Accounts
          </div>
          <div className="dropdown-content">
            <div onClick={() => setActiveTab('approve')}>Approve</div>
            <div onClick={() => setActiveTab('delete')}>Delete</div>
            <div onClick={() => setActiveTab('create')}>Create</div>
          </div>
        </div>

        <div
          className={`atab ${activeTab === 'delresults' ? 'active' : ''}`}
          onClick={() => setActiveTab('delresults')}
        >
          Delete Test Results
        </div>
      </div>

      {/* Render Tab Content */}
      <div className="atab-content">
        {activeTab === 'profile' && <Profile />}
        {activeTab === 'test' && <TestResultsPatient />}
        {activeTab === 'main' && <MainContence />}
        {activeTab === 'prediction' && <div>Prediction Report Content</div>}
        {activeTab === 'yearly' && <div>Yearly/Monthly Report Content</div>}
        {activeTab === 'approve' && <div>Approve Accounts Content</div>}
        {activeTab === 'delete' && <div>Delete Accounts Content</div>}
        {activeTab === 'create' && <div>Create Account Content</div>}
        {activeTab === 'delresults' && <div>Delete Test Results Content</div>}
      </div>
    </div>
  );
};

export default AdminMain;
