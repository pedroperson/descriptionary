# Model

A daily game like wordle, single player.

## Point system

- +10 good guess
- -1 bad guess
- -2 repeated guess

# Backend

- Figure out how to generate image
- What if guess wrong a lot of times?
  - Figure out if we give them hints through text or just making the image more clear
  - Limit the amount of attempts so user doesn't just try every word in the dictionary -> Throttle the server request like a password form, OR show a commercial every once in a while.
  - Generate the senteces -> Get a madlib database for these

# Frontend

[ ] Max amount of tries ?

[x] Keep a localStorage of user data

[x] Keep score of attempts

[x] Cache attempts so user doesn't forget? Maybe reduce points as a punishment?
