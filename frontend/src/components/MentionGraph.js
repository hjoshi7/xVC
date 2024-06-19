import React from 'react';
import Plot from 'react-plotly.js';


const MentionGraph = ({ data}) => {

  const widgetStyle = {
    borderRadius: '20px', // Sets rounded corners
    background: 'linear-gradient(to right, #6a3093, #a044ff)', // Purple gradient fill
    padding: '100px', // Optional padding to give space inside the borders
    color: '#fff', // Ensures text is visible on the purple background
    boxShadow: '0 4px 8px rgba(0, 0, 0, 0.1)' // Optional shadow for 3D effect
  };

  
  return (
    
    <div color={widgetStyle}>
    <Plot
      data={[
        {
          
          x: data.x,
          y: data.y,
          type: 'scatter',
          mode: 'lines',
          marker: { color: '#50b7f5' },
          line: { shape: 'spline' , 'width': 3} // This makes the line smooth

        }
      ]}
      
      layout={{
        width: 720,
        height: 440,
        margin: { t: 40, b: 40, l: 40, r: 40 },
        title: '𝕏 Popularity',
        xaxis: {
          title: 'Tweet Dates',
          showgrid: false,
          type: 'date'
        },
        yaxis: {
          title: 'Cumulative Number of Mentions',
          showgrid: false,
          // showticklabels: false

        },
        font: {
          color: "#fff"
        },
        paper_bgcolor: "rgba(0, 0, 0, 0)",
        plot_bgcolor: "rgba(0, 0, 0, 0)"
      }}
    />
    </div>
  );
};

export default MentionGraph;