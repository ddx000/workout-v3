from models.models import User
from flask import abort


def get_user(user):
    """hard code for now"""

    # Build the initial query
    user = (
        User.query.filter(User.user_id == user)
        .one_or_none()
    )

    # Did we find a menu?
    if user is not None:
        return {"user_name": user.name, "user_email": user.email, "profile_pic": user.profile_pic}, 200

    # Otherwise, nope, didn't find that menu
    else:
        abort(404, f"User not found for Id: {user}")
