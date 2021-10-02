

from models.models import User, Menu, Action, ActionSchema
from flask import make_response, abort, jsonify
from conf.config import db


def read_all_actions_in_menu(user, menu_id):
    """
    This function responds to a request for /api/menu/actions
    with the complete list of actions, sorted by action timestamp

    :return:                json list of all actions for all menu
    """

    print("##called", user, menu_id)

    # TODO user validation

    # Query the database for all the actions
    actions = Action.query.filter(Action.menu_id == menu_id).order_by(
        db.desc(Action._last_modified)).all()

    action_schema = ActionSchema(many=True)
    data = action_schema.dump(actions).data

    return data


def read_one(user, menu_id, action_id):
    """
    This function responds to a request for
    /api/menu/{menu_id}/actions/{action_id}
    with one matching action for the associated menu

    :param menu_id:       Id of menu the action is related to
    :param action_id:         Id of the action
    :return:                json string of action contents
    """

    # TODO user validation

    action = (
        Action.query.filter(Action.menu_id == menu_id)
        .filter(Action.action_id == action_id)
        .one_or_none()
    )

    # old one
    # Query the database for the action
    # action = (
    #     Action.query.join(Menu, Menu.menu_id == Action.menu_id)
    #     .filter(Menu.menu_id == menu_id)
    #     .filter(Action.action_id == action_id)
    #     .one_or_none()
    # )

    # Was a action found?
    if action is not None:
        action_schema = ActionSchema(many=False)
        data = action_schema.dump(action).data
        return data

    # Otherwise, nope, didn't find that action
    else:
        abort(404, f"Action not found for Id: {action_id}")


def create(user, menu_id, action):
    """
    This function creates a new action related to the passed in menu id.

    :param menu_id:       Id of the menu the action is related to
    :param action:            The JSON containing the action data
    :return:                201 on success
    """
    # get the parent menu
    menu = Menu.query.filter(Menu.menu_id == menu_id,
                             Menu.user_id == user).one_or_none()

    # Was a menu found?
    if menu is None:
        abort(404, f"Menu not found for Id: {menu_id}")

    new_action = Action(menu_id=menu_id, content=action.get('content'))

    db.session.add(new_action)
    db.session.commit()

    action_schema = ActionSchema(many=False)
    data = action_schema.dump(new_action).data

    return data, 201


def update(user, menu_id, action_id, action):
    """
    not implement yet
    """
    update_action = (
        Action.query.filter(Menu.menu_id == menu_id)
        .filter(Action.action_id == action_id)
        .one_or_none()
    )

    # Did we find an existing action?
    if update_action is not None:

        # Set the id's to the action we want to update

        schema = ActionSchema()

        print("action passed in ", action)

        update = schema.load(action, session=db.session).data

        update.menu_id = update_action.menu_id
        update.action_id = update_action.action_id

        print("update_action", update)

        # merge the new object into the old and commit it to the db
        db.session.merge(update)
        db.session.commit()

        data = schema.dump(update).data
        # return updated action in the response

        return data, 200

    # Otherwise, nope, didn't find that action
    else:
        abort(404, f"Action not found for Id: {action_id}")


def delete(user, menu_id, action_id):
    """
    not implement yet
    """
    # Get the action requested
    action = (
        Action.query.filter(Menu.menu_id == menu_id)
        .filter(Action.action_id == action_id)
        .one_or_none()
    )

    res = {'resource': "Action", "action": "Delete", "resource_id": action_id}

    # did we find a action?
    if action is not None:
        db.session.delete(action)
        db.session.commit()

        res['result'] = 'Success'
        return make_response(jsonify(res), 200)

    # Otherwise, nope, didn't find that action
    else:

        res['result'] = 'Not Found'

        return make_response(jsonify(res), 404)
