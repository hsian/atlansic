from flask import url_for
from datetime import datetime
from .. import db
from app.exceptions import ValidationError
from flask import jsonify

class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    enable = db.Column(db.Boolean, default=True)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))
    parent_id = db.Column(db.Integer, db.ForeignKey('comments.id'))
    chilren = db.relationship('Comment')
    level = db.Column(db.Integer)

    def __init__(self, **kwargs):
        super(Comment, self).__init__(**kwargs)
        if self.parent_id is None or self.parent_id == '':
            self.level = 1
        else:
            parent = Comment.query.filter_by(id=self.parent_id).first()
            if parent is None:
                raise ValidationError('父类不存在')
            self.level = parent.level + 1

    def __repr__(self):
        return '<Comment %r>' % self.body

    def to_json(self):
        json_comment = {
            'id': self.id,
            'body': self.body,
            'timestamp': self.timestamp,
            'enable': self.enable,
            'author': self.author.to_json(),
            'post_id': self.post.to_json()['id'],
            'post_title': self.post.to_json()['title'],
            'children': [comment.to_json() for comment in self.chilren],
            'level': self.level
        }
        return json_comment