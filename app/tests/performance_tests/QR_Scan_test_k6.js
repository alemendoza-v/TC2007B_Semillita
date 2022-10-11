// k6 run --duration 3s --vus 10 QR_Scan_test_k6.js

import http from 'k6/http';
import { check, sleep } from 'k6';

export let options = { maxRedirects: 4 };

// Common things
const API_URL = 'https://tc2007b-semillita.herokuapp.com/plantas/';

// Test scenario
export default function () {
	// Common requests params
	const params = { headers: { 'Content-Type': 'application/json' } };

	// Random planta_id value
	let randomInt = Math.floor(Math.random() * (135 - 132) + 132);

	// Scan QR
	let response = http.get(`${API_URL}${randomInt}`, params);
	check(response, {
		'QR response status code is 200': (r) => r.status == 200,
	});

	// Short break between iterations
	sleep(0.5);
}
