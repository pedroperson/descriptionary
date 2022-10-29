from model import IncomingData, Writer
from keywords import testGuess
from router import Router


def initRouter():
    r = Router()
    r.GET("/sentence", todays_sentence)
    r.POST("/guess", check_guess)
    r.start(8080)


def todays_sentence(data, writer: Writer):
    todays_sentence = "For instance, Zeus is the god of the { }, Poseidon is the { } of the sea and Hephaestus is the god of { }"
    writer.send_result(todays_sentence)


def check_guess(data: IncomingData, writer: Writer):
    guess = data['guess']
    FAKELIST = ["sky", "god", "fire"]
    guess_index = testGuess(guess, FAKELIST)
    writer.send_result(guess_index)


if __name__ == "__main__":
    initRouter()
