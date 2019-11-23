from flask import jsonify, request
from . import message_blueprint
from ..errors import bad_request, unauthorized
from ..auth import TokenAuth
from .model import Message
from ..decorators import admin_required

@message_blueprint.route('/')
@TokenAuth.login_required
def get_messages():
    page = request.args.get('page', 1, type=int)
    pagination = Message.query.paginate(
        page, per_page=current_app.config['PER_PAGE'], 
        error_out=False)
    messages = pagination.items
    prev = None
    if pagination.has_prev:
        prev = url_for('message.get_messages', page=page-1)
    next = None
    if pagination.has_next:
        next = url_for('message.get_messages', page=page+1)
    return jsonify({
        'messages': [message.to_json() for message in messages],
        'prev_url': prev,
        'next_url': next,
        'count': pagination.total
    })


@message_blueprint.route('/send_all/', methods=['POST'])
@TokenAuth.login_required
@admin_required
def send_all():
    pass

@message_blueprint.route('/send/<int:id>', methods=['POST'])
@TokenAuth.login_required
def send():
    pass