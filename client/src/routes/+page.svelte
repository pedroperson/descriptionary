<script lang="ts">
	import Prompt from '$lib/components/Prompt.svelte';

	import {Clock} from '$lib/static/control/clock';
	import {loadImages} from '$lib/static/control/imageLoader';
	import { post } from '$lib/static/fetcher';


	const numImagesInSet = 18;
	const delayBetweenImages = 500;
	
	// Keep track of the current step of the timer
	let counter = 0 ;

	let imageElem : HTMLImageElement;
	let images : HTMLImageElement[];

	let correctGuesses : string[] = [];

	let srcs = [];

	requestImagesFromServer(correctGuesses);

	async function requestImagesFromServer(guesses: string[]) {
		const srcs = await post(
			'http://localhost:8080/images', 
			{ correct_guesses: correctGuesses }
		).then((res)=>{
			console.log(res);
			return res;
		}).catch((err)=>{
			console.log("asdfasd",err)
		});

		console.log("I GOT THE IMAGES",srcs);
	}






	// const srcs = Array(numImagesInSet).fill('')
	// 	.map((_, i) => `/images/ Porcupine  sandwich ${i}.jpg`);

	
	if (typeof window !== "undefined"){
		loadImages(srcs).then((imgs) => {
			images = imgs;
			console.log("LETS STRAT");
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
		imageElem.src= "";
		yell(`THIS GAME IS OVEER YA GOON!`);
	}

	const clock = Clock(
		numImagesInSet,
		delayBetweenImages, 
		everyStep,
		onEnd,
	)


</script>

<svelte:head>
	<title>Home - Descriptionary</title>
	<meta name="description" content="Svelte demo app" />
</svelte:head>

<section>
	<h2>Create the image</h2>

	<img bind:this={imageElem} alt="created by ai, sorry I can't give you more hints without giving you the answer"/>
	<div>{messageToUser}</div>

	<Prompt />
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
