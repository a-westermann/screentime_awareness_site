from django.db import models
import json


class User:
    def __init__(self, email: str, username: str):
        self.email = email
        self.username = username

    def to_json(self):
        return json.dumps(
            self,
            default=lambda o: o.__dict__,
            sort_keys=True,
            indent=4)
