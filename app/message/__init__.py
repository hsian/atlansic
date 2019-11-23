from flask import Blueprint

message_blueprint = Blueprint('message', __name__)

from . import api