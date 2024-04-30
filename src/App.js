import InputDisplay from './InputDisplay';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import React, { useState } from 'react';
import Dashboard from './Dashboard';
import SpotifyEmbed from './SpotifyEmbed';
// import Login from './Login';
// import Signup from './Signup';
import './css/welcome.css';

import './App.css';

function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);

  const handleLogin = () => {
    setIsLoggedIn(true);
  };

  return (
    <div className="App">
      <h1 className="welcome-text">Welcome to Gaanam!!</h1>
      <Router>
        <Routes>
        <Route path="/dashboard" element={<Dashboard isLoggedIn={isLoggedIn} />} />
        <Route path="/" element={<InputDisplay onLogin={handleLogin} />} />
          {/* <Route path="/dashboard">
            {isLoggedIn ?  (<><Dashboard /><SpotifyEmbed /></> ): <InputDisplay />}
          </Route>
          <Route path="/" exact>
            <InputDisplay onLogin={handleLogin} />
          </Route> */}
      </Routes>
    </Router>
      {/* <InputDisplay /> */}
      {/* <InputDisplay /> */}
      {/* {isLoggedIn ? (<><Dashboard /><SpotifyEmbed /></> ): <InputDisplay onLogin={handleLogin} />}
      <Dashboard /> */}
      {/* <Login /> */}
      {/* <Signup/> */}
      
    </div>
  );
}

// export default App;

// import React from 'react';
// import Login from './Login';
// import Signup from './Signup';
// import './App.css';

// function App() {
//   return (
//     <div className="App">
//       <h1 className="welcome-text">Welcome to Gaanam!!</h1>
//       <div className="auth-container">
//       <Signup />

//         <div className="separator">|</div>
        
//         <Login />
//       </div>
//     </div>
//   );
// }

// export default App;

// import React from 'react';
// import Login from './Login';
// import Signup from './Signup';
// import './App.css';

// function App() {
//   return (
//     <div className="App">
//       <h1 className="welcome-text">Welcome to Gaanam!!</h1>
//       <div className="auth-container">
//         <Signup />
//         <div className="separator">|</div>
//         <Login />
//       </div>
//     </div>
//   );
// }

export default App;
