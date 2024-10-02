from django.core.mail import EmailMessage
from screentime_awareness.helpers import db, security


def email_pw_recovery(email_address: str):
    #TODO: Generate a unique identifier that links this email address to a
    # specific password reset url
    # The link needs to be generated at the time of this process
    # Save the email and UID in the db. Then when they follow the link
    #  you can select the dbo.user record by joining on the link uid table
    # Set up a regular process that expires the links in the db after x minutes
    # Clear the records out when they expire so the table is empty by default

    # insert into db a random link associated with the user's email
    dbc = db.DBC()
    results = dbc.select(f"select * from forgot_pw where email_address = '{email_address}")
    link_uid = security.generate_random_str(30)
    if len(results) > 0:  # if there is already one, overwrite it
        dbc.write(f"update forgot_pw set link_uid = '{link_uid}' where email_address = '{email_address}'")
    else:
        dbc.write(f"insert into forgot_pw values('{email_address}', '{link_uid}')")

    print(f'sending password recovery email to {email_address}')
    em = EmailMessage(subject='Go Beyond the Screen Password Recovery',
        body='We received a request to reset your password for '
                'gobeyondthescreen.org.'
                '\n\n<b>Please follow this link to reset your password:</b>'
                f'\nhttps://gobeyondthescreen.org/reset_pw/uid={link_uid}/'
                '\n\nIf you did not make this request, you can safely ignore this '
                'email.',
        to=[email_address])
    print(f'email send count: {em.send()}')
