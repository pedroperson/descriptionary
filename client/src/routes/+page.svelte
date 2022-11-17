<script lang="ts">
	import Prompt from '$lib/components/Prompt.svelte';

	import {Clock} from '$lib/static/control/clock';

	const numImagesInSet = 10;
	const delayBetweenImages = 500;
	let counter = 0 ;

	let messageToUser = '';

	const yell = (message:string) => messageToUser = message;

	const everyStep = ()=> {
		yell(`show image ${counter}`);
		counter +=1;
	}

	const onEnd = () => {
		yell(`THIS GAME IS OVEER YA GOON!`);
	}

	const clock = Clock(
		numImagesInSet,
		delayBetweenImages, 
		everyStep,
		onEnd,
	)


	console.log("LETS STRAT");
	clock.start();
</script>

<svelte:head>
	<title>Home - Descriptionary</title>
	<meta name="description" content="Svelte demo app" />
</svelte:head>

<section>
	<h2>Create the image</h2>

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
