from flask import jsonify, request, g, current_app, url_for
from sqlalchemy import or_,and_
from . import api
from ..errors import bad_request
from ..models import Comment, Post
from ..decorators import admin_required
from .authorization import auth
from .. import db

@api.route('/new_comment/', methods=['POST'])
@auth.login_required
def new_comment():
    try:
        form = request.json
        print(form)
        body, post_id, parent_id = form['body'], form['post_id'], \
                form.get('parent_id')
        comment = Comment(
            body = body,
            author = g.current_user,
            post_id = post_id,
            parent_id = parent_id
        )
        db.session.add(comment)
        db.session.commit()
        return jsonify({
            'message': '添加成功',
            'data': comment.to_json()
        })

    except Exception as e:
        return bad_request('错误原因：%s' % repr(e))

@api.route('/edit_comment/<int:id>', methods=['POST'])
@auth.login_required
@admin_required
def edit_comment(id):
    try:
        comment = Comment.query.get_or_404(id)
        form = request.json
        comment.enable = form.get('enable', comment.enable)
        db.session.add(comment)
        db.session.commit()
        return jsonify({
            'message': '编辑成功',
            'data': comment.to_json()
        })

    except Exception as e:
        return bad_request('错误原因：%s' % repr(e))
    

@api.route('/get_comments/<int:id>')
def get_comments(id):
    try:
        post = Post.query.get_or_404(id)
        page = request.args.get('page', 1, type=int)
        pagination = post.comments.filter(
                and_(Comment.enable==True, Comment.level==1)
            ).paginate(
            page, per_page=current_app.config['PER_PAGE'],
            error_out=False)
        comments = pagination.items
        prev = None
        if pagination.has_prev:
            prev = url_for('api.get_comments', id=id, page=page-1)
        next = None
        if pagination.has_next:
            next = url_for('api.get_comments', id=id, page=page+1)
        return jsonify({
            'comments': [comment.to_json() for comment in comments],
            'prev': prev,
            'next': next,
            'count': pagination.total
        })   
    except Exception as e:
        return bad_request('错误原因：%s' % repr(e))
