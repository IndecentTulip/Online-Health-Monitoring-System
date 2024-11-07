import './AdminMain.css';
import React, { useState } from 'react';

const AdminMain = () => {
  const [activeTab, setActiveTab] = useState('main');
  const [activeDropdown, setActiveDropdown] = useState(null); // Track active dropdown

  // Toggle dropdown visibility, close the others when a new one is opened
  const toggleDropdown = (dropdown) => {
    setActiveDropdown(activeDropdown === dropdown ? null : dropdown);
  };

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
              <div onClick={() => setActiveTab('yearly')}>Yearly/Monthly Report</div>
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
              <div onClick={() => setActiveTab('delete')}>Delete</div>
              <div onClick={() => setActiveTab('create')}>Create</div>
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

