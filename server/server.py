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


WORDS = ["plant", "pot", "glass", "wood"]


def todays_images(data: IncomingData, writer: Writer):
    guesses = data['correct_guesses']

    for i in range(len(guesses)):
        guesses[i] = int(guesses[i])

    new_words = []
    for i in range(len(WORDS)):
        if i not in guesses:
            new_words.append(WORDS[i])

    if len(new_words) is 0:
        writer.send_result([])
        return

    query = '+'.join(new_words)
    urls = []
    image_count = 25
    for i in range(image_count):
        urls.append(
            f"https://bitbu-public.s3.us-west-1.amazonaws.com/homepage/DELETE_aiproj/{query}+{i}.jpg")

    writer.send_result(urls)


def check_guess(data: IncomingData, writer: Writer):
    guess = data['guess']
    guess_index = testGuess(guess, WORDS)
    writer.send_result(guess_index)


if __name__ == "__main__":
    initRouter()
