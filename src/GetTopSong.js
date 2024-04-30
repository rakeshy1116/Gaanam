import React, { useState, useEffect } from 'react';
import playButton from './images/spotify.png';
import './css/GetTopSong.css';
import './css/PlayButton.css';

const GetTopSong = ({url}) => {
  const [songData, setSongData] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [selectedSongs, setSelectedSongs] = useState([]);

  useEffect(() => {
    // fetch('https://13.59.32.217/topSong')
    fetch(url)
      .then(response => response.json())
      .then(data => {setSongData(data);setIsLoading(false);})
      .catch(error => {console.error('Error:', error);setIsLoading(false);});
  }, []);

  if (isLoading) {
    return <div className='spinner'></div>; // Replace this with your loading spinner
  }

  const handleAlertClick = () => {
      // setDisplayNavSongs(false);
      // setDisplayNavArtist(false);
      // fetch(`http://127.0.0.1:5000/addTracks/${sessionStorage.getItem('user_id')}`, {
      fetch(`https://13.59.32.217/addTracks/${sessionStorage.getItem('user_id')}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          playlist_id: '32SR2YzI56EFpKwHLHgjLU',
          tracks: selectedSongs.join(',')
        }),
      })
      .then(response => response.json())
      .then(data => console.log(data))
      .catch((error) => {
        console.error('Error:', error);
      });
    };
  //   alert(`Selected songs: ${selectedSongs.join(', ')}`);
  // };
  

  return (
    <div>
    {/* <nav>
        <button onClick={handleClick}>Get Top Songs</button>
    </nav> */}
     
      {songData && (
        <table>
          <thead>
            <tr>
              <th> </th>
              <th data-testId="cypress-topSong-Image">Image</th>
              <th data-testId="cypress-topSong-SongName" >Song Name</th>
              <th data-testId="cypress-topSong-Artist">Artist</th>
              <th data-testId="cypress-topSong-Preview">Preview</th>
              <th data-testId="cypress-topSong-Play">Play</th>
            </tr>
          </thead>
          <tbody  data-testId="cypress-topSong-Table">
            {songData.map((song, index) => (
              <tr key={index}>
                <td>
                <button
                   data-testId="cypress-topSong-AddButton"
                   style={{
                    borderRadius: '50%', // makes the button circular
                    width: '30px', // sets a fixed width
                    height: '30px', // sets a fixed height
                    fontSize: '20px', // adjusts the font size
                    fontFamily: 'Arial, sans-serif', // sets the font
                    border: 'none', // removes the default button border
                    backgroundColor: '#4CAF50', // sets the background color
                    color: 'white', // sets the font color
                    cursor: 'pointer', // changes the cursor to a pointer when hovering over the button
                    display: 'flex', // uses flexbox for centering
                    alignItems: 'center', // centers vertically
                    justifyContent: 'center', // centers horizontally
                  }}
                    onClick={(e) => {
                      if (selectedSongs.includes(song.id)) {
                        setSelectedSongs((prev) => prev.filter((id) => id !== song.id));
                      } else {
                        setSelectedSongs((prev) => [...prev, song.id]);
                      }
                    }}
                  >
                    {selectedSongs.includes(song.id) ? '-' : '+'}
                </button>
                </td>
                <td><img className="song-image" src={song.image} alt={song.name} /></td>
                <td>{song.name}</td>
                <td>{song.artist}</td>
                <td>
                  <audio controls>
                    <source src={song.preview} type="audio/mpeg" />
                    Your browser does not support the audio element.
                  </audio>
                </td>
                <td><a href={`https://open.spotify.com/track/${song.id}`} target="_blank" rel="noopener noreferrer">
                        <img src={playButton} alt="Play" className='playButton'/>
                    </a>
                </td>
              </tr>
            ))}
          </tbody>
        </table>   
      )}
      <button data-testid="cypress-addplaylist-button"
        style={{
          padding: '10px 20px', // adjusts the size of the button
          fontSize: '16px', // adjusts the font size
          fontFamily: 'Arial, sans-serif', // sets the font
          border: 'none', // removes the default button border
          backgroundColor: '#4CAF50', // sets the background color
          color: 'white', // sets the font color
          cursor: 'pointer', // changes the cursor to a pointer when hovering over the button
          borderRadius: '5px', // rounds the corners of the button
          margin: '20px', // adds space above the button
        }}
        onClick={handleAlertClick}
      >
        Add Selected Songs
      </button>
    </div>
  );
};

export default GetTopSong;