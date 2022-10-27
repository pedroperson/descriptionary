import { writable, type Updater } from 'svelte/store';
import { newLocalStorageLayer } from './localStorage';

// Use the local store so that we can retain state even if the user refreshes the page
const localStore = newLocalStorageLayer('score', 0);

export const SCORE = ScoreKeeper();

function ScoreKeeper() {
	const { subscribe, set, update } = writable(localStore.read());

	// Update the store and save the current value in the local store
	const updateAndSave = (mod: Updater<any>) =>
		update((n) => {
			const newVal = mod(n);
			localStore.write(newVal);
			return newVal;
		});

	return {
		subscribe,
		correctGuess: () => updateAndSave((n) => n + 10),
		wrongGuess: () => updateAndSave((n) => n - 1),
		repeatedGuess: () => updateAndSave((n) => n - 2),
		reset: () => {
			set(0);
			localStore.write(0);
		}
	};
}
