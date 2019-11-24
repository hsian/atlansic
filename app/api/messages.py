from flask import jsonify, request, g, current_app, url_for
from sqlalchemy import or_,and_
from . import api
from ..errors import bad_request, unauthorized
from .authorization import auth
from ..models import Message, User
from ..decorators import admin_required
from .. import db

@api.route('/messages/')
@auth.login_required
def get_messages():
    page = request.args.get('page', 1, type=int)
    pagination = Message.query.filter(
            or_(Message.receiver == g.current_user, Message.public == True)
        ).paginate(
        page, per_page=current_app.config['PER_PAGE'],
        error_out=False
    )
    messages = pagination.items
    prev = None
    if pagination.has_prev:
        prev = url_for('api.get_messages', page=page-1)
    next = None
    if pagination.has_next:
        next = url_for('api.get_messages', page=page+1)
    return jsonify({
        'messages': [message.to_json() for message in messages],
        'prev_url': prev,
        'next_url': next,
        'count': pagination.total
    })

@api.route('/message/<int:id>')
@auth.login_required
def get_message(id):
    message = Message.query.get_or_404(id)
    message.read = True
    db.session.add(message)
    db.session.commit()
    return jsonify(message.to_json())

@api.route('/send_messages/')
@auth.login_required
def get_send_messages():
    page = request.args.get('page', 1, type=int)
    pagination = g.current_user.send_messages.paginate(
        page, per_page=current_app.config['PER_PAGE'],
        error_out=False
    )
    messages = pagination.items
    prev = None
    if pagination.has_prev:
        prev = url_for('api.get_messages', page=page-1)
    next = None
    if pagination.has_next:
        next = url_for('api.get_messages', page=page+1)
    return jsonify({
        'messages': [message.to_json() for message in messages],
        'prev_url': prev,
        'next_url': next,
        'count': pagination.total
    })

@api.route('/send_all_message/', methods=['POST'])
@auth.login_required
@admin_required
def send_all():
    form = request.json
    content = form['content']
    if content is None or content == '':
        return bad_request('内容不能为空')
    message = Message(
        content = content,
        sender = g.current_user,
        public = True
    )
    print(message)
    db.session.add(message)
    db.session.commit()
    return jsonify(message.to_json())

@api.route('/send_message/<int:id>', methods=['POST'])
@auth.login_required
def send(id):
    form = request.json
    content = form['content']
    if content is None or content == '':
        return bad_request('内容不能为空')
    receiver = User.query.get_or_404(id)
    message = Message(
        content = content,
        sender = g.current_user,
        receiver = receiver
    )
    db.session.add(message)
    db.session.commit()
    return jsonify(message.to_json())