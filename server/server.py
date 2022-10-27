# Python 3 server example
import ast
from http.server import BaseHTTPRequestHandler, HTTPServer
import time
import logging
from keywords import todays_list, testGuess

import json

hostName = "localhost"
serverPort = 8080


class MyServer(BaseHTTPRequestHandler):
    def _set_response(self, code=200):
        self.send_response(code)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.end_headers()

    def _read_body(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        return ast.literal_eval(post_data.decode('utf-8'))

    def do_GET(self):
        if self.path == "/sentence":
            self._set_response(200)
            todays_sentence = "For instance, Zeus is the god of the { }, Poseidon is the { } of the sea and Hephaestus is the god of { }"
            self.wfile.write(bytes(todays_sentence, "utf-8"))
            return

        self._set_response(404)

    def do_POST(self):
        if self.path == "/guess":
            mydata = self._read_body()
            guess = mydata['guess']
            FAKELIST = ["sky", "god", "fire"]
            guess_index = testGuess(guess, FAKELIST)
            self._set_response(200)
            self.wfile.write(bytes(str(guess_index), "utf-8"))
            return

        self._set_response(404)


if __name__ == "__main__":
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")
