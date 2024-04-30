import React, { useState, useEffect } from 'react';
import './css/InputDisplay.css';
import data from './data/dummyData.json';
import respData from './data/respData.json';
import { useLocation } from 'react-router-dom';

function InputDisplay() {
  const location = useLocation();

  const [selectedArtist, setSelectedArtist] = useState('');
  const [artistName, setArtistName] = useState('');
  const [artistPopularity, setArtistPopularity] = useState('');
  const [artistUrl, setArtistUrl] = useState('');
  const [loading, setLoading] = useState(false);

  const handleClick = () => {
    setLoading(true);
    const artist = data.artists.find(artist => artist.name.toLowerCase() === selectedArtist.toLowerCase());
    // fetch('http://127.0.0.1:5000/submit', {
    //   method: 'POST',
    //   headers: {
    //     'Content-Type': 'application/json'
    //   },
    //   body: JSON.stringify({"artist": artist.name})
    // })
    //   .then(response => response.json())
    //   .then(data => {
    //     setArtistName(data["artist_name"]);
    //     setArtistPopularity(data["artist_popularity"]);
    //     setArtistUrl(data["artist_url"]);
    //     setLoading(false);
      setTimeout(() => {
        const newData = respData[artist.name]
        setArtistName(newData.artist_name);
        setArtistPopularity(newData.artist_popularity);
        setArtistUrl(newData.artist_url);
        setLoading(false);
      }, 1000);
      // })
      // .catch(error => {
      //   console.error('Error posting data:', error);
      //   setLoading(false);
      // });
  };

  useEffect(() => {
    if (location.hash.includes('access_token')) {
      // If access_token is found, call the login function
      // You'll need to replace this with your actual login function
      handleLogin();
    }
  }, [location]);


  const handleLogin= () => {
    window.location.href = 'https://13.59.32.217/login';
    // window.location.href = 'http://127.0.0.1:5000/login';

    // if (window.location.hash.includes('access_token')) {
    //   // If so, call props.onLogin to display the Dashboard
    //   props.onLogin();
    // }
  }

  return (
    <div className="input-display">
      <select className="input-field" value={selectedArtist} onChange={e => setSelectedArtist(e.target.value)}>
        <option value="">Select an artist</option>
        {data.artists.map((artist, index) => (
          <option key={index} value={artist.name}>{artist.name}</option>
        ))}
      </select>
      <button className="display-button" onClick={handleClick}>Get Artist Info</button>
      {loading ? <div className="progress-bar"></div> : (
        <div>
          {artistName && <p className='display-text'>Artist Name : {artistName}</p>}
          {artistPopularity && <p className='display-text'>Artist Popularity : {artistPopularity}</p>}
          {artistUrl && <a href={artistUrl}>Spotify Profile</a>}
        </div>
      )}
      <button className="display-button" onClick={handleLogin}>Login with Spotify</button>
    </div>
  );
}

export default InputDisplay;