from flask import jsonify, request, g
from threading import Timer
from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth
from ..models import User, Role, Captcha
from ..errors import bad_request, unauthorized
from .. import db
from . import api

auth = HTTPTokenAuth() 

# auth.login_required修饰的函数会先校验token
@auth.verify_token
def verify_token(token):
    if token == '' or token is None:
        return False
    g.current_user = User.verify_auth_token(token)
    g.token_used = True
    return g.current_user is not None # True

@auth.error_handler
def auth_error():
    return unauthorized('Invalid credentials')

@api.route('/captcha/', methods=['POST'])
def get_captcha():
    # 先查询是否验证码还有效,有效的话就不用生成新的验证码了
    fake_code = 2233

    mobile = request.json['mobile']
    if mobile is None:
        return bad_request("手机号码不能空")
    
    if Captcha.validate_times(mobile) is False:
        return bad_request("发送频繁，请稍后再试")

    # 验证码虽然一样，但是还是会写入到数据库中的，因为会验证次数
    captcha = Captcha(
        mobile = mobile,
        code = fake_code
    )
    db.session.add(captcha)
    db.session.commit()

    return jsonify({
        'message': '验证码发送成功'
    })

@api.route('/register/', methods=['POST'])
def register():
    try:
        form = request.json
        username, password, captcha = form['username'], form['password'], \
            form['captcha']

        # 正则判断
        # re

        user = User.query.filter_by(username = username).first()
        if user:
            return bad_request("用户名重复")

        c = Captcha.query.filter_by(
            mobile = username,
            code = captcha,
            valid = True
        ).order_by(Captcha.timestamp.desc()).first()

        if not c or captcha != c.code:
            return bad_request("验证码错误或已过期")

        user = User(
            username = username,
            mobile = username,
            password = password
        )
        db.session.add(user)
        db.session.commit()
            
        return jsonify({
            'message': "注册成功"
        })
    except Exception as e:
        return bad_request('错误原因: %s' % repr(e))

@api.route('/login/', methods=['POST'])
def login():
    try:
        form = request.json
        username, password, captcha = form.get('username'), form.get('password'), form.get('captcha')

        if username is not None:
            user = User.query.filter_by(username = username).first()
            if not user:
                return unauthorized('用户名不存在')

        # 手机号码密码登录
        if password is not None:
            if user.verify_password(password):
                g.current_user = user
            else:
                return unauthorized('密码错误')

        # 手机号码短信验证码登录
        if captcha is not None:
            c = Captcha.query.filter_by(
                mobile = username,
                code = captcha,
                valid = True
            ).order_by(Captcha.timestamp.desc()).first()
            if not c or captcha != c.code:
                return bad_request("验证码错误或已过期")
            else:
                g.current_user = user

        return jsonify({
            'token': g.current_user.generate_auth_token(expiration=3600),
            'expiration': 3600,
            'message': "登录成功"
        })
    except Exception as e:
        return bad_request('错误原因：%s' % repr(e))
