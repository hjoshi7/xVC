import React, { useEffect, useRef } from 'react';

const TweetEmbed = ({ tweetId }) => {
  const tweetRef = useRef(null);

  useEffect(() => {
    console.log(`Attempting to embed tweet ID: ${tweetId}`);
  
    const embedTweet = () => {
      if (window.twttr && tweetRef.current && !tweetRef.current.hasChildNodes()) {
        console.log(`Embedding tweet ID: ${tweetId}`);
        window.twttr.widgets.createTweet(
          tweetId,
          tweetRef.current,
          {
            theme: 'dark'
          }
        );
      }
    };
  
    embedTweet();
  
    return () => {
     
    };
  }, [tweetId]);

  return <div ref={tweetRef} />;
};

export default TweetEmbed;
