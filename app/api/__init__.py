from flask import Blueprint

api = Blueprint('api', __name__)

from . import authorization, messages, users, categories, posts, tags, comments, upload