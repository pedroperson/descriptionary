from model import Handler,  Writer, RouteHandler
from node import traverse, handlers_to_node

import ast
from typing import List
from http.server import BaseHTTPRequestHandler, HTTPServer

ROOTS = {}


class Router:
    def __init__(self):
        self.root = []
        self.route_handlers_GET: List[RouteHandler] = []
        self.route_handlers_POST: List[RouteHandler] = []

    def GET(self, path: str, handler: Handler):
        path = clear_first_slash(path)
        self.route_handlers_GET.append(RouteHandler(path, handler))

    def POST(self, path: str, handler: Handler):
        path = clear_first_slash(path)
        self.route_handlers_POST.append(RouteHandler(path, handler))

    def start(self, serverPort: int = 8080):
        ROOTS["GET"] = handlers_to_node(self.route_handlers_GET)
        ROOTS["POST"] = handlers_to_node(self.route_handlers_POST)

        server = MyServer
        webServer = HTTPServer(("localhost", serverPort), server)
        print("Server started http://localhost:%d" % (serverPort))

        try:
            webServer.serve_forever()
        except KeyboardInterrupt:
            pass

        webServer.server_close()
        print("Server stopped.")


class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        callback = traverse(ROOTS["GET"], self.path)
        if callback is None:
            self._set_response(404)
            return

        callback({}, Writer(self))

    def do_POST(self):
        callback = traverse(ROOTS["POST"], self.path)
        if callback is None:
            self._set_response(404)
            return

        callback(self._read_body(), Writer(self))

    def _set_response(self, code=200):
        self.send_response(code)
        self.end_headers()

    def _read_body(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        return ast.literal_eval(post_data.decode('utf-8'))


def clear_first_slash(path):
    return path[1:] if path[0] == "/" else path
