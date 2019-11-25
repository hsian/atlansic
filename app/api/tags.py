from flask import jsonify, request, current_app, url_for
from ..models import Tag
from .authorization import auth
from . import api
from .. import db
from ..decorators import admin_required
from ..errors import bad_request

@api.route('/new_tag/', methods=['POST'])
@auth.login_required
@admin_required
def new_tag():
    try:
        name = request.json['name']
        tag = Tag(
            name = name
        )
        db.session.add(tag)
        db.session.commit()
        return jsonify({
            'message': '添加成功',
            'data': tag.to_json()
        })

    except Exception as e:
        return bad_request('错误原因：%s' % repr(e)) 

@api.route('/edit_tag/<int:id>', methods=['POST'])
@auth.login_required
@admin_required
def edit_tag(id):
    try:
        tag = Tag.query.get_or_404(id)
        if tag is None:
            return bad_request('标签不存在')
        tag.name = request.json.get('name', tag.name)
        db.session.add(tag)
        db.session.commit()
        return jsonify({
            'message': '编辑成功',
            'data': tag.to_json()
        })

    except Exception as e:
        return bad_request('错误原因：%s' % repr(e)) 

@api.route('/tags/')
def get_tags():
    page = request.args.get('page', 1, type=int)
    pagination = Tag.query.paginate(
        page, per_page=current_app.config['PER_PAGE'],
        error_out=False)
    tags = pagination.items
    prev = None
    if pagination.has_prev:
        prev = url_for('api.get_tags', page=page-1)
    next = None
    if pagination.has_next:
        next = url_for('api.get_tags', page=page+1)
    return jsonify({
        'tags': [tag.to_json() for tag in tags],
        'prev': prev,
        'next': next,
        'count': pagination.total
    })   

@api.route('/tag_posts/<int:id>')
def get_tag_posts(id):
    tag = Tag.query.get_or_404(id)
    if tag is None:
        return bad_request("标签不存在")
    page = request.args.get('page', 1, type=int)
    pagination = tag.posts.paginate(
        page, per_page=current_app.config['PER_PAGE'],
        error_out=False)
    posts = pagination.items
    prev = None
    if pagination.has_prev:
        prev = url_for('api.get_tag_posts', id=id, page=page-1)
    next = None
    if pagination.has_next:
        next = url_for('api.get_tag_posts', id=id, page=page+1)
    return jsonify({
        'posts': [post.to_json() for post in posts],
        'prev': prev,
        'next': next,
        'count': pagination.total
    })
