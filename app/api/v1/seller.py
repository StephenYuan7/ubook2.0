import os

from flask import jsonify, current_app, g, request
from app.libs.error_code import Success, DeleteSuccess, NotFound
from app.libs.red_print import Redprint
from app.libs.token_auth import auth
from app.libs.up_image import up_image
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


@api.route('/self', methods=['POST'])
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


@api.route('/upimage/<product_id>/<image_id>', methods=['POST'])
@auth.login_required
def up_product_image(product_id, image_id):
    image_id = int(image_id)
    if image_id > 3 or image_id < 1:
        return NotFound()
    product = Product().verify_user_product(g.user.uid, int(product_id))
    img = request.files.get('upload')
    image_name = up_image(img)
    with db.auto_commit():
        basedir = os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
        path = basedir + "/static/image/"
        if image_id == 1:
            if product.image1 and os.path.exists(path + str(product.image1)):
                os.remove(path + str(product.image1))
            product.image1 = image_name
        if image_id == 2:
            if product.image2 and os.path.exists(path + str(product.image2)):
                os.remove(path + str(product.image2))
            product.image2 = image_name
        if image_id == 3:
            if product.image3 and os.path.exists(path + str(product.image2)):
                os.remove(path + str(product.image3))
            product.image3 = image_name
    return Success()
