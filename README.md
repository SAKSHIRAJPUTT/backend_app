# Full-Stack Web Application

This is a full-stack web application with a Node.js backend and a React frontend. The backend uses Express and MongoDB, while the frontend uses React and charts to display user data.

## Features

- **User Registration**: Users can register through a simple form.
- **Data Visualization**: Displays user activity over time using charts.
- **API Integration**: React fetches data from the Express API.

## Getting Started

### Prerequisites

- Node.js (https://nodejs.org/)
- MongoDB (locally or using MongoDB Atlas)

### Setup Instructions

1. Clone the repository:
   git clone https://github.com/SAKSHIRAJPUTT/backend_app.git
   cd C:\Users\rajpu\backend_app

2. Set up the backend:

  Navigate to the backend folder:  cd backend
   Install dependencies:   npm install

Create a .env file with your environment variables:
MONGODB_URI=mongodb://localhost:27017/your-db-name
PORT=5000

Start the backend server:  npm start

3. Set up the frontend:

Navigate to the frontend folder:  cd frontend

Install dependencies:  npm install

Create a .env file with the following variable: 
REACT_APP_API_URL=http://localhost:5000/api
Start the frontend server: npm start

Visit http://localhost:3000 in your browser to see the app in action.

