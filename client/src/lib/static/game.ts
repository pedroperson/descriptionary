import { post, GET } from '../static/fetcher';
import previousAttempts from '../static/attempts';
import { SCORE } from '../static/points';
import { writable, get } from 'svelte/store';
import { newLocalStorageLayer } from './localStorage';

type Message = string;

// Number of words the user has to guess before winning the game
const wordCount = 4;

// Use the local store so that we can retain state even if the user refreshes the page
const localStore = newLocalStorageLayer('correctGuesses', []);

// Keep track of the correct guesses to keep track of progress and show them in the UI
export type CorrectGuess = { guess: string; index: number };
export const correctGuesses = writable<CorrectGuess[]>(localStore.read());

const appendCorrectGuess = (guess: string, index: number) => {
	correctGuesses.update((it) => [...it, { guess, index }]);
	localStore.write(get(correctGuesses));
};

export const submitGuess = async (guess: string): Promise<Message> => {
	if (gameIsOver()) return 'The game is already over';

	return validate(guess)
		.then(() => post('http://localhost:8080/guess', { guess: guess }))
		.then((res: string) => {
			const index = parseInt(res, 10);
			return index > -1 ? handleCorrectGuess(guess, index) : handleWrongGuess(guess);
		})
		.catch((err): Message => err.message);
};

const validate = async (guess: string) => {
	// Don't let user try the same prompt more than once to save redundant server calls
	if (previousAttempts.hasAttempted(guess)) {
		SCORE.repeatedGuess();
		throw new Error(`You've already guessed "${guess}"`);
	}

	previousAttempts.saveAttempt(guess);
};

const handleCorrectGuess = (guess: string, index: number): Message => {
	SCORE.correctGuess();

	appendCorrectGuess(guess, index);

	if (!gameIsOver()) return 'Correct guess!';
	return 'You won the game!!';
};

const handleWrongGuess = (guess: string): Message => {
	SCORE.wrongGuess();
	return `"${guess}" was a bad guess`;
};

const gameIsOver = () => get(correctGuesses).length === wordCount;

export const reset = () => {
	SCORE.reset();
	correctGuesses.set([]);
	localStore.write(get(correctGuesses));
	previousAttempts.reset();
};

export const todaysSentence = async (): Promise<string> => {
	return GET('http://localhost:8080/sentence').then((res: string) => res);
};
