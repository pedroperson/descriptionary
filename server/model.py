
from typing import Dict,  Any, Callable
from http.server import BaseHTTPRequestHandler
from dataclasses import dataclass, field

class Writer:
    def __init__(self, requestHandler: BaseHTTPRequestHandler):
        self.h = requestHandler

    def _set_response(self, code=200):
        self.h.send_response(code)
        self.h.send_header('Access-Control-Allow-Origin', '*')
        self.h.send_header('Access-Control-Allow-Methods',
                           'GET, POST, OPTIONS')
        self.h.end_headers()

    # Currently only accepts numbers and strings
    def send_result(self, result: Any):
        self._set_response(200)
        self.h.wfile.write(bytes(str(result), "utf-8"))

    def send_success(self):
        self._set_response(200)

    def send_error(self, error: str):
        self._set_response(400)
        self.h.wfile.write(bytes(str(error), "utf-8"))


IncomingData = Dict[str, Any]

Handler = Callable[[IncomingData, Writer], None]


@dataclass
class RouteHandler:
    path: str
    handler: Handler
