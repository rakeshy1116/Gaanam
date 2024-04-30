// // import React, { useEffect, useState } from 'react';

// // const Dashboard = () => {
// //   const [playlists, setPlaylists] = useState([]);
// //   const [topSong, setTopSong] = useState({});
// //   const [topArtist, setTopArtist] = useState({});
// //   const [topGenres, setTopGenres] = useState([]);
// //   const [totalMinutes, setTotalMinutes] = useState(0);

// //   useEffect(() => {
// //     // fetch('http://127.0.0.1:5000/playlists')
// //     //   .then(response => response.json())
// //     //   .then(data => setPlaylists(data))
// //     //   .catch(error => console.error('Error:', error));

// //     fetch('http://127.0.0.1:5000/topSong')
// //       .then(response => response.json())
// //       .then(data => {
// //             console.log(data)
// //             setTopSong(data)
// //         })
// //       .catch(error => console.error('Error:', error));

// //     // fetch('http://127.0.0.1:5000/topArtist')
// //     //   .then(response => response.json())
// //     //   .then(data => setTopArtist(data))
// //     //   .catch(error => console.error('Error:', error));

// //     // fetch('http://127.0.0.1:5000/topGenres')
// //     //   .then(response => response.json())
// //     //   .then(data => setTopGenres(data))
// //     //   .catch(error => console.error('Error:', error));

// //     // fetch('http://127.0.0.1:5000/totalMinutes')
// //     //   .then(response => response.json())
// //     //   .then(data => setTotalMinutes(data))
// //     //   .catch(error => console.error('Error:', error));
// //   }, []);

// //   return (
// //     <div className="dashboard">
// //       <div className="box">Playlists: {JSON.stringify(playlists)}</div>
// //       <div className="box">Top Song: {JSON.stringify(topSong)}</div>
// //       <div className="box">Top Artist: {JSON.stringify(topArtist)}</div>
// //       <div className="box">Top Genres: {JSON.stringify(topGenres)}</div>
// //       <div className="box">Total Minutes: {totalMinutes}</div>
// //     </div>
// //   );
// // };

// // export default Dashboard;

// import React, { useState } from 'react';
// import './Dashboard.css';

// const Dashboard = () => {
//   const [songData, setSongData] = useState(null);

//   const handleClick = () => {
//     console.log("clicked")
//     fetch('http://127.0.0.1:5000/topSong')
//       .then(response => response.json())
//       .then(data => setSongData(data))
//       .catch(error => console.error('Error:', error));
//   };

// //   return (
// //     <div>
// //         <nav>
// //          <button onClick={handleClick}>Get Top Songs</button>
// //        </nav>
// //         {songData && <div>{songData}</div>}
// //     </div>
// //   )

//   return (
//     <div className="dashboard">
//     <nav>
//         <button onClick={handleClick}>Get Top Songs</button>
//     </nav>
//      {/* {songData && <div>{songData}</div>} */}
//       {songData && (
//         <table>
//           <thead>
//             <tr>
//               <th>Image</th>
//               <th>Song Name</th>
//               <th>Artist</th>
//               <th>Preview</th>
//               <th>ID</th>
//             </tr>
//           </thead>
//           <tbody>
//             {songData.map((song, index) => (
//               <tr key={index}>
//                 <td><img className="song-image" src={song.image} alt={song.name} /></td>
//                 <td>{song.name}</td>
//                 <td>{song.artist}</td>
//                 <td>
//                   <audio controls>
//                     <source src={song.preview} type="audio/mpeg" />
//                     Your browser does not support the audio element.
//                   </audio>
//                 </td>
//                 <td>{song.id}</td>
//               </tr>
//             ))}
//           </tbody>
//         </table>
//       )}
//     </div>
//   );
// };

// export default Dashboard;

// import React, { useState } from 'react';
// import GetTopSong from './GetTopSong';
// import GetTopArtist from './GetTopArtist';
// import './Dashboard.css';
// import { Navigate } from 'react-router-dom';

// const Dashboard = ({ isLoggedIn }) => {
//   if (!isLoggedIn) {
//     return <Navigate to="/" />;
//   }

//   // Your Dashboard code here
// // const Dashboard = () => {
// //   const [showTopSongs, setShowTopSongs] = useState(false);
// //   const [showTopArtist, setShowTopArtist] = useState(false);
// const [displayComponent, setDisplayComponent] = useState('');


//   const handleSongsClick = () => {

//     setDisplayComponent("songs");
//   };

//   const handleArtistClick = () => {

//     setDisplayComponent("artists");
//   };

//   return (
//     <div className="dashboard">
//       <nav>
//         <button onClick={handleSongsClick}>Get Top Songs</button>
//         <button onClick={handleArtistClick}>Get Top Artist</button>
//       </nav>
//       {displayComponent === "songs" && <GetTopSong />}
//       {displayComponent === "artists" && <GetTopArtist />}
//     </div>
//   );
// };

// export default Dashboard;

import React, { useState } from 'react';
import GetTopSong from './GetTopSong';
import GetTopArtist from './GetTopArtist';
import { Navigate } from 'react-router-dom';
import './Dashboard.css';

const Dashboard = () => {
  // console.log("I am in dashboard")
  const queryString = window.location.search;
  const urlParams = new URLSearchParams(queryString);
  const paramValue = urlParams.get('user_id'); // "value"

  // Store 'user_id' and 'expiration' in the session
  sessionStorage.setItem('user_id', paramValue);

  const [isLoggedIn, setIsLoggedIn] = useState(true); // Add this line
  const [displayComponent, setDisplayComponent] = useState('');
  const [showOptions, setShowOptions] = useState(false);
  const [selectedOption, setSelectedOption] = useState('');
  // Remove the duplicate declaration of 'setDisplayNavSongs'
  const [displayNavSongs, setDisplayNavSongs] = useState(false);
  const [displayNavArtist, setDisplayNavArtist] = useState(false);
  const [displayRecommendation, setDisplayRecommendation] = useState(false);


  // Update this function to set isLoggedIn to true when the user logs in
  const handleLogin = () => {
    setIsLoggedIn(true);
  };

  // const handleSongsClick = () => {
  //   setDisplayComponent("songs");
  //   setSelectedOption('songs');
  //   setShowOptions(true);
  // };
  const handleArtistClick = () => {
    console.log(sessionStorage.getItem('user_id'));
    setDisplayNavSongs(false);
    setDisplayNavArtist(true);
    setDisplayRecommendation(false);
    setDisplayComponent(`artists`);
    setSelectedOption(`artists`);
  };

  const handleGetRecommendations = () => {
    console.log(sessionStorage.getItem('user_id'));
    setDisplayNavSongs(false);
    setDisplayNavArtist(false);
    setDisplayRecommendation(true);
    setDisplayComponent(`artists`);
    setSelectedOption(`artists`);
  };

  


  const handleSongsClick = (option) => {
    setDisplayNavSongs(true);
    setDisplayNavArtist(false);
    setDisplayRecommendation(false);
    setDisplayComponent(`songs`);
    setSelectedOption(`songs`);
    setShowOptions(true);
  };
  const handleArtistClick_4 = (option) => {
    setDisplayNavSongs(false);
    setDisplayNavArtist(true);
    setDisplayRecommendation(false);
    setDisplayComponent(`artists_4`);
    setSelectedOption(`artists_4`);
  };
  const handleSongsClick_4 = (option) => {
    setDisplayNavSongs(true);
    setDisplayNavArtist(false);
    setDisplayRecommendation(false);
    setDisplayComponent(`songs_4`);
    setSelectedOption(`songs_4`);
    setShowOptions(true);
  };
  const handleArtistClick_6 = (option) => {
    setDisplayNavSongs(false);
    setDisplayNavArtist(true);
    setDisplayRecommendation(false);
    setDisplayComponent(`artists_6`);
    setSelectedOption(`artists_6`);
  };
  const handleSongsClick_6 = (option) => {
    setDisplayNavSongs(true);
    setDisplayNavArtist(false);
    setDisplayRecommendation(false);
    setDisplayComponent(`songs_6`);
    setSelectedOption(`songs_6`);
    setShowOptions(true);
  };
  const handleArtistClick_12 = (option) => {
    setDisplayNavSongs(false);
    setDisplayNavArtist(true);
    setDisplayRecommendation(false);
    setDisplayComponent(`artists_12`);
    setSelectedOption(`artists_12`);
  };
  const handleSongsClick_12 = (option) => {
    setDisplayNavSongs(true);
    setDisplayNavArtist(false);
    setDisplayRecommendation(false);
    setDisplayComponent(`songs_12`);
    setSelectedOption(`songs_12`);
    setShowOptions(true);
  };

  const handleGetRecommendations_4 = (option) => {
    setDisplayNavSongs(false);
    setDisplayNavArtist(false);
    setDisplayRecommendation(true);
    setDisplayComponent(`recommendations_4`);
    setSelectedOption(`recommendations_4`);
    setShowOptions(true);
  };

  const handleGetRecommendations_6 = (option) => {
    setDisplayNavSongs(false);
    setDisplayNavArtist(false);
    setDisplayRecommendation(true);
    setDisplayComponent(`recommendations_6`);
    setSelectedOption(`recommendations_6`);
    setShowOptions(true);
  };
  const handleGetRecommendations_12 = (option) => {
    setDisplayNavSongs(false);
    setDisplayNavArtist(false);
    setDisplayRecommendation(true);
    setDisplayComponent(`recommendations_12`);
    setSelectedOption(`recommendations_12`);
    setShowOptions(true);
  };

  const handleCreatePlaylist = () => {
    setDisplayNavSongs(false);
    setDisplayNavArtist(false);
    fetch('http://127.0.0.1:5000/createPlaylist', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        user_id: 'your_user_id',
        playlist_name: 'new_playlist_name',
        playlist_description: 'your_playlist_description',
        playlist_public: true,
      }),
    })
    .then(response => response.json())
    .then(data => console.log(data))
    .catch((error) => {
      console.error('Error:', error);
    });
  };

  const handleAddTracks = () => {
    setDisplayNavSongs(false);
    setDisplayNavArtist(false);
    fetch('http://127.0.0.1:5000/addTracks', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        playlist_id: '32SR2YzI56EFpKwHLHgjLU',
        tracks: ['spotify:track:4O2DJnDHV46KfRZsOxrQzO'] // replace with actual track ids
      }),
    })
    .then(response => response.json())
    .then(data => console.log(data))
    .catch((error) => {
      console.error('Error:', error);
    });
  };

  // const handleGetRecommendations = () => {
  //   setDisplayNavSongs(true);
  //   fetch('http://127.0.0.1:5000/recommendations/short_term', {
  //     method: 'GET',
  //     headers: {
  //       'Content-Type': 'application/json',
  //     },
  //   })
  //   .then(response => response.json())
  //   .then(data => console.log(data))
  //   .catch((error) => {
  //     console.error('Error:', error);
  //   });
  // };
  
  
  
  // If the user is not logged in, redirect them to the login page
  if (!isLoggedIn) {
    return <Navigate to="/" />;
  }

  return (
    <div className='dashboard'>
      <nav>
        <button onClick={handleSongsClick}>Show Top Songs</button>
        <button onClick={handleArtistClick}>Show Top Artists</button>
        {/* <button onClick={handleCreatePlaylist}>Top Genres</button>
        <button onClick={handleAddTracks}>Add Tracks to Playlist</button> */}
        <button onClick={handleGetRecommendations}>Get Recommendations</button>
      </nav>

      {displayNavSongs && (
        <div>
          <nav>
            <button onClick={handleSongsClick_4}>Last 4 weeks</button>
            <button onClick={handleSongsClick_6}> Last 6 months</button>
            <button onClick={handleSongsClick_12}>Last 12 months</button>
          </nav>
          
        </div>
      )}
      {displayNavArtist && (
        <div>
          <nav>
            <button onClick={handleArtistClick_4}>Last 4 weeks</button>
            <button onClick={handleArtistClick_6}>Last 6 months</button>
            <button onClick={handleArtistClick_12}>Last 12 months</button>
          </nav>
        </div>
      )}
      {displayRecommendation && (
        <div>
          <nav>
            <button onClick={handleGetRecommendations_4}>Last 4 weeks</button>
            <button onClick={handleGetRecommendations_6}>Last 6 months</button>
            <button onClick={handleGetRecommendations_12}>Last 12 months</button>
          </nav>
        </div>
      )}

      {/* {displayComponent === 'songs' && <GetTopSong url = "http://127.0.0.1:5000/topSong/short_term" />}
      {displayComponent === 'songs_4' && <GetTopSong url={`http://127.0.0.1:5000/topSong/short_term/${sessionStorage.getItem('user_id')}`} />}
      {displayComponent === 'songs_6' && <GetTopSong url = {`http://127.0.0.1:5000/topSong/medium_term/${sessionStorage.getItem('user_id')}`}/>}
      {displayComponent === 'songs_12' && <GetTopSong  url = {`http://127.0.0.1:5000/topSong/long_term/${sessionStorage.getItem('user_id')}`}/>} */}

      {/* {displayComponent === 'artists' && <GetTopArtist  url = "http://127.0.0.1:5000/topArtist/short_term"/>} */}
      {/* {displayComponent === 'artists_4' && <GetTopArtist  url = {`http://127.0.0.1:5000/topArtist/short_term/${sessionStorage.getItem('user_id')}`}/>}
      {displayComponent === 'artists_6' && <GetTopArtist  url = {`http://127.0.0.1:5000/topArtist/medium_term/${sessionStorage.getItem('user_id')}`}/>}
      {displayComponent === 'artists_12' && <GetTopArtist  url = {`http://127.0.0.1:5000/topArtist/long_term/${sessionStorage.getItem('user_id')}`}/>} */}

      {/* {displayComponent === 'recommendations_4' && <GetTopSong  url = {`http://127.0.0.1:5000/recommendations/short_term/${sessionStorage.getItem('user_id')}`}/>}
      {displayComponent === 'recommendations_6' && <GetTopSong  url = {`http://127.0.0.1:5000/recommendations/medium_term/${sessionStorage.getItem('user_id')}`}/>}
      {displayComponent === 'recommendations_12' && <GetTopSong  url = {`http://127.0.0.1:5000/recommendations/long_term/${sessionStorage.getItem('user_id')}`}/>}
       */}
      {/* {displayComponent === 'songs' && <GetTopSong url = "http://127.0.0.1:5000/topSong/short_term" />} */}
      {displayComponent === 'songs_4' && <GetTopSong url={`https://13.59.32.217/topSong/short_term/${sessionStorage.getItem('user_id')}`} />}
      {displayComponent === 'songs_6' && <GetTopSong url = {`https://13.59.32.217/topSong/medium_term/${sessionStorage.getItem('user_id')}`}/>}
      {displayComponent === 'songs_12' && <GetTopSong  url = {`https://13.59.32.217/topSong/long_term/${sessionStorage.getItem('user_id')}`}/>}

      {/* {displayComponent === 'artists' && <GetTopArtist  url = "http://127.0.0.1:5000/topArtist/short_term"/>} */}
      {displayComponent === 'artists_4' && <GetTopArtist  url = {`https://13.59.32.217/topArtist/short_term/${sessionStorage.getItem('user_id')}`}/>}
      {displayComponent === 'artists_6' && <GetTopArtist  url = {`https://13.59.32.217/topArtist/medium_term/${sessionStorage.getItem('user_id')}`}/>}
      {displayComponent === 'artists_12' && <GetTopArtist  url = {`https://13.59.32.217/topArtist/long_term/${sessionStorage.getItem('user_id')}`}/>}

      {displayComponent === 'recommendations_4' && <GetTopSong  url = {`https://13.59.32.217/recommendations/short_term/${sessionStorage.getItem('user_id')}`}/>}
      {displayComponent === 'recommendations_6' && <GetTopSong  url = {`https://13.59.32.217/recommendations/medium_term/${sessionStorage.getItem('user_id')}`}/>}
      {displayComponent === 'recommendations_12' && <GetTopSong  url = {`https://13.59.32.217/recommendations/long_term/${sessionStorage.getItem('user_id')}`}/>}

    
    </div>
  );
};

export default Dashboard;


// import React from 'react';
// import { BrowserRouter as Router, Route, Routes, Link } from 'react-router-dom';
// import TopSongs from './GetTopSong';  // Import your TopSongs component
// import TopArtists from './GetTopArtist';  // Import your TopArtists component

// function Dashboard() {
//   return (
//     <Router>
//       <Routes>
//       <div>
//         <nav>
//           <ul>
//             <li>
//               <Link to="/topSongs">Show Top Songs</Link>
//             </li>
//             <li>
//               <Link to="/topArtists">Show Top Artists</Link>
//             </li>
//           </ul>
//         </nav>

//         <Route path="/topSongs" component={TopSongs} />
//         <Route path="/topArtists" component={TopArtists} />
//       </div>
//       </Routes>
//     </Router>
//   );
// }

// export default Dashboard;