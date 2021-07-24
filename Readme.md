## workout-v3

tech stack

- connexion + flask + swagger as framework
- Google login SDK + JWT extension
- flask-admin
- pytest

## How to run it

pipenv run python server.py

## Menu

GET /menus: get all menus for an user
POST /menus: create a menu for an user
GET /menus/{menu_id}: get a menu for an user
PUT /menus/{menu_id}: update a menu (not actions) for an user
DELETE /menus/{menu_id} for an user

## Action

GET /menus/{menu_id}/actions: get all actions under a menu
POST /menus/{menu_id}/actions: create a action with a menu
GET /menus/{menu_id}/actions/{action_id}: get a action under a menu
PUT /menus/{menu_id}/actions/{action_id}: update a action with a menu
DELETE /menus/{menu_id}/actions/{action_id}: delete a action with a menu

## RECORD

GET /menus/{menu_id}/actions/{action_id}/records: return all records under an action
POST /menus/{menu_id}/actions/{action_id}/records: create a record with a action
GET /menus/{menu_id}/actions/{action_id}/records/{record_id}: get a record under a action
PUT /menus/{menu_id}/actions/{action_id}/records/{record_id}: update a record under a action
DELETE /menus/{menu_id}/actions/{action_id}/records/{record_id}: delete a record under a action

## USER

GET /users/info: return current user info
