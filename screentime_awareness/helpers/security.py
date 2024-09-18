import bcrypt
from screentime_awareness.helpers.db import DBC


def get_secret() -> str:
    secret = open("../Tokens/secret_key.txt").read().strip()
    return secret

def encrypt_pw(user_id: str, password: str):
    # add the local secret to the password and hash them
    salt = bcrypt.gensalt()
    hashed_pw = str(bcrypt.hashpw((get_secret() + password).encode(), salt))
    print(f'salt: {salt}')
    print(f'password hashed: {hashed_pw}')
    dbc = DBC()
    sql = f"insert into users values('{user_id}', '{hashed_pw}');"
    dbc.write(sql)

def decrypt_pw(user_id: str):
    pass
