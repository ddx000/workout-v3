'''
Basic example of a resource server
'''

from google.auth.transport import requests as google_requests
from google.oauth2 import id_token

import time
import json
import connexion
import requests
from jose import JWTError, jwt
from werkzeug.exceptions import Unauthorized


from models.models import User
from conf.config import db


JWT_ISSUER = 'com.zalando.connexion'
JWT_SECRET = 'change_this'
# TODO change secret and put in env
JWT_LIFETIME_SECONDS = 86400
JWT_ALGORITHM = 'HS256'


with open("./conf/key.json", "r") as f:
    key = json.load(f)
    GOOGLE_OAUTH2_CLIENT_ID = key["GOOGLE_OAUTH2_CLIENT_ID"]


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

        # create user in db
        user_id = create_user_by_googleoauth(id_info)
        # issue jwt token for that user
        token = generate_token(user_id)

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
    print(unique_id, users_email, picture, users_name)

    # prevent overflow in sqlite
    user_id = int(unique_id[-8:])

    # # Doesn't exist? Add to database
    existing_user = (
        User.query.filter(User.user_id == user_id)
        .one_or_none()
    )

    if existing_user:
        print("user already exist")
        return

    # create a model
    new_user = User(
        user_id=user_id, name=users_name, email=users_email, profile_pic=picture
    )
    db.session.add(new_user)
    db.session.commit()

    return user_id


def generate_token(user_id):
    timestamp = int(time.time())
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
