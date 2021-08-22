from datetime import datetime
from conf.config import db, ma, admin
from marshmallow import fields
from flask_admin.contrib.sqla import ModelView


class User(db.Model):
    __tablename__ = "user"
    user_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32))
    email = db.Column(db.String(32))
    profile_pic = db.Column(db.String(256))
    _last_modified = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )
    menus = db.relationship(
        "Menu",
        backref="User",
        cascade="all, delete, delete-orphan",
        single_parent=True,
        order_by="desc(Menu._last_modified)",
    )


class Menu(db.Model):
    __tablename__ = "menu"
    menu_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32))
    plan_time = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey("user.user_id"))

    _last_modified = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )
    actions = db.relationship(
        "Action",
        backref="Menu",
        cascade="all, delete, delete-orphan",
        single_parent=True,
        order_by="desc(Action._last_modified)",
    )


class Action(db.Model):
    __tablename__ = "action"
    action_id = db.Column(db.Integer, primary_key=True)
    menu_id = db.Column(db.Integer, db.ForeignKey("menu.menu_id"))
    content = db.Column(db.String, nullable=False)
    _last_modified = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )
    records = db.relationship(
        "Record",
        backref="Action",
        cascade="all, delete, delete-orphan",
        single_parent=True,
        order_by="desc(Record._last_modified)",
    )


class Record(db.Model):
    __tablename__ = "record"
    record_id = db.Column(db.Integer, primary_key=True)
    action_id = db.Column(db.Integer, db.ForeignKey("action.action_id"))
    weight = db.Column(db.Integer)
    reps = db.Column(db.Integer)
    _last_modified = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )


class MenuSchema(ma.ModelSchema):
    def __init__(self, **kwargs):
        super().__init__(strict=True, **kwargs)

    class Meta:
        model = Menu
        sqla_session = db.session

    actions = fields.Nested("MenuActionSchema", default=[], many=True)


class MenuActionSchema(ma.ModelSchema):
    def __init__(self, **kwargs):
        super().__init__(strict=True, **kwargs)

    action_id = fields.Int()
    menu_id = fields.Int()
    content = fields.Str()
    _last_modified = fields.Str()
    records = fields.Nested("RecordSchema", default=[], many=True)


class ActionSchema(ma.ModelSchema):
    def __init__(self, **kwargs):
        super().__init__(strict=True, **kwargs)

    class Meta:
        model = Action
        sqla_session = db.session

    records = fields.Nested("RecordSchema", default=[], many=True)


class ActionMenuSchema(ma.ModelSchema):
    """
    This class exists to get around a recursion issue
    """

    def __init__(self, **kwargs):
        super().__init__(strict=True, **kwargs)

    menu_id = fields.Int()
    user_id = fields.Int()
    name = fields.Str()
    _last_modified = fields.Str()


class RecordSchema(ma.ModelSchema):
    def __init__(self, **kwargs):
        super().__init__(strict=True, **kwargs)

    class Meta:
        model = Record
        sqla_session = db.session


admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Menu, db.session))
admin.add_view(ModelView(Action, db.session))
admin.add_view(ModelView(Record, db.session))
