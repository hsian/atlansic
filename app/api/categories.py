from flask import jsonify, request, g, current_app, url_for
from sqlalchemy import or_,and_
from . import api
from ..errors import bad_request
from ..models import Category, Post
from ..decorators import admin_required
from .authorization import auth
from .. import db

# @desc 新增栏目
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

# @desc 编辑栏目
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

# @desc 所有栏目
@api.route('/categories/')
def get_categories():
    categories = Category.query.filter(
        and_(Category.level == 1, Category.enable == True)).all()
    return  jsonify({
        'categories': [category.to_json() for category in categories]
    })

# @desc 指定栏目下的子栏目
@api.route('/categories/<int:id>')
def get_categories_by_id(id):
    categories = Category.query.filter(
        and_(Category.id == id, Category.enable == True)).all()
    return  jsonify({
        'categories': [category.to_json() for category in categories]
    })

# @desc 栏目下的文章
@api.route('/category_posts/<int:id>')
def get_category_posts(id):
    category = Category.query.get_or_404(id)
    if category is None or category.enable == None or category.enable == False:
        return bad_request("栏目不存在或已关闭")
    page = request.args.get('page', 1, type=int)
    pagination = Post.query.filter(
        and_(Post.enable == True, Post.category_id == id)).paginate(
        page, per_page=current_app.config['PER_PAGE'],
        error_out=False)
    posts = pagination.items
    prev = None
    if pagination.has_prev:
        prev = url_for('api.get_category_posts', id=id, page=page-1)
    next = None
    if pagination.has_next:
        next = url_for('api.get_category_posts', id=id, page=page+1)
    return jsonify({
        'posts': [post.to_json() for post in posts],
        'prev': prev,
        'next': next,
        'count': pagination.total
    })