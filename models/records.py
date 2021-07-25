

from models.models import User, Action, Record, RecordSchema
from flask import make_response, abort
from conf.config import db


def read_all_records_in_action(user, action_id):
    records = Record.query.filter(Record.action_id == action_id).order_by(
        db.desc(Record._last_modified)).all()
    record_schema = RecordSchema(many=True)
    data = record_schema.dump(records).data
    return data


def read_one(user, action_id, record_id):
    record = (
        Record.query.filter(Record.action_id == action_id)
        .filter(Record.record_id == record_id)
        .one_or_none()
    )
    # Was a record found?
    if record is not None:
        record_schema = RecordSchema(many=False)
        data = record_schema.dump(record).data
        return data

    # Otherwise, nope, didn't find that record
    else:
        abort(404, f"Record not found for Id: {record_id}")


def create(user, action_id, record):

    # TODO User validation

    action = Action.query.filter(Action.action_id == action_id).one_or_none()

    # Was a action found?
    if action is None:
        abort(404, f"Action not found for Id: {action_id}")

    schema = RecordSchema()
    print("record passed in ", record)
    new_re = schema.load(record, session=db.session).data

    print(new_re)

    #new_record = Record(action_id=action_id, content=record.get('content'))

    db.session.add(new_re)
    db.session.commit()

    record_schema = RecordSchema(many=False)
    data = record_schema.dump(new_record).data

    return data, 201


def update(user, action_id, record_id, record):

    update_record = (
        Record.query.filter(Action.action_id == action_id)
        .filter(Record.record_id == record_id)
        .one_or_none()
    )

    # Did we find an existing record?
    if update_record is not None:
        # Set the id's to the record we want to update
        schema = RecordSchema()
        print("record passed in ", record)

        update = schema.load(record, session=db.session).data
        update.action_id = update_record.action_id
        update.record_id = update_record.record_id
        print("update_record", update)

        # merge the new object into the old and commit it to the db
        db.session.merge(update)
        db.session.commit()

        data = schema.dump(update).data
        # return updated record in the response

        return data, 200

    # Otherwise, nope, didn't find that record
    else:
        abort(404, f"Record not found for Id: {record_id}")


def delete(user, action_id, record_id):

    record = (
        Record.query.filter(Action.action_id == action_id)
        .filter(Record.record_id == record_id)
        .one_or_none()
    )

    # did we find a record?
    if record is not None:
        db.session.delete(record)
        db.session.commit()
        return make_response(
            "Record {record_id} deleted".format(record_id=record_id), 200
        )

    # Otherwise, nope, didn't find that record
    else:
        abort(404, f"Record not found for Id: {record_id}")
