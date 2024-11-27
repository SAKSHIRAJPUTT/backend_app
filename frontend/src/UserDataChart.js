
import React, { useEffect, useState } from 'react';
import { Bar } from 'react-chartjs-2';  // Import Bar chart component from react-chartjs-2
import { Chart as ChartJS, CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend } from 'chart.js';
import React from 'react';
import { Line } from 'react-chartjs-2';

ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend);

const UserDataChart = () => {
    const [data, setData] = useState({});

    // Fetch data from the backend when the component mounts
    useEffect(() => {
        fetch('http://127.0.0.1:8000/data-analysis/')  // Assuming your backend runs on this endpoint
            .then(response => response.json())
            .then(data => {
                setData(data);
            });
    }, []);

    // Prepare the chart data in the format required by Chart.js
    const chartData = {
        labels: Object.keys(data.users_per_month || {}),
        datasets: [
            {
                label: 'Users per Month',
                data: Object.values(data.users_per_month || {}),
                backgroundColor: 'rgba(75, 192, 192, 0.6)',
            },
        ],
    };

    return (
        <div>
            <h2>User Data Analysis</h2>
            <Bar data={chartData} />  {/* Render the Bar chart */}
        </div>
    );
};

export default UserDataChart;
