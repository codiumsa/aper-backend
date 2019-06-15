from aper import login_manager, app
from .models import User
from .db import db_session
from google.oauth2 import id_token
from google.auth.transport import requests
import json


@login_manager.request_loader
def load_user(request):
    token = request.headers.get('Authorization')

    dummy_info = ''' {
        "iss": "https://accounts.google.com",
        "sub": "110169484474386276334",
        "azp": "1008719970978-hb24n2dstb40o45d4feuo2ukqmcc6381.apps.googleusercontent.com",
        "aud": "1008719970978-hb24n2dstb40o45d4feuo2ukqmcc6381.apps.googleusercontent.com",
        "iat": "1433978353",
        "exp": "1433981953",
        "email": "testuser@gmail.com",
        "email_verified": "true",
        "name" : "Test User",
        "picture": "https://lh4.googleusercontent.com/-kYgzyAWpZzJ/ABCDEFGHI/AAAJKLMNOP/tIXL9Ir44LE/s99-c/photo.jpg",
        "given_name": "Test",
        "family_name": "User",
        "locale": "en"
        }'''

    try:
        # Specify the CLIENT_ID of the app that accesses the backend:
        idinfo = id_token.verify_oauth2_token(token, requests.Request(),
                                              app.config['GOOGLE_CLIENT_ID'])

        #idinfo = json.loads(dummy_info)

        # Or, if multiple clients access the backend server:
        # idinfo = id_token.verify_oauth2_token(token, requests.Request())
        # if idinfo['aud'] not in [CLIENT_ID_1, CLIENT_ID_2, CLIENT_ID_3]:
        #     raise ValueError('Could not verify audience.')

        if idinfo['iss'] not in [
                'accounts.google.com', 'https://accounts.google.com'
        ]:
            raise ValueError('Wrong issuer.')

        # If auth request is from a G Suite domain:
        # if idinfo['hd'] != GSUITE_DOMAIN_NAME:
        #     raise ValueError('Wrong hosted domain.')

        # ID token is valid. Get the user's Google Account ID from the decoded token.
        user = User.query.filter(User.email == idinfo['email']).first()
        if not user:
            user = User(idinfo['name'], idinfo['email'])
            db_session.add(user)
            db_session.commit()
        return user
    except ValueError:
        # Invalid token
        return None
