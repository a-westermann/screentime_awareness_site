import bcrypt
from screentime_awareness.helpers.db import DBC
from screentime_awareness.models import User


def get_secret() -> str:
    secret = open("../Tokens/secret_key.txt").read().strip()
    return secret

def add_user_to_db(email: str, password: str, username: str):
    # add the local secret to the password and hash them
    salt = bcrypt.gensalt()
    # note that using bcrypt, the salt is saved into the hash itself, so no need to store separately
    # due to length limits from bcrypt, it's important to put the secret at the end of the hash
    hashed_pw = bcrypt.hashpw((password + get_secret()).encode(), salt).decode()
    print(f'salt: {salt}')
    print(f'password hashed: {hashed_pw}')
    dbc = DBC()
    sql = f"insert into users values('{email}', '{hashed_pw}', '{username}');"
    dbc.write(sql)

def check_registered(email_address: str) -> bool:
    sql = f"select * from users where email = '{email_address}' LIMIT 1;"
    dbc = DBC()
    results = dbc.select(sql)
    return len(results) > 0

def get_user(email_or_username: str, entered_pw: str) -> User or None:
    try:
        dbc = DBC()
        sql = f"select * from users where email = '{email_or_username}' LIMIT 1;"
        results = dbc.select(sql)
        if len(results) == 0:
            sql = f"select * from users where user_name = '{email_or_username}' LIMIT 1;"
            results = dbc.select(sql)
            if len(results) == 0:
                return None

        if not validate_pw(results[0]['hashed_password'], entered_pw):
            return None
        return User(email_or_username, results[0]['user_name'])
    except:
        # if DEBUG  how to?
        # debug machine. allow log in
        return User('adw8122@gmail.com', 'debug')

def validate_pw(hashed_pw: str, entered_pw: str) -> bool:
    # combine the local secret to the prompted pw and encode to bytes
    # note again, the secret needs to be consistently appended
    #  to the end of the password (same as when encrytping)
    entered_pw = (entered_pw + get_secret()).encode()
    return bcrypt.checkpw(entered_pw, hashed_pw.encode())
