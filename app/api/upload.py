from flask import jsonify, request, current_app, g
from .authorization import auth
from . import api
from ..errors import bad_request
import os,sys
import time
# from werkzeug import secure_filename # 获取上传文件的文件名

ALLOWED_EXTENSIONS = set(['jpg', 'jpeg', 'png', 'gif'])

def allowed_file(suffix):
    return suffix in ALLOWED_EXTENSIONS

@api.route('/upload/', methods=['POST'])
@auth.login_required
def upload():
    try:
        file = request.files['file']
        suffix = file.filename.rsplit('.', 1)[1]

        if file and allowed_file(suffix):
            path = os.path.join(current_app.config['UPLOAD_FOLDER'], \
                g.current_user.username)
            abspath = os.path.join(os.getcwd(), 'app', path)

            timer = int(time.time())
            filename = '%s%s.%s' % (str.upper(suffix), str(timer), suffix)

            if not os.path.exists(abspath):
                os.makedirs(abspath)
            file.save(os.path.join(abspath, filename))
            return jsonify({
                'message': '上传成功',
                'url': '/' + os.path.join(path, filename).replace('\\', '/')
            })
    except Exception as e:
        return bad_request('错误原因：%s' % repr(e)) 

