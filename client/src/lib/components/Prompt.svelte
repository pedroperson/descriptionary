<script lang="ts">
    import {post} from "../static/fetcher"

    let query = '';
    let stateElem:Element;

    const tellUser = (str:string)=> stateElem.innerHTML = str;

    const wordCount = 4;
    let guessIndex = 0;
    const correctGuesses:string[] = new Array(wordCount).fill('');

    const submit = ()=>{
        console.log("submit!");
        const q = query;
        if (correctGuesses.includes(q)) {
            tellUser(`You've already guessed "${query}"`);
            return
        }
        post("/guess", {guess:q})
        .then(({correct})=>{
            if (correct) {
                correctGuesses[guessIndex] = q;
                guessIndex += 1;
                tellUser("holy shit you got a word right");
                query = '';

                if (guessIndex === wordCount) {
                    window.alert("you won the game");
                }
            }else {
                tellUser(`"${query}" was a shit guess`);
                query = '';
            }
        }).catch(err=>console.log("err",err))
    }




</script>

<div class="words-of-the-day">
    {#each correctGuesses as g,i (i)}
        <div class="word" class:filled={g}>
            {g}
        </div>
    {/each}
</div>

<form on:submit|preventDefault={submit}>
    <label for="promp-textbox">Write your guess, one word, five letters long</label>
    <input id="promp-textbox" type="text" placeholder="Denim..." bind:value={query} >

    <div class="state" bind:this={stateElem}> </div>

    <button class="submit" type="button" on:click={submit}>Submit</button>
</form>

<style>

    label {
        font-weight: 600;
        max-width:500px;
    }
    input {
        width:100%;
        max-width:500px;
        margin-top:0.5em;
        margin-bottom:0.5em;
    }


    .state {
        font-style: italic;
    }

    button {
        margin-top:2em;
    }

    .words-of-the-day {
        display:flex;
        gap:20px;
        margin-bottom: 10px;
    }
    .word {
        padding:0.5em 1em;
        background-color:gray;
        border-radius:5px;
        font-size:20px;
        color:black;
    }

    .word.filled {
        background-color:green;
        color:white;
    }
</style>