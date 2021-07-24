

from models.models import User, Menu, Action, ActionSchema
from flask import make_response, abort, jsonify
from config import db


def read_all():
    """
    This function responds to a request for /api/menu/actions
    with the complete list of actions, sorted by action timestamp

    :return:                json list of all actions for all menu
    """
    # Query the database for all the actions
    actions = Action.query.order_by(db.desc(Action.timestamp)).all()

    action_schema = ActionSchema(many=True)
    data = action_schema.dump(actions).data

    return data


def read_one(menu_id, action_id):
    """
    This function responds to a request for
    /api/menu/{menu_id}/actions/{action_id}
    with one matching action for the associated menu

    :param menu_id:       Id of menu the action is related to
    :param action_id:         Id of the action
    :return:                json string of action contents
    """
    # Query the database for the action
    action = (
        Action.query.join(Menu, Menu.menu_id == Action.menu_id)
        .filter(Menu.menu_id == menu_id)
        .filter(Action.action_id == action_id)
        .one_or_none()
    )

    # Was a action found?
    if action is not None:
        return jsonify(action)

    # Otherwise, nope, didn't find that action
    else:
        abort(404, f"Action not found for Id: {action_id}")


def create(menu_id, action):
    """
    This function creates a new action related to the passed in menu id.

    :param menu_id:       Id of the menu the action is related to
    :param action:            The JSON containing the action data
    :return:                201 on success
    """
    # get the parent menu
    menu = Menu.query.filter(Menu.menu_id == menu_id).one_or_none()

    # Was a menu found?
    if menu is None:
        abort(404, f"Menu not found for Id: {menu_id}")

    new_menu = Action(menu_id=menu_id, content=action)

    db.session.add(new_menu)
    db.session.commit()

    return jsonify(new_menu), 201


def update(menu_id, action_id, action):
    """
    This function updates an existing action related to the passed in
    menu id.

    :param menu_id:       Id of the menu the action is related to
    :param action_id:         Id of the action to update
    :param content:            The JSON containing the action data
    :return:                200 on success
    """
    update_action = (
        Action.query.filter(Menu.menu_id == menu_id)
        .filter(Action.action_id == action_id)
        .one_or_none()
    )

    # Did we find an existing action?
    if update_action is not None:

        # Set the id's to the action we want to update
        update.menu_id = update_action.menu_id
        update.action_id = update_action.action_id

        # merge the new object into the old and commit it to the db
        db.session.merge(update)
        db.session.commit()

        # return updated action in the response

        return data, 200

    # Otherwise, nope, didn't find that action
    else:
        abort(404, f"Action not found for Id: {action_id}")


def delete(menu_id, action_id):
    """
    This function deletes a action from the action structure

    :param menu_id:   Id of the menu the action is related to
    :param action_id:     Id of the action to delete
    :return:            200 on successful delete, 404 if not found
    """
    # Get the action requested
    action = (
        Action.query.filter(Menu.menu_id == menu_id)
        .filter(Action.action_id == action_id)
        .one_or_none()
    )

    # did we find a action?
    if action is not None:
        db.session.delete(action)
        db.session.commit()
        return make_response(
            "Action {action_id} deleted".format(action_id=action_id), 200
        )

    # Otherwise, nope, didn't find that action
    else:
        abort(404, f"Action not found for Id: {action_id}")
