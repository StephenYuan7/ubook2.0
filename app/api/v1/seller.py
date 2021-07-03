from flask import jsonify, current_app, g
from app.libs.error_code import Success, DeleteSuccess
from app.libs.red_print import Redprint
from app.libs.token_auth import auth
from app.models.base import db
from app.models.product import Product
from app.models.transaction import Transaction
from app.validators.form import ProductUpForm, ProductRenewForm, ProductDeleteForm, PageForm, TransactionForm

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
    Product.renew(form.product_id.data,
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


@api.route('/delete', methods=['DELETE'])
@auth.login_required
def delete_product():
    form = ProductDeleteForm().validate_for_api()
    product = Product().verify_user_product(g.user.uid, form.product_id.data)
    with db.auto_commit():
        product.delete()
    return DeleteSuccess()


@api.route('/self', methods=['GET'])
@auth.login_required
def my_up():
    form = PageForm().validate_for_api()
    begin = current_app.config['PAGE'] * form.page.data
    products = Product().get_user_products(g.user.uid, begin, current_app.config['PAGE'])
    return jsonify(products)


@api.route('/confirm', methods=['POST'])
@auth.login_required
def confirm_transaction():
    form = TransactionForm().validate_for_api()
    transaction = Transaction().verify_seller_transaction(g.user.uid, form.transaction_id.data)
    if transaction.state == '0':
        with db.auto_commit():
            transaction.state = '1'
    return Success()


@api.route('/refuse', methods=['POST'])
@auth.login_required
def refuse_transaction():
    form = TransactionForm().validate_for_api()
    transaction = Transaction().verify_seller_transaction(g.user.uid, form.transaction_id.data)
    if transaction.state == '0':
        with db.auto_commit():
            transaction.state = 'b'
    return Success()
