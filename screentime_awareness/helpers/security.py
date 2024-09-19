import bcrypt
from screentime_awareness.helpers.db import DBC


def get_secret() -> str:
    secret = open("../Tokens/secret_key.txt").read().strip()
    return secret

def encrypt_pw(user_id: str, password: str):
    # add the local secret to the password and hash them
    salt = bcrypt.gensalt()
    # note that using bcrypt, the salt is saved into the hash itself, so no need to store separately
    hashed_pw = bcrypt.hashpw((get_secret() + password).encode(), salt).decode()
    print(f'salt: {salt}')
    print(f'password hashed: {hashed_pw}')
    dbc = DBC()
    sql = f"insert into users values('{user_id}', '{hashed_pw}');"
    dbc.write(sql)

def validate_pw(user_id: str, entered_pw: str) -> bool:
    dbc = DBC()
    sql = f"select * from users where id = '{user_id}' LIMIT 1;"
    hashed_pw = dbc.select(sql)[0]['hashed_password']
    entered_pw =  entered_pw.encode()
    return bcrypt.checkpw(hashed_pw, entered_pw)
