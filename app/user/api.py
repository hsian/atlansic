from flask import jsonify, request, g
from . import user
from .model import User, Role
from ..errors import bad_request

@user.route("/roles/")
def get_roles():
    roles = Role.query.all()
    return jsonify({
        "roles": [role.to_json() for role in roles]
    })

@user.route('/captcha/')
def get_captcha():
    fake_captcha = 1234
    g.captcha = fake_captcha

    return jsonify({
        'message': '验证码发送成功'
    })

@user.route('/register/', methods=['POST'])
def register():
    form = request.form
    username, password, captcha = form.get('username'), form.get('password'), \
        form.get('captcha')

    # 正则判断

    user = User.query.filter_by(username = username).first()
    if user:
        return bad_request("用户名重复")
        
    return jsonify({
        'message': "注册成功"
    })
