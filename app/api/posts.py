from flask import jsonify, request, g, current_app, url_for
from sqlalchemy import or_,and_
from . import api
from ..errors import bad_request, forbidden
from .authorization import auth
from ..models import Category, User, Post, Permission, Tag
from ..decorators import permission_required
from .. import db

@api.route('/posts/')
def get_posts():
    page = request.args.get('page', 1, type=int)
    pagination = Post.query.filter_by(enable=True).paginate(
        page, per_page=current_app.config['PER_PAGE'],
        error_out=False)
    posts = pagination.items
    prev = None
    if pagination.has_prev:
        prev = url_for('api.get_posts', page=page-1)
    next = None
    if pagination.has_next:
        next = url_for('api.get_posts', page=page+1)
    return jsonify({
        'posts': [post.to_json() for post in posts],
        'prev': prev,
        'next': next,
        'count': pagination.total
    })     

@api.route('/posts_self/')
@auth.login_required
def get_posts_self():
    page = request.args.get('page', 1, type=int)
    page_size = request.args.get('pageSize', current_app.config['PER_PAGE'], type=int)
    pagination = Post.query.filter(
        and_(Post.author == g.current_user, Post.enable == True)
        ).paginate(
        page, per_page=page_size,
        error_out=False)
    posts = pagination.items
    prev = None
    if pagination.has_prev:
        prev = url_for('api.get_posts', page=page-1)
    next = None
    if pagination.has_next:
        next = url_for('api.get_posts', page=page+1)
    return jsonify({
        'posts': [post.to_json() for post in posts],
        'prev': prev,
        'next': next,
        'count': pagination.total
    })

@api.route('/post/<int:id>')
def get_post(id):
    post = Post.query.filter(and_(Post.id == id, Post.enable == True)).first()
    if post is None:
        return bad_request("文章不存在或已关闭")
    return jsonify(post.to_json())

@api.route('/new_post/', methods=['POST'])
@auth.login_required
@permission_required(Permission.WRITE)
def new_post():
    try:
        form = request.json
        title, body, category_id = form['title'], form['body'], \
            form['category_id']

        # 禁止提交到public栏目
        if Category.is_public(category_id) is False and \
            not g.current_user.can(Permission.ADMIN):
            return forbidden("权限不够")
        post = Post(
            title = title,
            body = body,
            author = g.current_user,
            category_id = category_id
        )
        tags = form.get('tags')
        if isinstance(tags,list):
            for tag_id in tags:
                tag = Tag.query.get_or_404(tag_id)
                post.tags.append(tag)
        db.session.add(post)
        db.session.commit()
        return jsonify({
            'message': '新增成功',
            'data': post.to_json()
        })

    except Exception as e:
        return bad_request('错误原因：%s' % repr(e))

@api.route('/edit_post/<int:id>', methods=['POST'])
@auth.login_required
@permission_required(Permission.WRITE)
def edit_post(id):
    try:
        post = Post.query.get_or_404(id)
        if g.current_user != post.author and \
            not g.current_user.can(Permission.ADMIN):
            return forbidden('权限不够')
        post.title = request.json.get('title', post.title)
        post.body = request.json.get('body', post.body)
        post.enable = request.json.get('enable', post.enable)
        # post.category_id = request.json.get('category_id', post.category_id)
        tags = request.json.get('tags')
        if isinstance(tags,list):
            if len(tags) == 0 and post.tags:
                for post_tag in post.tags:
                    post.tags.remove(post_tag)
            else:    
                for tag_id in tags:
                    tag = Tag.query.get_or_404(tag_id)
                    post.tags.append(tag)
        db.session.add(post)
        db.session.commit()
        return jsonify({
            'message': '修改成功',
            'data': post.to_json()
        })

    except Exception as e:
        return bad_request('错误原因：%s' % repr(e))