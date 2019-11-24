from flask import g, url_for
from datetime import datetime
from .. import db
from .permissions import Permission

class Level:
    ALL = 1 # 系统通知
    ADMIN = 2 # 管理员信息
    PRIVATE = 3 # 普通信息

class Message(db.Model):
    __tablename__ = 'messages'
    id = db.Column(db.Integer, primary_key=True)
    level = db.Column(db.Integer)
    sender_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    receiver_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    title = db.Column(db.String(256))
    content = db.Column(db.Text)
    expire = db.Column(db.Boolean, default=False) # 过期
    read = db.Column(db.Boolean, default=False) # 已读
    public = db.Column(db.Boolean, default=False) # 系统通知

    def __init__(self, **kwargs):
        super(Message, self).__init__(**kwargs)
        if self.sender.can(Permission.ADMIN) and self.public == True:
            self.level = Level.ALL
        elif self.sender.can(Permission.ADMIN) and self.public == False:
            self.level = Level.ADMIN
        else:
            self.level = Level.PRIVATE

    def __repr__(self):
        return '<Message %r>' % self.title

    def to_json(self):
        json_message = {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'sender_url': url_for('api.get_user', id=self.sender_id),
            'sender': self.sender.to_json(),
            'expire': self.expire,
            'read': self.read,
            'public': self.public,
            'timestamp': self.timestamp,
            'url': url_for('api.get_message', id=self.id)
        }

        if self.receiver_id:
            json_message['receiver_url'] = url_for('api.get_user', id=self.receiver_id)
            json_message['receiver'] = self.receiver.to_json()

        return json_message
    