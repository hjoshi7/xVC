import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom'; // Import useNavigate hook
import './BoxComponent.css';

const BoxComponent = ({ gradient1, gradient2, name, category }) => {
  const [profileData, setProfileData] = useState(null);
  const navigate = useNavigate(); // Initialize navigate function

  useEffect(() => {
    fetch(`http://127.0.0.1:8080/profile/${name}`)
      .then(response => response.json())
      .then(data => {
        setProfileData(data.data); 
      })
      .catch(error => {
        console.error('Failed to fetch profile data:', error);
        setProfileData(null);
      });
  }, [name]);

  if (!profileData) {
    return <p>Loading...</p>;
  }

  // Function to handle click event
  const handleClick = () => {
    navigate(`/profile/${name}`); // Navigate to the profile page
  };

  return (
    <button className="box" style={{ backgroundImage: `linear-gradient(${gradient1}, ${gradient2})` }} onClick={handleClick}>
      <div className="content">
        <img src={profileData.profile_image_url.replace('_normal', '_400x400')} alt={profileData.name} className="logo" />
        <div>
          <h2 className="title">{profileData.name}</h2>
          <div className="category">{category}</div>
        </div>
      </div>
      <p className="description">{profileData.description}</p>
    </button>
  );
};

export default BoxComponent;
