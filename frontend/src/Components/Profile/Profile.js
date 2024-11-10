import React, { useEffect, useState } from 'react';
import { useRole } from '../../Utils/RoleContext';
import axios from 'axios';

const Profile = ({ userId }) => {
  const { role } = useRole(); // Get the role from context (either 'patient' or 'worker')
  const [profileData, setProfileData] = useState(null);
  const [editData, setEditData] = useState(null); // To store the data for editing
  const [error, setError] = useState(null);
  const [successMessage, setSuccessMessage] = useState(null); // Success message after update
  const [loading, setLoading] = useState(false); // Loading state for the API request

  // Determine the API endpoint based on the role
  const apiEndpoint = role === 'Patient'
    ? `http://localhost:5000/profile/patient/view?patient_id=${userId}`
    : `http://localhost:5000/profile/worker/view?worker_id=${userId}`;

  const patchApiEndpoint = role === 'Patient'
    ? `http://localhost:5000/profile/patient/edit?patient_id=${userId}`
    : `http://localhost:5000/profile/worker/edit?worker_id=${userId}`;

  // Fetch the profile data
  useEffect(() => {
    const fetchProfileData = async () => {
      try {
        const response = await axios.get(apiEndpoint);
        setProfileData(response.data);
        setEditData(response.data); // Initialize edit data
      } catch (err) {
        setError('Failed to load profile data');
      }
    };

    if (userId) {
      fetchProfileData();
    }
  }, [apiEndpoint, userId]);

  // Handle input changes for the edit form
  const handleChange = (e) => {
    const { name, value } = e.target;
    setEditData(prevData => ({
      ...prevData,
      [name]: value,
    }));
  };

  // Handle form submission to update the profile
  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setSuccessMessage(null);
    setError(null);

    try {
      const response = await axios.patch(patchApiEndpoint, editData, {
        headers: { 'Content-Type': 'application/json' }
      });
      if (response.status === 200) {
        setSuccessMessage('Profile updated successfully!');
        setProfileData(editData); // Update the profileData with the edited data
      }
    } catch (err) {
      setError('Failed to update profile');
    } finally {
      setLoading(false);
    }
  };

  if (error) {
    return <div style={{ color: 'red' }}>{error}</div>;
  }

  return (
    <div>
      <h2>{role === 'Patient' ? 'Patient Profile' : 'Worker Profile'}</h2>

      {successMessage && <div style={{ color: 'green' }}>{successMessage}</div>}

      {profileData ? (
        <form onSubmit={handleSubmit}>
          <div>
            <label>
              <strong>Name:</strong>
              <input
                type="text"
                name="name"
                value={editData.name || ''}
                onChange={handleChange}
              />
            </label>
          </div>

          <div>
            <label>
              <strong>Email:</strong>
              <input
                type="email"
                name="email"
                value={editData.email || ''}
                onChange={handleChange}
              />
            </label>
          </div>

          <div>
            <label>
              <strong>Phone:</strong>
              <input
                type="tel"
                name="phone"
                value={editData.phone || ''}
                onChange={handleChange}
              />
            </label>
          </div>

          <button type="submit" disabled={loading}>
            {loading ? 'Updating...' : 'Update Profile'}
          </button>
        </form>
      ) : (
        <p>Loading profile...</p>
      )}
    </div>
  );
};

export default Profile;

