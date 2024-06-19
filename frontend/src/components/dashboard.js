import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { Avatar, Box, Typography, Paper, Grid, List, ListItem, ListItemText } from '@mui/material';
import CircularProgress from "@mui/material/CircularProgress";
import AssistantIcon from '@mui/icons-material/Assistant';
import PeopleIcon from '@mui/icons-material/People';
import FavoriteIcon from '@mui/icons-material/Favorite';
import ListIcon from '@mui/icons-material/ListAlt';

import MentionGraph from './MentionGraph';
import SmoothLineGraph from './SmoothLineGraph';
import TweetEmbed from './trendingtweets';

const ProfileDashboard = () => {
  const { username } = useParams();
  const [profileData, setProfileData] = useState(null);
  const [graphData, setGraphData] = useState(null);
  // const [cacheData, setCacheData] = useState({});
  const [tweets_array, setTweetsArray] = useState([]);

  useEffect(() => {
  setGraphData(null);
  fetch(`http://127.0.0.1:8080/profile/${username}`)
    .then(response => response.json())
    .then(data => {setProfileData(data.data); 
  })
  .catch(error => {
    console.error('Failed to fetch profile data:', error);
    setProfileData(null);
});

  // for (const [key, value] of Object.entries(cacheData)) {
  //   if (username == key) {
  //     setGraphData(value);
  //     return;
  //   }
  // }

  fetch(`http://127.0.0.1:8080/data/${username}`)
    .then(response => response.json())
    .then(data => {setGraphData(data);
      // let tmp = {...cacheData};
      // tmp[username] = data;
      // setCacheData(tmp);
    })
  .catch(error => {
    console.error('Failed to fetch profile data:', error);
    setProfileData(null);
});


}, [username]);

 useEffect(() => {
  if (!graphData) {return;}
  setTweetsArray(graphData[2].map(tweetId => (
    <TweetEmbed tweetId={tweetId} />
  )));
 }, [graphData])




  if (!profileData || !graphData) {
    return   <div style={{ backgroundColor: "-moz-initial", minHeight: '100vh' }}> 
    <Box sx={{ display: "flex", justifyContent: "center", backgroundColor: "#15202b", height: '100px', width: '100%' }}>
      <CircularProgress style={{ color: '#50b7f5' }}/>
    </Box>
  </div>
  }
  return (
    <Grid container spacing={2}>
      <Grid item xs={12} md={8} >
        <Paper elevation={0} sx={{ p: 2, mb: 2, backgroundColor:"#15202b"}}>
          <Box sx={{ display: 'flex', alignItems: 'center', gap: 2,           borderRadius: '20px',
          background: 'linear-gradient(145deg, #15202b, #22303c)',
          margin: '25px',
          mb: 2}}>
            <Avatar
              sx={{ width: 128, height: 128 }}
              src={profileData.profile_image_url.replace('_normal', '_400x400')}
            />
            
            <Box sx={{flexDirection: 'column'}}>
            <div className='rowC'>
              <Typography variant="h4" sx={{ color: "#fff" }}><b>{profileData.name}</b></Typography>
              <Typography variant="body1" sx={{ color: "#50b7f5" }}>@{username}</Typography>
              <Typography variant="body2" sx={{ color: "#fff" }}>{profileData.description}</Typography>
            </div>
            <div>
            <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}> {/* Add gap for spacing */}
      <Box sx={{ display: 'flex', alignItems: 'center' }}>
        <PeopleIcon sx={{ color: '#fff' }} />
        <Typography variant="body2" sx={{ color: "#fff", ml: 0.5 }}>
          {profileData.public_metrics.followers_count}
        </Typography>
      </Box>
      <Box sx={{ display: 'flex', alignItems: 'center' }}>
        <FavoriteIcon sx={{ color: '#fff' }} />
        <Typography variant="body2" sx={{ color: "#fff", ml: 0.5 }}>
          {profileData.public_metrics.like_count} 
        </Typography>
      </Box>
      <Box sx={{ display: 'flex', alignItems: 'center' }}>
        <ListIcon sx={{ color: '#fff' }} />
        <Typography variant="body2" sx={{ color: "#fff", ml: 0.5 }}>
          {profileData.public_metrics.listed_count}
        </Typography>
      </Box>

    </Box>
            </div>
            </Box>
            <Box sx={{}}>
              
            </Box>
          </Box>
        </Paper>
        <Box sx={{ borderRadius: '20px',
          background: 'linear-gradient(145deg, #15202b, #22303c)',
          margin: '25px',
          marginTop: '5px',
          mb: 2}}>
         
          <Typography variant="h4" sx={{ color: "#fff", flexGrow: 1 }}>
          <AssistantIcon style={{ color: '#FFFFFF'}} />
        <b> Grok description</b>
      </Typography>
          <Typography variant="body2" sx={{ color: "#fff" }}>{graphData[3]}</Typography>

          <Box sx={{margin:'50px'}}>

</Box>
          </Box>
        <Box sx={{
          borderRadius: '20px',
          background: 'linear-gradient(145deg, #15202b, #22303c)',
          margin: '25px',
          mb: 2
        }}>
  
          <SmoothLineGraph data={{ x: graphData[0], y: graphData[1] }} layout={{ width: 700, height: 400, margin: { t: 40, b: 40, l: 40, r: 40 } }} />
          </Box>
          <Box sx={{margin:'50px'}}>

          </Box>

          <Box sx={{
          borderRadius: '20px',
          background: 'linear-gradient(145deg, #15202b, #22303c)',
          margin: '25px',
          mb: 2
        }}>

          <MentionGraph data={{ x: graphData[4], y: graphData[5] }} layout={{ width: 700, height: 400, margin: { t: 40, b: 40, l: 40, r: 40 } }} />
          </Box>
      </Grid>
      <Grid item xs={12} md={4}>
        <Paper elevation={1} sx={{ height: '1350px', overflow: 'auto', bgcolor: '#15202b', color: 'white', p: 2 }}>
        <Typography variant="h6" sx={{ mb: 2 }}>
      <b>Trending Tweets for @{username}</b>
    </Typography>
    <List>
          {tweets_array}
          {/* {tweets} */}
        </List>
        </Paper>
      </Grid>
    </Grid>
  );
};
    
    

export default ProfileDashboard;