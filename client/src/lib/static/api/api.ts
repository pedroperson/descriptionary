import { loadImages } from '$lib/static/control/imageLoader';
import { postToJSON, getToJSON } from '$lib/static/fetcher';

export async function submitGuess(guess: string): Promise<{
	guess_index: number;
	guess: string;
}> {
	const res = await postToJSON('http://localhost:8080/guess', { guess });

	const { guess_index, guess: submittedGuess } = res;

	console.log('guess_index,', guess_index, typeof guess_index);
	console.log('submittedGuess,', submittedGuess, typeof submittedGuess);
	return res;
}
