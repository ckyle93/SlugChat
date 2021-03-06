# Helper functions for interacting with login

# Get the user model so we can return it in logged_in
from home.models import User
# Run pip install --upgrade google-api-python-client
# to get the oath2client
from oauth2client import client, crypt


class QuizObj(object):

    def __init__(self):
        self.id = -1
        self.question_text = 'N/A'
        self.choices = []


# (Receive token by HTTPS POST)
def verify_user(token):
    # Open google key file
    try:
        with open('key_file.txt', 'r') as f:
            CLIENT_ID = f.read().rstrip()
    except IOError:
        CLIENT_ID = None
        print("key_file not found. \nMessage Ckyle for key_file.txt")

    try:
        idinfo = client.verify_id_token(token, CLIENT_ID)
        # If multiple clients access the backend server:
        if idinfo['aud'] != CLIENT_ID:
            raise crypt.AppIdentityError("Unrecognized client.")
        if idinfo['iss'] not in ['accounts.google.com',
                                 'https://accounts.google.com']:
            raise crypt.AppIdentityError("Wrong issuer.")
    except crypt.AppIdentityError as error:
        # Invalid token
        return {'error': error}

    return idinfo


# If the user is logged in, return the corresponsing User model
def logged_in(request):
    if 'user' in request.session:
        return User.objects.get(userID=request.session['user'])
    else:
        return None
