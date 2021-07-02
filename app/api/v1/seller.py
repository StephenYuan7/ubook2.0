from flask import jsonify, current_app, g
from app.libs.error_code import Success
from app.libs.red_print import Redprint
from app.libs.token_auth import auth
from app.models.product import Product
from app.validators.form import ProductUpForm, ProductRenewForm

api = Redprint('seller')


@api.route('/add', methods=['POST'])
@auth.login_required
def up_product():
    form = ProductUpForm().validate_for_api()
    Product.add(form.title.data,
                form.currentPrice.data,
                form.originalPrice.data,
                form.description.data,
                form.address.data,
                form.kind.data,
                form.degree.data,
                form.state.data,
                g.user.uid)
    return Success()


@api.route('/renew', methods=['POST'])
@auth.login_required
def renew_product():
    form = ProductRenewForm().validate_for_api()
    product = Product.query.filter_by(id=form.product_id.data, user_id=g.user.uid).first_or_404()
    Product.renew(product,
                  form.title.data,
                  form.currentPrice.data,
                  form.originalPrice.data,
                  form.description.data,
                  form.address.data,
                  form.kind.data,
                  form.degree.data,
                  form.state.data,
                  g.user.uid)
    return Success()
