import os
from conf.config import db
from models.models import User, Menu, Action, Record

if os.path.exists("./conf/testsqlite.db"):
    os.remove("./conf/testsqlite.db")


# Create the database
db.create_all()

lst = [
    User(user_id=1, name='jimmy',
         email='jimmy@example.com'),
    User(user_id=2, name='allen',
         email='allen@example.com'),
    Menu(menu_id=2, user_id=1, name="平日菜單"),
    Menu(menu_id=3, user_id=1, name="假日菜單"),
    Menu(menu_id=4, user_id=2, name="user2菜單"),
    Action(action_id=3, menu_id=2, content='握推32*12下*2組(計畫)'),
    Action(action_id=4, menu_id=3, content='深蹲15*20下*3組(計畫)'),
    Record(action_id=3, weight=32, reps=12),
    Record(action_id=3, weight=32, reps=11),
    Record(action_id=4, weight=15, reps=20),
    Record(action_id=4, weight=14, reps=19),
]

for i in lst:
    db.session.add(i)
db.session.commit()
