from django.db import models

class User:
    def __init__(self, email: str, username: str):
        self.email = email
        self.username = username
