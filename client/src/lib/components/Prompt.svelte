<script lang="ts">
	import { post } from '../static/fetcher';
	import previousAttempts from '../static/attempts';

	// Number of words the user has to guess
	const wordCount = 4;

	// Current state of the user query
	let query = '';

	// Keep a reference to the state element so we can talk to the user through it
	let stateElem: Element;
	const tellUser = (msg: string) => (stateElem.innerHTML = msg);

	// Keep track of the correct guesses to keep track of progress and show them in the UI
	const correctGuesses: string[] = [];

	const gameIsOver = () => correctGuesses.length === wordCount;

	const submit = () => {
		console.log('submit!');
		const q = query;
		validate(q)
			.then(() => post('/guess', { guess: q }))
			.then(({ correct }) => {
				correct ? handleCorrectGuess(q) : handleWrongGuess(q);
			})
			.catch((err) => tellUser(err.message))
			.finally(() => {
				// Reset the query so the textbox is emptied and user can try again
				query = '';
			});
	};

	const validate = async (prompt: string) => {
		// Don't let user try the same prompt more than once to save redundant server calls
		if (previousAttempts.hasAttempted(prompt)) {
			throw new Error(`You've already guessed "${query}"`);
		}

		previousAttempts.newAttempt(prompt);
	};

	const handleCorrectGuess = (guess: string) => {
		tellUser('Correct guess!');

		correctGuesses.push(guess);
		if (gameIsOver()) {
			window.alert('You won the game!!');
		}
	};

	const handleWrongGuess = (guess: string) => {
		tellUser(`"${guess}" was a bad guess`);
	};
</script>

<div class="words-of-the-day">
	{#each correctGuesses as g, i (i)}
		<div class="word" class:filled={g}>
			{g}
		</div>
	{/each}
</div>

<form on:submit|preventDefault={submit}>
	<label for="promp-textbox">Write your guess, one word, five letters long</label>
	<input id="promp-textbox" type="text" placeholder="Denim..." bind:value={query} />

	<div class="state" bind:this={stateElem} />

	<button class="submit" type="button" on:click={submit}>Submit</button>
</form>

<style>
	label {
		font-weight: 600;
		max-width: 500px;
	}
	input {
		width: 100%;
		max-width: 500px;
		margin-top: 0.5em;
		margin-bottom: 0.5em;
	}

	.state {
		font-style: italic;
	}

	button {
		margin-top: 2em;
	}

	.words-of-the-day {
		display: flex;
		gap: 20px;
		margin-bottom: 10px;
	}
	.word {
		padding: 0.5em 1em;
		background-color: gray;
		border-radius: 5px;
		font-size: 20px;
		color: black;
	}

	.word.filled {
		background-color: green;
		color: white;
	}
</style>
