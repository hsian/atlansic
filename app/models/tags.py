from flask import url_for
from datetime import datetime
from .. import db
from app.exceptions import ValidationError
from flask import jsonify

tag_post_relation = db.Table('tag_post_relation',
    db.Column('tag_id', db.Integer, db.ForeignKey('tags.id')),
    db.Column('post_id', db.Integer, db.ForeignKey('posts.id'))
)

class Tag(db.Model):
    __tablename__ = 'tags'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, index=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    posts = db.relationship('Post',
        secondary=tag_post_relation,
        backref=db.backref('tags', lazy='dynamic'),
        lazy='dynamic')

    def to_json(self):
        json_tags = {
            'id': self.id,
            'name': self.name,
            'timestamp': self.timestamp,
            # 'url': url_for('api.get_tag_posts', id=self.id)
        }
        return json_tags