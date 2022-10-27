<script lang="ts">
	import { submitGuess, correctGuesses, reset } from '../static/game';
	import { SCORE } from '../static/points';

	// Current state of the user query
	let query = '';

	// Keep a reference to the state element so we can talk to the user through it
	let stateElem: Element;
	const tellUser = (msg: string) => (stateElem.innerHTML = msg);

	const submit = () =>
		submitGuess(query)
			.then(tellUser)
			.then(() => {
				// Reset the query so the textbox is emptied and user can try again
				query = '';
			});
</script>

<div class="score">
	{$SCORE}
</div>

<div class="words-of-the-day">
	{#each $correctGuesses as g, i (i)}
		<div class="word" class:filled={g}>
			{g}
		</div>
	{/each}
</div>

<form on:submit|preventDefault={submit}>
	<label for="promp-textbox">Write your guess, one word, five letters long</label>
	<input
		id="promp-textbox"
		type="text"
		placeholder="Denim..."
		bind:value={query}
		autocomplete="off"
	/>

	<div class="state" bind:this={stateElem} />

	<button class="submit" type="button" on:click={submit}>Submit</button>
    <button class="submit" type="button" on:click={reset}>Reset</button>
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
