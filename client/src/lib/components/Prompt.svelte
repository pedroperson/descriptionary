<script lang="ts">
	import { onMount } from 'svelte';
	import {
		submitGuess,
		correctGuesses,
		reset,
		todaysSentence,
		type CorrectGuess
	} from '../static/game';
	import { SCORE } from '../static/points';

	// Current state of the user query
	let query = '';
	const resetQuery = ()=>(query="")

	// Keep a reference to the state element so we can broadcast state to the user through it
	let stateElem: Element;
	const tellUser = (msg: string) => (stateElem.innerHTML = msg);

	const submit = () =>
		submitGuess(query)
			.then(tellUser)
			.then(resetQuery);

	let promise: Promise<string> = new Promise(() => {});

	const separator = '{ }';
	const separator2 = '______';

	onMount(() => {
		promise = todaysSentence()
			.then((rawSentence) => rawSentence.replaceAll(separator, separator2))
			.catch((err) => '');
	});

	const fillInTheBlanks = (sentence: string, guesses: CorrectGuess[]): string => {
        console.log("fill",sentence,guesses)
		return sentence.split(separator2).reduce((acc, phrase, i) => {
			if (i == 0) return phrase;

			const relatedGuess = guesses.find((g) => g.index === i - 1);

			if (relatedGuess === undefined) return acc + separator2 + phrase;
			return acc + relatedGuess.guess + phrase;
		}, '');
	};
</script>

<div class="score">
	{$SCORE}
</div>

<div class="sentence">
	{#await promise}
		loading sentence....
	{:then sentence}
		{fillInTheBlanks(sentence, $correctGuesses)}
	{:catch err}
		fuck there was error: {JSON.stringify(err)}
	{/await}
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
