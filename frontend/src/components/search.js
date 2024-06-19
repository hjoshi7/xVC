import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Box, Paper, InputBase, IconButton, Grid } from '@mui/material';
import SearchIcon from '@mui/icons-material/Search';
import ArrowBackIosNewIcon from '@mui/icons-material/ArrowBackIosNew';
import './search.css';

const Search = () => {
  const [searchTerm, setSearchTerm] = useState('');
  const navigate = useNavigate();

  const handleSearch = () => {
    console.log("Search Term:", searchTerm);
    if (searchTerm.startsWith('@')) {
      const username = searchTerm.slice(1); // Remove the @ symbol
      console.log("Navigating to profile:", username);
      navigate(``);
      navigate(`/profile/${username}`);
    }
  };

  const handleKeyPress = (event) => {
    if (event.key === 'Enter') {
      event.preventDefault(); // Prevent the form from being submitted
      handleSearch();
    }
  };

  return (

    <Box className="feed">
      <Box className="searchMain">

        <Paper component="form" className="search-bar">
        <IconButton aria-label="go back" onClick={() => navigate(-1)}>
          <ArrowBackIosNewIcon sx={{ color: "#fff"}}/>
        </IconButton>
          <IconButton className="search-icon" aria-label="search" onClick={handleSearch} onKeyPr>
            <SearchIcon />
          </IconButton>
          <InputBase
            className="search-input"
            placeholder="Search 𝕏VC"
            inputProps={{ 'aria-label': 'search twitter' }}
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            onKeyPress={handleKeyPress}
          />
        </Paper>
      </Box>
    </Box>
  );
};

export default Search;