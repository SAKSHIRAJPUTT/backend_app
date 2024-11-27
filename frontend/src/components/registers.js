import React, { useState } from 'react';

const Register = () => {
    const [email, setEmail] = useState('');
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');

    const handleSubmit = async (e) => {
        e.preventDefault();
        
        // Simple validation before submitting the form
        if (!email || !username || !password) {
            setError("All fields are required.");
            return;
        }
        
        // You can add more validation for email or password if necessary, e.g., regex for email, password strength

        setError("");  // Reset error
        setLoading(true);  // Start loading
        
        try {
            // Replace this with your API endpoint for registration
            const response = await fetch('http://127.0.0.1:8000/register', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ email, username, password }),
            });

            const data = await response.json();

            if (response.ok) {
                // Handle success (e.g., redirect to login page or show a success message)
                console.log('User registered:', data);
            } else {
                // Handle server-side errors
                setError(data.detail || "Something went wrong!");
            }
        } catch (error) {
            // Handle network or other errors
            setError("An error occurred, please try again.");
        } finally {
            setLoading(false);  // End loading
        }
    };

    return (
        <div>
            <h2>Register</h2>
            {error && <p style={{ color: 'red' }}>{error}</p>}  {/* Display error message if any */}
            <form onSubmit={handleSubmit}>
                <input
                    type="email"
                    placeholder="Email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    required
                />
                <input
                    type="text"
                    placeholder="Username"
                    value={username}
                    onChange={(e) => setUsername(e.target.value)}
                    required
                />
                <input
                    type="password"
                    placeholder="Password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    required
                />
                <button type="submit" disabled={loading}>
                    {loading ? "Registering..." : "Register"}  {/* Change text while loading */}
                </button>
            </form>
        </div>
    );
};

export default Register;
