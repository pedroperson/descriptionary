<script lang="ts">
	import Prompt from '$lib/components/Prompt.svelte';

	import {Clock} from '$lib/static/control/clock';
	import {loadImages} from '$lib/static/control/imageLoader';
	import { post,postToJSON } from '$lib/static/fetcher';


	const numImagesInSet = 18;
	const delayBetweenImages = 100;
	
	// Keep track of the current step of the timer
	let counter = 0 ;

	let imageElem : HTMLImageElement;
	let images : HTMLImageElement[];

	let correctGuesses : number[] = [];

	let srcs :string[]= [];

	requestImagesFromServer(correctGuesses);

	async function requestImagesFromServer(guesses: number[]) {
		 postToJSON(
			'http://localhost:8080/images', 
			{ correct_guesses: correctGuesses }
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
clock.stop();
yell("HOLY MOLY JULIE! THEY WON! THEY WON THE GAMEE!!");}
	
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
		yell(`show image ${counter}`);
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
		return  post('http://localhost:8080/guess', { guess: textboxValue })
		.then((res: string) => {
			console.log("GUES RESULT: ",res);
			const index = parseInt(res, 10);
			
			if (index === -1) return;

			correctGuesses.push(index);
			correctGuesses = correctGuesses;
			requestImagesFromServer(correctGuesses);
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
		CORRECT GUESSES : {JSON.stringify(correctGuesses)}
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
