7/19 menu
7/21 action
7/22 record

for each user

## Menu

GET /menus: get all menus
POST /menus: create a menu

GET /menus/{menu_id}: get a menu
PUT /menus/{menu_id}: update a menu (not actions)
DELETE /menus/{menu_id}

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

GET

- Record

- flask
- connexion
- swagger (api first)
- oauth
- jwt_token
- api_protect
- flask-login
- flask-admin
- pytest
- file-structure
