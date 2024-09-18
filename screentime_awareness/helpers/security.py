import bcrypt
from screentime_awareness.helpers.db import DBC


def get_secret() -> str:
    secret = open("../Tokens/secret_key.txt").read().strip()
    return secret

def encrypt_pw(user_id: str, password: str):
    # add the local secret to the password and hash them
    salt = bcrypt.gensalt()
    hashed_pw = bcrypt.hashpw((get_secret() + password).encode(), salt)
    dbc = DBC()
    sql = f"insert into users values('{user_id}', '{salt}');"
    dbc.write(sql)

def decrypt_pw(user_id: str):
    pass
