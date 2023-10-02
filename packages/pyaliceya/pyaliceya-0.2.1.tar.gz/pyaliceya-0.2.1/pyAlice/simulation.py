import os
from sys import platform

from pyAlice.functions import clear_console


class Simulation:
    def __init__(self, handler):
        clear_console()
        self.handler = handler
        self.user_data = ""
        self.storage = {}
        self.response()

    def request(self):
        self.user_data = input()
        return self.handler({
            "meta": {
                "locale": "ru-RU",
                "timezone": "UTC",
                "client_id": "ru.yandex",
                "interfaces": {
                    "screen": {},
                    "payments": {},
                    "account_linking": {}
                }
            },
            "session": {
                "message_id": 5,
                "session_id": "4567hjl-e484-48666-b253-f4c7b4632385",
                "skill_id": "37ccdfghb22-0b07-4a83-85c0-8517d17ccda7",
                "user": {
                    "user_id": "000000000000000000"
                },
                "application": {
                    "application_id": "00000000000"
                },
                "new": False,
                "user_id": "000000000"
            },
            "request": {
                "command": f"{self.user_data}",
                "original_utterance": f"{self.user_data}",
                "nlu": {
                    "tokens": [item for item in self.user_data.split(" ")],
                    "entities": [],
                    "intents": {}
                },
                "markup": {
                    "dangerous_context": False
                },
                "type": "SimpleUtterance"
            },
            "state": {
                "session": self.storage,
                "user": {},
                "application": {}
            },
            "version": "1.0"
        }, "context")

    def response(self):
        while True:
            req = self.request()
            print(req["response"]["text"])
            print("Press ctrl+c to exit")
            self.storage = req["state"]["session"]
            if req["response"]["end_session"] == True:
                exit()
