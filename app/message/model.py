from flask import g
from datetime import datetime
from app.exceptions import ValidationError
from .. import db
from ..user.model import User, Role, Permission

class Level:
    ALL = 1
    ADMIN = 2
    PRIVATE = 3

class Message(db.Model):
    __tablename__ = 'messages'
    id = db.Column(db.Integer, primary_key=True)
    level = db.Column(db.Integer)
    sender_id = db.Column(db.Integer, db.ForeignKey('users.id'),primary_key=True)
    receiver_id = db.Column(db.Integer, db.ForeignKey('users.id'),primary_key=True)   
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    title = db.Column(db.String(256))
    content = db.Column(db.Text)
    expire = db.Column(db.Boolean, default=False)
    read = db.Column(db.Boolean, default=False)


    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)

    def __repr__(self):
        return '<User %r>' % self.title

    @staticmethod
    def from_json(json_message):
        content = json_message.get('content')
        if content is None or content == '':
            raise ValidationError('内容不能为空')
        return Message(**json_message)

    