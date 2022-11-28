import { loadImages } from '$lib/static/control/imageLoader';
import { postToJSON, getToJSON } from '$lib/static/fetcher';

// submitGuess send the given guess to the server, and the server responds back with the guess and its position in the correct words array. If the guess is not correct, we receive a position of -1.
const submitGuess = (
	guess: string
): Promise<{
	guess_index: number;
	guess: string;
}> => postToJSON('http://localhost:8080/guess', { guess });

// requestImages request the next set of images given your current correct guesses. It first reqeusts the sources of the images from the server, and then loads the images from those sources. It returs an array of image elements so you can render them right away.
const requestImages = (correctGuessesIndexes: number[]): Promise<HTMLImageElement[]> =>
	postToJSON('http://localhost:8080/images', { correct_guesses: correctGuessesIndexes }).then(
		loadImages
	);

const requestWordCount = (): Promise<number> =>
	getToJSON('http://localhost:8080/word_count').then((res) => res.count);

export default {
	submitGuess,
	requestImages,
	requestWordCount
};
