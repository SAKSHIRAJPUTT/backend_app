import React from 'react';
import './App.css';  // Importing styles for the app
import UserDataChart from './UserDataChart';  // Import the chart component
import Register from './components/Register'; // Import the Register component

const App = () => {
  return (
    <div className="App">
      <h1>Welcome to the Data Analysis Dashboard</h1>
      
      <UserDataChart />  {/* Include the User Data Chart component */}

      <h2>Registration Page</h2>
      <Register />  {/* Include the Register form component */}
    </div>
  );
};

export default App;
