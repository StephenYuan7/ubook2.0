from flask import g, jsonify

from app.libs.error_code import Success, DeleteSuccess
from app.libs.red_print import Redprint
from app.libs.token_auth import auth
from app.models.address import Addressinfo
from app.models.base import db
from app.validators.form import  UserIdForm, AddressCreateForm, AddressDeleteForm

api = Redprint('address')


@api.route('/create', methods=['POST'])
@auth.login_required
def create_address():
    form = AddressCreateForm().validate_for_api()
    Addressinfo().create(g.user.uid,
                         form.phone.data,
                         form.address.data)
    return Success()


@api.route('/information', methods=['GET'])
@auth.login_required
def get_address_information():
    form = UserIdForm().validate_for_api()
    if form.user_id.data:
        address = Addressinfo().get(form.user_id.data)
    else:
        address = Addressinfo().get(g.user.uid)
    return jsonify(address)


@api.route('/delete', methods=['DELETE'])
@auth.login_required
def delete_address_information():
    form = AddressDeleteForm().validate_for_api()
    address = Addressinfo().verify_user_address(g.user.uid, form.address_id.data)
    with db.auto_commit():
        address.delete()
    return DeleteSuccess()
