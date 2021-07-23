'''
Basic example of a resource server
'''

from google.auth.transport import requests as google_requests
from google.oauth2 import id_token

import time
import json
import connexion
import requests
from config import connex_app
from jose import JWTError, jwt
from werkzeug.exceptions import Unauthorized

JWT_ISSUER = 'com.zalando.connexion'
JWT_SECRET = 'change_this'
JWT_LIFETIME_SECONDS = 100
JWT_ALGORITHM = 'HS256'


with open("key.json", "r") as f:
    key = json.load(f)
    GOOGLE_OAUTH2_CLIENT_ID = key["GOOGLE_OAUTH2_CLIENT_ID"]


# @connex_app.route("/auth/google_sign_in", methods=["OPTIONS"])
# def handle_cors():
#     return "", 200


def google_sign_in():
    print("called")
    # frontend user authorized and send a token(authtoken) here

    req_json = connexion.request.json

    token = req_json['id_token']
    try:
        id_info = id_token.verify_oauth2_token(
            token,
            google_requests.Request(),
            GOOGLE_OAUTH2_CLIENT_ID
        )
        # use this token and client_id to get more detailed info in backend

        print(id_info)
        if id_info['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
            raise ValueError('Wrong issuer.')

        create_user_by_googleoauth(id_info)

        USER_ID = 1

        token = generate_token(USER_ID)

    except ValueError:
        # Invalid token
        raise ValueError('Invalid token')
    print('登入成功')

    return token, 200


def create_user_by_googleoauth(userinfo_response):
    if userinfo_response.get("email_verified"):
        unique_id = userinfo_response["sub"]
        users_email = userinfo_response["email"]
        picture = userinfo_response["picture"]
        users_name = userinfo_response["given_name"]
    else:
        print("User email not available or not verified by Google.")

    print("try to create a model")
    # create a model
    # user = User(
    #     id_=unique_id, name=users_name, email=users_email, profile_pic=picture
    # )

    # # Doesn't exist? Add to database
    # if not User.get(unique_id):
    #     User.create(unique_id, users_name, users_email, picture)


def generate_token(user_id):
    timestamp = _current_timestamp()
    payload = {
        "iss": JWT_ISSUER,
        "iat": int(timestamp),
        "exp": int(timestamp + JWT_LIFETIME_SECONDS),
        "sub": str(user_id),
    }

    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)


def decode_token(token, required_scopes=None):
    try:
        return jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
    except JWTError as e:
        raise Unauthorized from e


def get_secret(user, token_info) -> str:
    return '''
    You are user_id {user} and the secret is 'wbevuec'.
    Decoded token claims: {token_info}.
    '''.format(user=user, token_info=token_info)


def _current_timestamp() -> int:
    return int(time.time())
