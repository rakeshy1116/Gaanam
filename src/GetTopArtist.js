import React, { useState, useEffect } from 'react';
import './css/GetTopSong.css';
import './css/PlayButton.css';
import playButton from './images/spotify.png';

const GetTopArtist = ({url}) => {
  const [artistData, setArtistData] = useState(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    // fetch('https://13.59.32.217/topArtist')
    fetch(url)
      .then(response => response.json())
      .then(data => {setArtistData(data); setIsLoading(false);})
      .catch(error => {
        console.error('Error:', error);
        setIsLoading(false)
      });
  }, []);

  if (isLoading) {
    return <div className='spinner'></div>; // Replace this with your loading spinner
  }

  return (
    <div>
     
      {artistData && (
        <table>
          <thead>
            <tr>
              <th>Image</th>
              <th>Artist Name</th>
              <th>ID</th>
            </tr>
          </thead>
          <tbody>
            {artistData.map((artist, index) => (
              <tr key={index}>
                <td><img className="song-image" src={artist.image} alt={artist.name} /></td>
                <td>{artist.name}</td>
                <td><a href={`https://open.spotify.com/artist/${artist.id}`} target="_blank" rel="noopener noreferrer">
                        <img src={playButton} alt="Play" className='playButton'/>
                    </a>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
};

export default GetTopArtist;