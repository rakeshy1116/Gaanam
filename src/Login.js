import React, { useState } from 'react';
import './css/Login.css'

function Login() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');

  const handleSubmit = event => {
    event.preventDefault();
    // Here you can handle the login logic
    console.log(`Logged in with username: ${username} and password: ${password}`);
  };

  return (
    <div className="login">
      <h2>Login</h2>
      <form onSubmit={handleSubmit} className="login-form">
        <label>
          Username:
          <input type="text" value={username} onChange={e => setUsername(e.target.value)} className="login-input" />
        </label>
        <label>
          Password:
          <input type="password" value={password} onChange={e => setPassword(e.target.value)} className="login-input" />
        </label>
        <input type="submit" value="Log In" className="login-submit" />
      </form>
    </div>
  );
}

export default Login;