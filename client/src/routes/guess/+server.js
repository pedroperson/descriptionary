import { json } from '@sveltejs/kit';

/** @type {import('./$types').RequestHandler} */
export async function POST({ request }) {
	const { guess } = await request.json();
	const res = await fetch('http://localhost:8080/guess', {
		method: 'POST',
		body: JSON.stringify({ guess })
	})
		// .then((res) => res.json())
		.catch((err) => console.log('err', err));

	if (!res) {
		return json({ correct: false });
	}

	return json({ correct: res.status === 200 });
}
