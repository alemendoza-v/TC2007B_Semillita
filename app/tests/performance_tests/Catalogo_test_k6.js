// k6 run --duration 3s --vus 10 Catalogo_test_k6.js

import http from 'k6/http';
import { check, sleep } from 'k6';

export let options = { maxRedirects: 4 };

// Common things
const API_URL_TOKEN = 'https://tc2007b-semillita.herokuapp.com/api/token/';
const API_URL_TEST = 'https://tc2007b-semillita.herokuapp.com/api/plantas/';

export function setup() {
	const body = {
		username: 'equipo',
		password: 'semillita1738',
	};

	const token_response = http.post(`${API_URL_TOKEN}`, body);
	const t = token_response.json('access');
	console.log(t);
	return t;
}

// Test scenario
export default function (t) {
	// Common requests params
	const params = {
		headers: {
			'Content-Type': 'application/json',
			Authorization: `Bearer ${t}`,
		},
	};

	// Scan QR
	let response = http.get(`${API_URL_TEST}`, params);
	check(response, {
		'Catalogo response status code is 200': (r) => r.status == 200,
	});

	// Short break between iterations
	sleep(0.5);
}
