<script lang="ts">
	import Prompt from '$lib/components/Prompt.svelte';

	import {Clock} from '$lib/static/control/clock';
	import {loadImages} from '$lib/static/control/imageLoader';
	import { postToJSON } from '$lib/static/fetcher';


	const numImagesInSet = 24;
	const delayBetweenImages = 800;
	
	// Keep track of the current step of the timer
	let counter = 0 ;

	let imageElem : HTMLImageElement;
	let images : HTMLImageElement[];

	let prompt : number[] = [];

	let correctGuessIndexes : number[] = [];
	let correctGuesses : string[] = [];

	let srcs :string[]= [];

	requestImagesFromServer(correctGuessIndexes);

	async function requestImagesFromServer(guesses: number[]) {
		 postToJSON(
			'http://localhost:8080/images', 
			{ correct_guesses: correctGuessIndexes }
		).then((srcs)=>{
			console.log("I GOT THESE SRCS",srcs);
			if (!srcs || srcs.length ===0) {
				youWon()
				throw '';
			}
			
			return srcs;
		}).then(loadImages).then((imgs) => {
			images = imgs;
			clock.start();
		}).catch((err)=>{
			if (err==="") return;
			console.log("IMAGE ERROR:",err.message)

			
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


	async function submitGuess(){
		return  postToJSON('http://localhost:8080/guess', { guess: textboxValue })
		.then((res: any) => {
			console.log("GUES RESULT: ",res);
			const index = parseInt(res.guess_index, 10);

			console.log("index: ",res.guess_index,res.guess);
			if (index === -1) return;

			correctGuesses.push(res.guess);
			correctGuesses = correctGuesses;

			// prompt[index] = guess;

			correctGuessIndexes.push(index);
			correctGuessIndexes = correctGuessIndexes;
			requestImagesFromServer(correctGuessIndexes);
			textboxValue='';
		})
		.catch((err) => console.log("ERROR",err));
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


	<form on:submit|preventDefault={submitGuess}>

	<div>
		CORRECT GUESSES :

		{#each correctGuesses as guess}
			<span>
				{guess}
			</span>
		{/each}
	</div>
		<input type="text" bind:value={textboxValue} use:autoFocus>


		<button type="submit" on:click={submitGuess}> SUBMIT!!</button>
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
