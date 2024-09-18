import bcrypt


def get_secret() -> str:
    secret = open("../Tokens/secret_key.txt").read().strip()
    return secret
