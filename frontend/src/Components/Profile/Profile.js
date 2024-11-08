import React, { useEffect, useState } from 'react';
import { useRole } from '../../Utils/RoleContext';
import axios from 'axios';

const Profile = ({ userId }) => {
  console.log("User ID in Profile:", userId)
  const { role } = useRole();
  const [profileData, setProfileData] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchProfileData = async () => {
      try {
        let response;


      // Fetch based on the user's role
        if (role === 'Patient') {
          response = await axios.get(`http://localhost:5000/profile/patient?id=${patientId}`);
        } else if (['Staff', 'Administrator', 'Doctor'].includes(role)) {
          response = await axios.get(`http://localhost:5000/profile/worker?id=${workerId}`);
        }
        // Update state with the fetched profile data
        setProfileData(response.data);
      } catch (error) {
        // Handle any error that occurs during the request
        console.error('Error fetching profile data:', error);
        setError('Failed to fetch profile data');
      }
    };

    fetchProfileData();
  }, [role]);

  return (
    <div>
      <h2>Profile Content for {role} with id {userId}</h2>
      {error && <p>{error}</p>}
      {profileData ? (
        <pre>{JSON.stringify(profileData, null, 2)}</pre> // Display profile data as JSON (for debugging)
      ) : (
        <p>Loading...</p>
      )}
    </div>
  );
};

export default Profile;

