import React, { useState } from "react";
import './Register.css'; // You can define the styles here

function Register() {
  const [email, setEmail] = useState("");
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  const handleSubmit = async (event) => {
    event.preventDefault();
    
    // Simulating a registration attempt
    try {
      if (!email || !username || !password) {
        setError("Please fill in all fields.");
        return;
      }

      // Call your API here to submit registration data (e.g., POST to your backend)
      // const response = await api.register(email, username, password);
      console.log("User Registered:", { email, username, password });
      setError(""); // Clear any previous errors
      alert("Registration successful!");
    } catch (err) {
      setError("An error occurred, please try again.");
    }
  };

  return (
    <div className="register-container">
      <h1>Registration Page</h1>
      <form onSubmit={handleSubmit} className="register-form">
        <label htmlFor="email">Email</label>
        <input
          type="email"
          id="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          placeholder="Enter your email"
        />

        <label htmlFor="username">Username</label>
        <input
          type="text"
          id="username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          placeholder="Choose a username"
        />

        <label htmlFor="password">Password</label>
        <input
          type="password"
          id="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          placeholder="Enter your password"
        />

        {error && <p className="error-message">{error}</p>}

        <button type="submit" className="register-button">Register</button>
      </form>
    </div>
  );
}

export default Register;
