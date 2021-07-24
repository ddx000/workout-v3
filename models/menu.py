"""
This is the menu module and supports all the REST actions for the
menu data
"""

from flask import make_response, abort, jsonify
from conf.config import db
from models.models import User, Menu, Action, MenuSchema
import connexion


def read_all(user, token_info):
    """
    This function responds to a request for /api/menu
    with the complete lists of menu

    :return:        json string of list of menu
    """

    print("USer is ", user)
    # Create the list of menu from our data
    menus = Menu.query.order_by(Menu.menu_id).all()

    # Serialize the data for the response
    menu_schema = MenuSchema(many=True)
    data = menu_schema.dump(menus).data

    return data, 200


def read_one(menu_id, user):
    """
    This function responds to a request for /api/menu/{menu_id}
    with one matching menu from menu

    :param menu_id:   Id of menu to find
    :return:            menu matching id
    """
    print("user is", user)
    # Build the initial query
    menu = (
        Menu.query.filter(Menu.menu_id == menu_id)
        .outerjoin(Action)
        .one_or_none()
    )

    # Did we find a menu?
    if menu is not None:
        # Serialize the data for the response
        menu_schema = MenuSchema(many=False)
        data = menu_schema.dump(menu).data

        return data, 200

    # Otherwise, nope, didn't find that menu
    else:
        abort(404, f"Menu not found for Id: {menu_id}")


def create(menu):
    """
    This function creates a new menu in the menu structure
    based on the passed in menu data

    :param menu:  menu to create in menu structure
    :return:        201 on success, 406 on menu exists
    """

    # user_id = menu.get("user_id")
    # user = User.query.filter(User.user_id == user_id).one_or_none()
    # # Was a person found?
    # if user is None:
    #     abort(404, f"user not found for Id: {user_id}")

    user_id = 1  # hard-code for user

    name = menu.get("name")

    existing_menu = (
        Menu.query.filter(Menu.name == name)
        .one_or_none()
    )

    # Can we insert this menu?
    if existing_menu is None:
        # Add the menu to the database
        new_menu = Menu(name=name, user_id=user_id)

        db.session.add(new_menu)
        db.session.commit()

        menu_schema = MenuSchema(many=False)
        data = menu_schema.dump(new_menu).data

        return data, 201

        return jsonify({'success': True}), 201

    # Otherwise, nope, menu exists already
    else:
        abort(409, f"Menu {name} exists already")


def update(menu_id, menu):

    # Get the menu requested from the db into session
    update_menu = Menu.query.filter(
        Menu.menu_id == menu_id
    ).one_or_none()

    # Did we find an existing menu?
    if update_menu is not None:

        # turn the passed in menu into a db object
        schema = MenuSchema()
        update = schema.load(menu, session=db.session).data

        # Set the id to the menu we want to update
        update.menu_id = update_menu.menu_id

        # merge the new object into the old and commit it to the db
        db.session.merge(update)
        db.session.commit()

        # return updated menu in the response
        data = schema.dump(update_menu).data

        return data, 200

    # Otherwise, nope, didn't find that menu
    else:
        abort(404, f"Menu not found for Id: {menu_id}")


def delete(menu_id):
    """
    This function deletes a menu from the menu structure

    :param menu_id:   Id of the menu to delete
    :return:            200 on successful delete, 404 if not found
    """
    # Get the menu requested
    menu = Menu.query.filter(Menu.menu_id == menu_id).one_or_none()

    # Did we find a menu?
    if menu is not None:
        db.session.delete(menu)
        db.session.commit()
        return make_response(f"Menu {menu_id} deleted", 200)

    # Otherwise, nope, didn't find that menu
    else:
        abort(404, f"Menu not found for Id: {menu_id}")
