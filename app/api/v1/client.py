import os

from flask import jsonify, current_app, g, request

from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

from app.libs.error_code import Success, SizeOverflow
from app.libs.red_print import Redprint
from app.libs.token_auth import auth
from app.libs.up_image import up_image
from app.models.base import db
from app.models.user import User
from app.validators.form import ClientForm, TokenForm, ClientCreateForm, ClientIdentityForm

api = Redprint('client')


@api.route('/create', methods=['POST'])
def create_client():
    form = ClientCreateForm().validate_for_api()
    User.register(
        form.real_name.data,
        form.user_academy.data,
        form.nickname.data,
        form.school_id.data,
        form.user_grade.data,
        form.student_number.data,
        form.password.data)
    return Success()


@api.route('/secret', methods=['GET'])
def get_token_info():
    """获取令牌信息"""
    form = TokenForm().validate_for_api()
    expiration = current_app.config['TOKEN_EXPIRATION']
    identity = User.verify(form.student_number.data, form.password.data)
    token = generate_auth_token(identity['uid'],
                                identity['scope'],
                                expiration)
    t = {
        'token': token.decode('ascii')
    }
    return jsonify(t), 201


@api.route('/reset', methods=['POST'])
@auth.login_required
def reset_client():
    uid = g.user.uid
    with db.auto_commit():
        form = ClientForm().validate_for_api()
        user = User.query.filter_by(id=uid).first_or_404()
        user.reset(user,
                   form.real_name.data,
                   form.user_academy.data,
                   form.nickname.data,
                   form.school_id.data,
                   form.user_grade.data,
                   form.student_number.data, )
    return Success()


@api.route('/information', methods=['GET'])
@auth.login_required
def get_information():
    form = ClientIdentityForm().validate_for_api()
    if form.student_number.data == '0000000000':
        user = User.query.filter_by(id=g.user.uid).first_or_404()
    else:
        user = User.query.filter_by(student_number=form.student_number.data).first_or_404()
    return jsonify(user)


@api.route('/upprofile', methods=['POST'])
@auth.login_required
def up_profile():
    uid = g.user.uid
    cl = request.content_length
    if cl is not None and cl > 3 * 1024 * 1024:
        return SizeOverflow()
    # 获取图片文件 name = upload
    user = User.query.filter_by(id=uid).first_or_404()
    img = request.files.get('upload')
    image_name = up_image(img)
    with db.auto_commit():
        if user.profile and user.profile != 'default.jpg':
            basedir = os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
            path = basedir + "/static/image/"
            if os.path.exists(path + user.profile):
                os.remove(path + user.profile)
        user.profile = image_name
    return Success()


def generate_auth_token(uid, scope=None,
                        expiration=7200):
    """生成令牌"""
    s = Serializer(current_app.config['SECRET_KEY'],
                   expires_in=expiration)
    return s.dumps({
        'uid': uid,
        'scope': scope
    })
