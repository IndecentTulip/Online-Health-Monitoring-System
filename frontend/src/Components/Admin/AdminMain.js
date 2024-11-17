import './AdminMain.css';
import React, { useState } from 'react';
import { useLocation } from 'react-router-dom';
import DelResults from '../Results/DelTestResults';
import ApproveAcc from '../Accounts/ApproveAcc';
import ManageAcc from '../Accounts/ManageAcc';
import PredicRep from '../Reports/Prediction';
import YearMonthRep from '../Reports/YearNMonth';
import Profile from '../Profile/Profile';
import MainContence from '../Profile/MainContence';


const AdminMain = () => {
  const [activeTab, setActiveTab] = useState('main');
  const [activeDropdown, setActiveDropdown] = useState(null); // Track active dropdown

  const location = useLocation();
  const userId = location.state?.id;
  console.log("id:", userId)

  // Toggle dropdown visibility, close the others when a new one is opened
  const toggleDropdown = (dropdown) => {
    setActiveDropdown(activeDropdown === dropdown ? null : dropdown);
  };

  return (
    <div className="admin-container">
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
            onClick={() => {
              setActiveTab('reports');
              toggleDropdown('reports'); // Toggle Reports dropdown
            }}
          >
            Manage Reports
          </div>
          {activeDropdown === 'reports' && (
            <div className="dropdown-content">
              <div onClick={() => setActiveTab('prediction')}>Prediction Report</div>
              <div onClick={() => setActiveTab('yearlynmonthly')}>Yearly/Monthly Report</div>
            </div>
          )}
        </div>

        {/* Manage Accounts Dropdown */}
        <div className="atab-dropdown">
          <div
            className={`atab ${activeTab === 'accounts' ? 'active' : ''}`}
            onClick={() => {
              setActiveTab('accounts');
              toggleDropdown('accounts'); // Toggle Accounts dropdown
            }}
          >
            Manage Accounts
          </div>
          {activeDropdown === 'accounts' && (
            <div className="dropdown-content">
              <div onClick={() => setActiveTab('approve')}>Approve</div>
              <div onClick={() => setActiveTab('manage')}>Manage</div>
            </div>
          )}
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
        {activeTab === 'main' && <MainContence userId={userId}/>}
        {activeTab === 'profile' && <Profile userId={userId} />}
        {activeTab === 'prediction' && <PredicRep userId={userId} />}
        {activeTab === 'yearlynmonthly' && <YearMonthRep userId={userId} />}
        {activeTab === 'approve' && <ApproveAcc userId={userId} />}
        {activeTab === 'manage' && <ManageAcc userId={userId} />}
        {activeTab === 'delresults' && <DelResults userId={userId} />}
      </div>
    </div>
  );
};

export default AdminMain;

