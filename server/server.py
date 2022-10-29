from model import IncomingData, Writer
from keywords import testGuess
from router import Router


def initRouter():
    r = Router()
    r.GET("/sentence", returnTodaysSentence)
    r.POST("/guess", checkGuess)
    r.start(8080)


def returnTodaysSentence(data, writer: Writer):
    todays_sentence = "For instance, Zeus is the god of the { }, Poseidon is the { } of the sea and Hephaestus is the god of { }"
    writer.send_result(todays_sentence)


def checkGuess(data: IncomingData, writer: Writer):
    guess = data['guess']
    FAKELIST = ["sky", "god", "fire"]
    guess_index = testGuess(guess, FAKELIST)
    writer.send_result(guess_index)


if __name__ == "__main__":
    initRouter()
