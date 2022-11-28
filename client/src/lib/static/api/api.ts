import { loadImages } from '$lib/static/control/imageLoader';
import { postToJSON, getToJSON } from '$lib/static/fetcher';

// submitGuess send the given guess to the server, and the server responds back with the guess and its position in the correct words array. If the guess is not correct, we receive a position of -1.
export const submitGuess = (
	guess: string
): Promise<{
	guess_index: number;
	guess: string;
}> => postToJSON('http://localhost:8080/guess', { guess });
