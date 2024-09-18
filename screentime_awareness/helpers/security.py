import bcrypt


def get_secret() -> str:
    secret = open("../Tokens/secret_key.txt").read().strip()
    return secret

def encrypt_pw(user_id: str, password: str):
    # add the local secret to the password and hash them
    hashed_pw = bcrypt.hashpw((get_secret() + password).encode(), bcrypt.gensalt())

