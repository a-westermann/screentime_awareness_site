import bcrypt
from screentime_awareness.helpers.db import DBC


def get_secret() -> str:
    secret = open("../Tokens/secret_key.txt").read().strip()
    return secret

def add_user_to_db(user_id: str, password: str):
    # add the local secret to the password and hash them
    salt = bcrypt.gensalt()
    # note that using bcrypt, the salt is saved into the hash itself, so no need to store separately
    # due to length limits from bcrypt, it's important to put the secret at the end of the hash
    hashed_pw = bcrypt.hashpw((password + get_secret()).encode(), salt).decode()
    print(f'salt: {salt}')
    print(f'password hashed: {hashed_pw}')
    dbc = DBC()
    sql = f"insert into users values('{user_id}', '{hashed_pw}');"
    dbc.write(sql)

def validate_pw(email_address: str, entered_pw: str) -> bool:
    try:
        dbc = DBC()
        sql = f"select * from users where id = '{email_address}' LIMIT 1;"
        results = dbc.select(sql)
        if len(results) == 0:
            return False
        hashed_pw = results[0]['hashed_password']
        # combine the local secret to the prompted pw and encode to bytes
        # note again, the secret needs to be consistently appended
        #  to the end of the password (same as when encrytping)
        entered_pw = (entered_pw + get_secret()).encode()
        return bcrypt.checkpw(entered_pw, hashed_pw.encode())
    except:  # on debug machine - remove in prod
        return True
