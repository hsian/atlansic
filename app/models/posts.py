from datetime import datetime
from flask import jsonify
from .. import db
from app.exceptions import ValidationError

class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(256))
    body = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    enable = db.Column(db.Boolean, default=True)
    comments = db.relationship('Comment', backref='post', lazy='dynamic')

    def __repr__(self):
        return '<Post %r>' % self.title

    def to_json(self):
        json_post = {
            'id': self.id,
            'title': self.title,
            'body': self.body,
            'timestamp': self.timestamp,
            'author': self.author.to_json(),
            'category': self.category.to_json(),
            'tags': [tag.to_json() for tag in self.tags],
            'enable': self.enable
        }
        return json_post