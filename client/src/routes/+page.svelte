<script lang="ts">
	import Prompt from '$lib/components/Prompt.svelte';

	import {Clock} from '$lib/static/control/clock';
	import {loadImages} from '$lib/static/control/imageLoader';

	const numImagesInSet = 18;
	const delayBetweenImages = 500;
	let counter = 0 ;

	const srcs = Array(numImagesInSet).fill('').map((_,i)=>`/images/ Porcupine  sandwich ${i}.jpg`);
	console.log("srcs",srcs);
	

	let imageElem : HTMLImageElement;
	let images : HTMLImageElement[];
	
	if (typeof window !== "undefined"){
		loadImages(srcs)
		.then((imgs) => {
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
