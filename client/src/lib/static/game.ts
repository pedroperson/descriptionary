import { post } from '../static/fetcher';
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
export const correctGuesses = writable<string[]>(localStore.read());
const appendCorrectGuess = (guess: string) => {
	correctGuesses.update((it) => [...it, guess]);
	localStore.write(get(correctGuesses));
};

export const submitGuess = async (guess: string): Promise<Message> => {
	if (gameIsOver()) return 'The game is already over';

	return validate(guess)
		.then(() => post('/guess', { guess: guess }))
		.then(({ correct }) => (correct ? handleCorrectGuess(guess) : handleWrongGuess(guess)))
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

const handleCorrectGuess = (guess: string): Message => {
	SCORE.correctGuess();

	appendCorrectGuess(guess);

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
