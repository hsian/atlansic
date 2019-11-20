from flask import jsonify, request, g
from . import user
from .model import User, Role, Captcha
from ..errors import bad_request, unauthorized
from .. import db


@user.route("/roles/")
def get_roles():
    roles = Role.query.all()
    return jsonify({
        "roles": [role.to_json() for role in roles]
    })
    
# @desc: follow and unfollow
# @param:  int:id  | 要关注的用户id
@user.route('/user_follow/<int:id>')
def user_follow(id):
    pass

# @desc: 用户关注了谁，只能查看自己
@user.route('/user_followed/')
def user_followed():
    pass

# @desc 谁关注了该用户
@user.route('/user_followers/<int:id>')
def user_followers():
    pass

# @desc: g.current_user可以获取当前用户
@user.route('/user/<int:id>')
def get_user(id):
    pass

@user.route('/users/')
def get_users():
    pass

# @desc: g.current_user可以获取当前用户
@user.route('/user_posts/<int:id>')
def get_user_posts(id):
    pass

@user.route('/user_comments/<int:id>')
def get_user_comments(id):
    pass