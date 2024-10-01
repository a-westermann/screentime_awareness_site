from django.core.mail import EmailMessage


# Plan: send an email with a link. If link is followed, it allows
#  the user to enter a new password
def email_pw_recovery(email_address: str):
    #TODO: Generate a unique identifier that links this user to a
    # specific password reset url
    # The link needs to be generated at the time of this process
    # Save the email and UID in the db. Then when they follow the link
    #  you can select the dbo.user record by joining on the link uid table
    # Set up a regular process that expires the links in the db after x minutes
    # Clear the records out when they expire so the table is empty by default
    print(f'sending password recovery email to {email_address}')
    em = EmailMessage(subject='Go Beyond the Screen Password Recovery',
        body='We received a request to reset your password for '
                'gobeyondthescreen.org.'
                '\nPlease follow this link to reset your password:'
                '\nhttps://gobeyondthescreen.org/reset_password=XLKjsijknmcJLKXoi20982klclSLKj'
                '\n\nIf you did not make this request, you can safely ignore this '
                'email.',
        to=[email_address])
    print(f'email send count: {em.send()}')
