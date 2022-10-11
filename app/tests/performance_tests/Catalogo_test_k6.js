// k6 run --duration 3s --vus 10 Catalogo_test_k6.js

import http from 'k6/http';
import { check, sleep } from 'k6';

export let options = { maxRedirects: 4 };

// Common things
const API_URL = 'https://tc2007b-semillita.herokuapp.com/api/plantas/';

let token = null;

// Test scenario
export default function () {
	if (__ITER === 0) {
		const body = {
			username: 'equipo',
			password: 'semillita1738',
		};

		const token_response = http.post(`${API_URL}/api/token/`, body);

		token = token_response.json('access');
	}

	// Common requests params
	const params = {
		headers: {
			'Content-Type': 'application/json',
			Authorization: `Bearer ${token}`,
		},
	};

	// Scan QR
	let response = http.get(`${API_URL}`, params);
	check(response, {
		'Catalogo response status code is 200': (r) => r.status == 200,
	});

	// Short break between iterations
	sleep(0.5);
}
