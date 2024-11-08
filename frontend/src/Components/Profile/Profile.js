import React, { useEffect, useState } from 'react';
import { useRole } from '../../Utils/RoleContext';
import axios from 'axios';

const Profile = ({ userId }) => {
  const { role } = useRole(); // Get the role from context
  const [profileData, setProfileData] = useState(null);
  const [error, setError] = useState(null);

  // use role (Patient to call API for patient)
  // use riles (Doctor, Staff, Administrator to call API for worker)
  return (
    <div></div>
  );
};

export default Profile;

