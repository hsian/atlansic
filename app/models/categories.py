from datetime import datetime
from .. import db
from app.exceptions import ValidationError
from flask import jsonify

class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, index=True)
    summary =  db.Column(db.Text())
    level = db.Column(db.Integer)
    parent_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    chilren = db.relationship('Category')
    enable = db.Column(db.Boolean, default=True)
    posts = db.relationship('Post', backref='category', lazy='dynamic')
    public = db.Column(db.Boolean, default=True)

    def __init__(self, **kwargs):
        super(Category, self).__init__(**kwargs)
        if self.parent_id is None or self.parent_id == '':
            self.level = 1
        else:
            parent = Category.query.filter_by(id=self.parent_id).first()
            if parent is None:
                raise ValidationError('父类不存在')
            self.level = parent.level + 1

    def __repr__(self):
        return '<Category %r>' % self.name

    @staticmethod
    def is_public(cid):
        category = Category.query.filter_by(id=cid).first()
        if category is None:
            raise ValidationError('类目不存在')
        return category.public

    def to_json(self):
        json_categories = {
            'id': self.id,
            'name': self.name,
            'summary': self.summary,
            'level': self.level,
            'children': [category.to_json() for category in self.chilren],
            'enable': self.enable
        }
        return json_categories
