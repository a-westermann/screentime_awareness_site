from django.db import models

class User:
    def __init__(self, email: str):
        self.email = email
        self.user_name = email.split('@')[0]
