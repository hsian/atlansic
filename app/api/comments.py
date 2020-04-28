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

@api.route('/new_temp_comment/', methods=['POST'])
def new_temp_comment():
	try:
		form = request.json
		body, post_id, parent_id, temp_name, temp_contact_type, temp_contact_value = form['body'], form['post_id'], \
		form.get('parent_id'), form['temp_name'], form['temp_contact_type'], form['temp_contact_value']
		comment = Comment(
			body = body,
			post_id = post_id,
			parent_id = parent_id,
			temp_name = temp_name,
			temp_contact_type = temp_contact_type,
			temp_contact_value = temp_contact_value
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
    

@api.route('/post_comments/<int:id>')
def post_comments(id):
    try:
        post = Post.query.get_or_404(id)
        page = request.args.get('page', 1, type=int)
        page_size = request.args.get('pageSize', current_app.config['PER_PAGE'], type=int)
        pagination = post.comments.filter(
                and_(Comment.level==1)
            ).order_by(
                Comment.timestamp.desc()
            ).paginate(
                page, per_page=page_size,
                error_out=False)
        comments = pagination.items
        prev = None
        if pagination.has_prev:
            prev = url_for('api.post_comments', id=id, page=page-1)
        next = None
        if pagination.has_next:
            next = url_for('api.post_comments', id=id, page=page+1)
        return jsonify({
            'comments': [comment.to_json() for comment in comments],
            'prev': prev,
            'next': next,
            'count': pagination.total
        })   
    except Exception as e:
        return bad_request('错误原因：%s' % repr(e))

@api.route('/all_comments/')
def all_comments():
    try:
        page = request.args.get('page', 1, type=int)
        page_size = request.args.get('pageSize', current_app.config['PER_PAGE'], type=int)
        pagination = Comment.query.order_by(
                Comment.timestamp.desc()
            ).paginate(
                page, per_page=page_size,
                error_out=False)
        comments = pagination.items
        prev = None
        if pagination.has_prev:
            prev = url_for('api.all_comments', id=id, page=page-1)
        next = None
        if pagination.has_next:
            next = url_for('api.all_comments', id=id, page=page+1)
        return jsonify({
            'comments': [comment.to_json() for comment in comments],
            'prev': prev,
            'next': next,
            'count': pagination.total
        })   
    except Exception as e:
        return bad_request('错误原因：%s' % repr(e))

