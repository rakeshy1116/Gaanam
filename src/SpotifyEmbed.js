import React from 'react';

const SpotifyEmbed = () => {
  return (
    <iframe
      title="Spotify Embed: Recommendation Playlist"
      src="https://open.spotify.com/embed/playlist/44cIfSbwr3HvbAxYCRNWFx?utm_source=generator&amp;theme=0"
      width="100%"
      height="100%"
      style={{ minHeight: '360px' }}
      frameBorder="0"
      allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture"
      loading="lazy"
    ></iframe>
  );
};

export default SpotifyEmbed;