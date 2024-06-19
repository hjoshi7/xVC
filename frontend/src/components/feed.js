import React from 'react';
import BoxComponent from './BoxComponent'; // Make sure this path is correct for your project
import { Typography } from '@mui/material';

// Define the props for each box in an array
const boxData = [
  {
    gradient1: '#FF5F6D',
    gradient2: '#FFC371',
    name: 'cradlewise',
    category: ''
  },
  {
    gradient1: '#673B8B',
    gradient2: '#B767F6',
    name: 'getkarate',
    category: ''
  },
  {
    gradient1: '#3B778B',
    gradient2: '#67F6D4',
    name: 'ServeRobotics',
    category: ''
  },
  {
    gradient1: '#FFD600',
    gradient2: '#FF6B00',
    name: 'OpenPipeAI',
    category: ''
  },
  {
    gradient1: '#AC792E',
    gradient2: '#F56B08',
    name: 'ApolloCurrency',
    category: ''
  },
{
  gradient1: '#0DF024 ',
  gradient2: '#10E5D9',
  name: 'SimpleHashInc',
  category: ''
}
];

const Feed = () => {
  return (
    <div className="feed">
       <Typography variant="h3" sx={{ color: "#fff", paddingLeft: 45}}><b>                 𝕏plore Startups</b></Typography>
      {boxData.map((box, index) => (
        <BoxComponent
          key={index}
          gradient1={box.gradient1}
          gradient2={box.gradient2}
          name={box.name}
          category={box.category}
        />
      ))}
    </div>
  );
};

export default Feed;
