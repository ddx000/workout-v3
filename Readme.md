## workout-v3

tech stack

- connexion + flask + swagger as framework
- Google login SDK + JWT extension
- flask-admin
- pytest

## how to setup develop env

install python3.7  
https://www.python.org/downloads/release/python-379/  

pipenv install --skip-lock  
pipenv run python -m conf.build_database  

## How to run it

pipenv run python -m server or  
pipenv run python server.py  


## useful page

test JWT token
```eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJjb20uemFsYW5kby5jb25uZXhpb24iLCJpYXQiOjE2MjcxOTkzMTUsImV4cCI6MTAwMDAwMDAwMTYyNzE5OTMxNSwic3ViIjoiMSJ9.CF0FOEpnZpHHH7SBflQ8q-BPGe-He8nvihhPgozf3Xs```

http://localhost:5500/login_example.html  
http://localhost:5000/admin/  
http://localhost:5000/api/ui/  

## Note

https://www.cnblogs.com/xueweihan/p/5118222.html  

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

## RECORD[Not implement]

GET /menus/{menu_id}/actions/{action_id}/records: return all records under an action  
POST /menus/{menu_id}/actions/{action_id}/records: create a record with a action  
GET /menus/{menu_id}/actions/{action_id}/records/{record_id}: get a record under a action  
PUT /menus/{menu_id}/actions/{action_id}/records/{record_id}: update a record under a action  
DELETE /menus/{menu_id}/actions/{action_id}/records/{record_id}: delete a record under a action  

## USER[Not implement]  

GET /users/info: return current user info  
