import random
import string
import sys

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

def get_user(email_or_username: str, entered_pw: str,
             ignore_pw: bool = False) -> User or None:
    try:
        dbc = DBC()
        sql = f"select * from users where email = '{email_or_username}' LIMIT 1;"
        results = dbc.select(sql)
        if len(results) == 0:
            sql = f"select * from users where user_name = '{email_or_username}' LIMIT 1;"
            results = dbc.select(sql)
            if len(results) == 0:
                return None

        if not ignore_pw and not validate_pw(results[0]['hashed_password'], entered_pw):
            return None
        return User(email_or_username, results[0]['user_name'])
    except:
        if 'runserver' in sys.argv:
            # debug machine. allow log in
            return User('adw8122@gmail.com', 'debug')

def validate_pw(hashed_pw: str, entered_pw: str) -> bool:
    # combine the local secret to the prompted pw and encode to bytes
    # note again, the secret needs to be consistently appended
    #  to the end of the password (same as when encrytping)
    entered_pw = (entered_pw + get_secret()).encode()
    return bcrypt.checkpw(entered_pw, hashed_pw.encode())

def bad_creds_chars(cred_str: str) -> bool:
    bad_chars = ['{', '}', '\'', '\\']
    return len([c for c in cred_str if c in bad_chars]) > 0


def generate_random_str(length: int) -> str:
    return ''.join(random.SystemRandom().choice(string.ascii_uppercase
                    + string.ascii_lowercase + string.digits) for _ in range(length))

def reset_pw(link_uid: str):
    # This method is called when a user follows the emailed reset
    # The link must be followed within 30 minutes or it will expire, and the record
    #  is deleted from the table
    dbc = DBC()
    results = dbc.select(f"select email_address from forgot_pw where link_uid = '{link_uid}';")
    if (len(results)) > 0:
        # valid reset link. Delete the link NOW and store the email in a session variable in order
        #  to prevent a situation where the auto-expiration process removes it between now and
        #  when they choose a new password
        dbc.write(f"delete from forgot_pw where link_uid = '{link_uid}';")
        return results[0]['email_address']

def update_pw(pw: str, email: str):
    dbc = DBC()
    salt = bcrypt.gensalt()
    hashed_pw = bcrypt.hashpw((pw + get_secret()).encode(), salt).decode()
    dbc.write(f"update users set set hashed_password = '{hashed_pw}' where email = '{email}';")
