from pydantic import BaseModel
from enum import Enum
from typing import Optional


class ResponseTypes(Enum):
    HTML = 'html'
    JSON = 'json'


class RestHeaders:
    def __init__(self, request):
        headers = request.headers
        self.host = headers['host'] if 'host' in headers else None
        self.connection = headers['connection'] if 'connection' in headers else None
        self.accept = headers['accept'] if 'accept' in headers else None
        self.accept_encoding = headers['accept_encoding'] if 'accept_encoding' in headers else None

    @property
    def response_type(self):
        if 'html' in self.accept:
            return ResponseTypes.HTML
        else:
            return ResponseTypes.JSON

    # host
    # connection
    # sec_ch_ua
    # Chromium
    # sec_ch_ua_platform
    # upgrade_insecure_requests
    # user_agent
    # accept
    # accept_encoding
