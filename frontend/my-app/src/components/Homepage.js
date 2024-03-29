import React, { useState } from 'react';
import DataTable from './DataTable';

function Homepage() {
    const [insurerId, setInsurerId] = useState(null);
	const [insurersData, setInsurersData] = useState(null);
	const [exercisesData, setExercisesData] = useState(null);

	const fetchInsurers = () => {
		fetch('http://localhost:8000/insurer')
		.then(response => response.json())
		.then(data => setInsurersData(data))
		.catch(error => console.error(error))
	};

	const fetchExercises = (insurerId) => {
		fetch(`http://localhost:8000/exercise/${insurerId}`)
		.then(response => response.json())
		.then(data => setExercisesData(data))
		.catch(error => console.server(error));
	};

    const handleInputChange = (event) => {
        setInsurerId(event.target.value);
    };

    const handleButtonClick = () => {
        fetchExercises(insurerId);
    };

	return (
		<div class="main">
			<h1 class="header">Welcome to the Homepage</h1>
			<button class="myButton" onClick={fetchInsurers}>Get Insurers</button>
            <input class="text-input" type="text" value={insurerId} onChange={handleInputChange} placeholder="Enter insurer ID" />
			<button class="myButton" onClick={handleButtonClick}>Get Exercises</button>
			{insurersData && (
				<div>
					<h2>Insurers Data:</h2>
					<pre>{JSON.stringify(insurersData, null, 2)}</pre>
				</div>
			)}
			{exercisesData && (
            	<div>
                	<h2>Exercises Data:</h2>
                	<DataTable class="data-table" data={exercisesData} />
            	</div>
            )}
		</div>
	);
}

export default Homepage;
