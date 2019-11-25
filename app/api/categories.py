from flask import jsonify, request, g, current_app, url_for
from sqlalchemy import or_,and_
from . import api
from ..errors import bad_request
from ..models import Category
from ..decorators import admin_required
from .authorization import auth
from .. import db

@api.route('/new_category/', methods=['POST'])
@auth.login_required
@admin_required
def new_category():
    try:
        form = request.json
        name, summary, parent_id = form['name'], form.get('summary'), \
            form.get('parent_id')
        
        category = Category(
            name = name,
            summary = summary,
            parent_id = parent_id
        )
        db.session.add(category)
        db.session.commit()
        return jsonify({
            'message': '添加成功'
        })
    
    except Exception as e:
        return bad_request('错误原因：%s' % repr(e))


@api.route('/edit_category/<int:id>', methods=['POST'])
@auth.login_required
@admin_required
def edit_category(id):
    try:
        form = request.json
        category = Category.query.get_or_404(id)
        category.name = form.get('name', category.name)
        category.summary = form.get('summary', category.summary)
        category.enable = form.get('enable', category.enable)
        category.public = form.get('public', category.public)
        # category.parent_id = parent_id or category.parent_id # 要修改可以去掉level层级
        db.session.add(category)
        db.session.commit()
        return jsonify({
            'message': '编辑成功'
        })
    except Exception as e:
        return bad_request('错误原因：%s' % repr(e))


@api.route('/categories/')
def get_categories():
    categories = Category.query.filter(
        and_(Category.level == 1, Category.enable == True)).all()
    return  jsonify({
        'categories': [category.to_json() for category in categories]
    })