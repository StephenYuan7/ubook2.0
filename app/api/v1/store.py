from flask import g, jsonify

from app.libs.error_code import Success
from app.libs.red_print import Redprint
from app.libs.token_auth import auth
from app.models.store import Store
from app.validators.form import StoreCreateForm, UserIdForm

api = Redprint('store')


@api.route('/create', methods=['POST'])
@auth.login_required
def create_store():
    form = StoreCreateForm().validate_for_api()
    Store().create(g.user.uid,
                   form.name.data,
                   form.phone.data,
                   form.address.data,
                   form.description.data)
    return Success()


@api.route('/information', methods=['POST'])
@auth.login_required
def get_store_information():
    form = UserIdForm().validate_for_api()
    if form.user_id.data:
        store = Store().get(form.user_id.data)
    else:
        store = Store().get(g.user.uid)
    return jsonify(store)


