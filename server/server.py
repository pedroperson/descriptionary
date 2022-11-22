from model import IncomingData, Writer
from keywords import testGuess
from router import Router


def initRouter():
    r = Router()
    r.GET("/sentence", todays_sentence)
    r.POST("/images", todays_images)
    r.POST("/guess", check_guess)
    r.start(8080)


def todays_sentence(data, writer: Writer):
    todays_sentence = "For instance, Zeus is the god of the { }, Poseidon is the { } of the sea and Hephaestus is the god of { }"
    writer.send_result(todays_sentence)


def todays_images(data: IncomingData, writer: Writer):
    print("Incoming data", data)
    words = ["plant", "pot", "glass", "wood"]

    guesses = data['correct_guesses']

    for i in range(len(guesses)):
        guesses[i] = int(guesses[i])

    new_words = []
    for i in range(len(words)):
        if i not in guesses:
            new_words.append(words[i])

    print("new_words", new_words)

    query = '+'.join(new_words)
    urls = []
    image_count = 18
    for i in range(image_count):
        urls.append(
            f"https://bitbu-public.s3.us-west-1.amazonaws.com/homepage/DELETE_aiproj/{query}+{i}.jpg")

    print("urls", urls)

    writer.send_result(urls)


def check_guess(data: IncomingData, writer: Writer):
    guess = data['guess']
    FAKELIST = ["sky", "god", "fire"]
    guess_index = testGuess(guess, FAKELIST)
    writer.send_result(guess_index)


if __name__ == "__main__":
    initRouter()
