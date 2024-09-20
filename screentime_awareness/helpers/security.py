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

def validate_pw(email_address: str, entered_pw: str) -> bool:
    dbc = DBC()
    sql = f"select * from users where id = '{email_address}' LIMIT 1;"
    results = dbc.select(sql)
    if len(results) == 0:
        return False
    hashed_pw = results['hashed_password']
    # combine the local secret to the prompted pw and encode to bytes
    entered_pw = (get_secret() + entered_pw).encode()
    return bcrypt.checkpw(entered_pw, hashed_pw.encode())
