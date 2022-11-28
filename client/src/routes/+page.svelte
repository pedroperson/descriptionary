<script lang="ts">
	import Prompt from '$lib/components/Prompt.svelte';

	import {Clock} from '$lib/static/control/clock';
	import {loadImages} from '$lib/static/control/imageLoader';
	import { postToJSON, getToJSON } from '$lib/static/fetcher';
	import api from '$lib/static/api/api';
	


	const numImagesInSet = 24;
	const delayBetweenImages = 800;
	
	// Keep track of the current step of the timer
	let counter = 0 ;

	let imageElem : HTMLImageElement;
	let images : HTMLImageElement[];

	let prompt : string[] = [];
	requestWordCount();

	let correctGuessIndexes : number[] = [];
	let correctGuesses : string[] = [];

	let srcs :string[]= [];

	requestImagesFromServer(correctGuessIndexes);

	async function requestImagesFromServer(guesses: number[]) {
		api.requestImages(correctGuessIndexes).then((imgs)=>{
			if (!imgs || imgs.length ===0) {
				youWon()
				throw '';
			}

			images = imgs;
			clock.start();
		}).catch((err)=>{
			if (err==="") return;
			console.log("IMAGE ERROR:",err.message)
		});

	}

	async function requestWordCount() {
		api.requestWordCount()
			.then((count)=>{
				console.log("count", count);
				for (let index = 0; index < count; index++) {
					prompt.push("");
				}
				console.log("prompt0,",prompt);
			}).catch((err)=>{
				console.log("count ERROR:",err.message);
			});
	}

	const youWon = ()=> {
	    counter = 0 ;
		clock.stop();
		yell("HOLY MOLY JULIE! THEY WON! THEY WON THE GAMEE!!");
	}
	
	if (typeof window !== "undefined"){
		loadImages(srcs).then((imgs) => {
			images = imgs;
			console.log("INITIAL IMAGES");
			clock.start();
		})
	}
	
	let messageToUser = '';

	const yell = (message:string) => messageToUser = message;

	const everyStep = ()=> {
		// yell(`show image ${counter}`);
		if (counter >= images.length) return;

		imageElem.src= images[counter].src;
		counter +=1;
	}

	const onEnd = () => {
		console.log("OMG ITS OVER!");
		counter = 0;
		clock.start();
	}

	const clock = Clock(
		numImagesInSet,
		delayBetweenImages, 
		everyStep,
		onEnd,
	)

	let textboxValue = '';


	async function submitForm(){
		return api.submitGuess(textboxValue)
			.then((res) => {
				const isIncorrectGuess = res.guess_index === -1;

				console.log("isIncorrectGuess",isIncorrectGuess)
				if (isIncorrectGuess) return;
				// TODO: break to separate function

				correctGuesses.push(res.guess);
				correctGuesses = correctGuesses;

				prompt[res.guess_index] = res.guess;

				correctGuessIndexes.push(res.guess_index);
				correctGuessIndexes = correctGuessIndexes;

				requestImagesFromServer(correctGuessIndexes);
				textboxValue='';
		})
		.catch((err) => console.log("SUBMIT ERROR",err));
	}


	const autoFocus = (node:HTMLInputElement) => {
		setTimeout(()=>node.focus(),200);
	}

</script>

<svelte:head>
	<title>Home - Descriptionary</title>
	<meta name="description" content="Svelte demo app" />
</svelte:head>

<section>
	<h2>Create the image</h2>

	<img bind:this={imageElem} alt="created by ai, sorry I can't give you more hints without giving you the answer"/>
	<div>{messageToUser}</div>


	<form on:submit|preventDefault={submitForm}>

	<div>
		CORRECT GUESSES :

		{#each prompt as guess}
			<span>
				{#if !guess || guess === ''}
				 _______ 
				{:else}
				{guess}
				{/if}
			</span>
		{/each}
	</div>
		<input type="text" bind:value={textboxValue} use:autoFocus>


		<button type="submit" on:click={submitForm}> SUBMIT!!</button>
	</form>
</section>

<style>
	section {
		display: flex;
		flex-direction: column;
		justify-content: center;
		align-items: center;
		flex: 0.6;
	}
</style>
