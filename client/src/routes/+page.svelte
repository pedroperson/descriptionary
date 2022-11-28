<script lang="ts">
	import {Clock} from '$lib/static/control/clock';
	import api from '$lib/static/api/api';
	
	const numImagesInSet = 24;
	const delayBetweenImages = 800;
	
	// Keep track of the current step of the timer 
	// TODO: This is bad right? just use th timer's own count
	let counter = 0 ;

	let textboxValue = '';

	let imageElem : HTMLImageElement;
	let images : HTMLImageElement[];

	let prompt : string[] = [];

	let correctGuessIndexes : number[] = [];
	let correctGuesses : string[] = [];

	// Load the images ASAP so we can show them to the user
	requestImagesFromServer(correctGuessIndexes);
	// Request the word count ASAP so we can show the correct number of "blank spaces" 
	requestWordCount();

	// We will keep a Clock to tick between images
	function onClockTick(){
		if (counter >= images.length) {
			// Loop the counter background
			counter = 0;
		};
		console.log("COUNTER",counter);
		console.log("images.length",images.length);
		imageElem.src= images[counter].src;
		counter +=1;
	}

	// When the clock reaches its end, we start it up again
	const onClockTimeout = () => {
		counter = 0;
		clock.start();
	}

	const clock = Clock(
		numImagesInSet,
		delayBetweenImages, 
		onClockTick,
		onClockTimeout,
	)


	async function requestWordCount() {
		api.requestWordCount()
			.then((count)=>{
				for (let index = 0; index < count; index++) {
					prompt.push("");
				}
			}).catch((err)=>{
				//  TODO: deal with this error properly
				console.log("count ERROR:",err.message);
			});
	}

	// requestImagesFromServer submits our current correct answers to the server and gets the next set of images
	async function requestImagesFromServer(guesses: number[]) {
		const imgs = await api.requestImages(guesses).catch((err)=>{
			console.log("IMAGE ERROR:",err.message ?err.message:err);
			return null
		});

		if (imgs === null ) return;
		
		// TODO: This is bad. We are interpreting an empty response as a game win point.
		if ( imgs.length ===0) {
			youWon()
			throw '';
		}

		images = imgs;
		clock.start();
	}

	const youWon = ()=> {
	    counter = 0 ;
		clock.stop();
		yell("HOLY MOLY JULIE! THEY WON! THEY WON THE GAMEE!!");
	}

	const isIncorrectGuess = (index:number) => index === -1;

	async function submitForm(){
		const res = await api.submitGuess(textboxValue).catch(err=>{
			// TODO: properly handle this error
			console.log("SUBMIT GUESS ERROR",err);
			return null;
		});
		if (res ===null) return;

		if (isIncorrectGuess(res.guess_index)) return;

		handleCorrectGuess(res.guess_index, res.guess);
	}

	// handleCorrectGuess stores the correct guess data so we can display it to the user
	function handleCorrectGuess(index:number, guess:string){
		correctGuesses.push(guess);
		correctGuesses = correctGuesses;

		prompt[index] = guess;

		correctGuessIndexes.push(index);
		correctGuessIndexes = correctGuessIndexes;

		requestImagesFromServer(correctGuessIndexes);

		// Clear the textbox to facilitate next guess
		textboxValue='';
	}


	// Allows us to focus on the textbox soon after the page has opened
	const autoFocus = (node:HTMLInputElement) => {
		setTimeout(()=>node.focus(),200);
	}

	// Show messages to the user in the page layout
	let messageToUser = '';
	const yell = (message:string) => messageToUser = message;

</script>

<svelte:head>
	<title>Home - Descriptionary</title>
	<meta name="description" content="Svelte demo app" />
</svelte:head>

<section>
	<form on:submit|preventDefault={submitForm}>
		<div class="submitdiv">
			<input class="textbox" type="text" bind:value={textboxValue} use:autoFocus>
			<button class="submitbtn" type="submit" on:click={submitForm}> SUBMIT!!</button>
		</div>
</form>

	<div class="responsediv">

		<img class = "imagedisplay" bind:this={imageElem} alt="created by ai, sorry I can't give you more hints without giving you the answer"/>
		<div>{messageToUser}</div>


		<div class="correctguesses">
		 <div>	CORRECT GUESSES :</div>
	
			<ul class="prompts">
				{#each prompt as guess}
					<li>
						{#if !guess || guess === ''}
						_______ 
						{:else}
						{guess}
						{/if}
					</li>
				{/each}
				</ul>
		</div>
	</div>
</section>

<style>

	section {
		display: flex;
		flex-direction: column;
		justify-content: center;
		flex: 0.6;
		gap: 20px;
	}

	.prompts {
		list-style: none; margin:0;padding:0;
		display: flex;
		flex-wrap: wrap;
		gap: 5px;
	}
	
	.responsediv {
		display: flex;
		gap: 10px;
	}

	.submitdiv {
		display: flex;
		gap: 10px;
	}

	.textbox {
		width: 800px;
		height: 78px;

		background: #D9D9D9;
		border: 3px solid #140F0F;
		border-radius: 7px;
	}

	.submitbtn {
		height: 78px;
		border-radius: 19px;
		background: #468B00;

		font-family: 'Helvetica';
		font-style: normal;
		font-weight: 400;
		font-size: 32px;
		line-height: 37px;
		display: flex;
		align-items: center;
		text-align: center;

		color: #000000;
	}

	.imagedisplay {
		width: 50%;
		height: 419px;
		left: 207px;
		top: 282px;
	}

	.correctguesses {
		height: 427px;
		left: 677px;
		top: 271px;

		font-family: 'Helvetica';
		font-style: normal;
		font-weight: 400;
		font-size: 24px;
		line-height: 28px;
		display: flex;
		align-items: center;
		flex-direction: column
	}
</style>
