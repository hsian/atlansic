from flask import jsonify, request, g, current_app
from . import api
from ..models import User, Role, Captcha
from ..errors import bad_request, unauthorized
from .. import db
from .authorization import auth
import re
    
# @desc: follow and unfollow
# @param:  int:id  | 要关注的用户id
@api.route('/user_follow/<int:id>')
@auth.login_required
def user_follow(id):
    user = User.query.filter_by(id=id).first()
    if user is None:
        return bad_request('关注的用户不存在')
    if g.current_user.is_following(user):
        return jsonify({
            'message': '已关注'
        })
    g.current_user.follow(user)
    db.session.commit()
    return jsonify({
        'message': '关注成功'
    })

# @desc: 用户关注了谁，只能查看自己
@api.route('/user_followed/')
@auth.login_required
def user_followed():
    page = request.args.get('page', 1, type=int)
    pagination = g.current_user.followed.paginate(
        page, per_page=current_app.config['PER_PAGE'],
        error_out=False)
    follows = pagination.items
    prev = None
    if pagination.has_prev:
        prev = url_for('api.user_followed', page=page-1)
    next = None
    if pagination.has_next:
        next = url_for('api.user_followed', page=page+1)
    return jsonify({
        'follows': [follow.followed.to_json() for follow in follows],
    })       

# @desc 谁关注了该用户
@api.route('/user_followers/<int:id>')
def user_followers(id):
    user = User.query.filter_by(id=id).first()
    if user is None:
        return bad_request('该用户不存在')
    page = request.args.get('page', 1, type=int)
    pagination = user.followers.paginate(
        page, per_page=current_app.config['PER_PAGE'],
        error_out=False)
    follows = pagination.items
    prev = None
    if pagination.has_prev:
        prev = url_for('api.user_followers', page=page-1)
    next = None
    if pagination.has_next:
        next = url_for('api.user_followers', page=page+1)
    return jsonify({
        'follows': [follow.follower.to_json() for follow in follows],
    })    

# @desc: 用户信息
@api.route('/user/<int:id>')
@auth.login_required
def get_user(id):
    user = User.query.get_or_404(id)
    return jsonify(user.to_json())

# @desc: 用户信息
@api.route('/user_self/')
@auth.login_required
def get_user_self():
    return jsonify(g.current_user.to_json())

# @desc: 修改密码
@api.route('/user_change_password/', methods=['POST'])
@auth.login_required
def user_change_password():
    try:
        password, old_password = request.json['password'],  \
            request.json['old_password']
        if password == old_password:
            return bad_request('新旧密码不能一致')
        if g.current_user.verify_password(old_password) is False:
            return bad_request('旧密码错误')
        g.current_user.password = password
        db.session.add(g.current_user)
        db.session.commit()
        return jsonify({
            'message': '密码修改成功'
        })    

    except Exception as e:
        return bad_request('错误原因：%s' % repr(e))

# @desc: 编辑资料
@api.route('/user_edit_profile/', methods=['POST'])
@auth.login_required
def user_edit_profile():
    try:
        user = g.current_user
        form = request.json
        email, name, location, about_me, avatar, company, blog = form.get('email'), \
            form.get('name'), form.get('location'), form.get('about_me'), \
            form.get('avatar'), form.get('company'), form.get('blog')

        if name and re.match(r"^[a-zA-Z0-9\w\u4e00-\u9fcc]{2,6}$", name) is None:
            return bad_request('名字长度为2~6字符') 

        user.email = email or user.email
        user.name = name or user.name
        user.location = location or user.location
        user.about_me = about_me or user.about_me
        user.avatar = avatar or user.avatar
        user.company = company or user.company
        user.blog = blog or user.blog
        db.session.add(user)
        db.session.commit()
        return jsonify({
            'message': '修改成功'
        })  

    except Exception as e:
        return bad_request('错误原因：%s' % repr(e))

# @desc: g.current_user可以获取当前用户
@api.route('/user_posts/<int:id>')
@auth.login_required
def get_user_posts(id):
    pass

@api.route('/user_comments/<int:id>')
@auth.login_required
def get_user_comments(id):
    pass