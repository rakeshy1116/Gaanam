import React, { useState } from 'react';
import './css/Signup.css'; // Import the CSS file

function Signup() {
  const [emailId, setEmailId] = useState('');
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [clientId, setClientId] = useState('');
  const [clientSecret, setClientSecret] = useState('');

  const handleSubmit = event => {
    event.preventDefault();
    // Here you can handle the signup logic
    console.log(`Signed up with emailId: ${emailId}, username: ${username}, password: ${password}, clientId: ${clientId}, and clientSecret: ${clientSecret}`);
  };

  return (
    <div className="signup">
      <h2>Sign Up</h2>
      <form onSubmit={handleSubmit} className="signup-form">
        <label>
          Email ID:
          <input type="email" placeholder='name@domain.com' value={emailId} onChange={e => setEmailId(e.target.value)} className="signup-input" />
        </label>
        <label>
          Username:
          <input type="text" placeholder='Username' value={username} onChange={e => setUsername(e.target.value)} className="signup-input" />
        </label>
        <label>
          Password:
          <input type="password" placeholder='Password' value={password} onChange={e => setPassword(e.target.value)} className="signup-input" />
        </label>
        <label>
          Client ID:
          <input type="text" placeholder='Enter your client id' value={clientId} onChange={e => setClientId(e.target.value)} className="signup-input" />
        </label>
        <label>
          Client Secret:
          <input type="password" placeholder='Enter your client secret' value={clientSecret} onChange={e => setClientSecret(e.target.value)} className="signup-input" />
        </label>
        <input type="submit" value="Sign Up" className="signup-submit" />
      </form>
    </div>
  );
}

export default Signup;