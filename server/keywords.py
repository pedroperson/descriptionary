import random
import os


# # gives the path of demo.py
# path = os.path.realpath(__file__)
# print(path)
# parent = path.split('/keywords')[0]
# print(parent)
# file = parent+"/static/valid-wordle-words.txt"

# with open(file, 'r') as f:
#     word_list = f.read()

# word_list = word_list.split()
# todays_list = random.sample(word_list, 4)
# print("Todays list:", todays_list)


def testGuess(guess: str,
              word_list: list) -> int:
    try:
        return word_list.index(guess)
    except ValueError:
        return -1
