from flask import jsonify, current_app, g
from datetime import datetime
from app.libs.error_code import Success, DeleteSuccess
from app.libs.red_print import Redprint
from app.libs.token_auth import auth
from app.models.base import db
from app.models.product import Product
from app.models.transaction import Transaction
from app.validators.form import PageForm, ProductSearchForm, \
    TransactionAddForm, TransactionForm, TransactionEvaluateForm

api = Redprint('buyer')


@api.route('/search', methods=['GET'])
@auth.login_required
def search_product():
    form = ProductSearchForm().validate_for_api()
    products = Product().get_products_filter(form).all()
    return jsonify(products)


@api.route('/add', methods=['POST'])
@auth.login_required
def add_transaction():
    form = TransactionAddForm().validate_for_api()
    Transaction().add(form, g.user.uid)
    return Success()


@api.route('/self', methods=['GET'])
@auth.login_required
def my_buy():
    form = PageForm().validate_for_api()
    begin = current_app.config['PAGE'] * form.page.data
    transactions = Transaction().get_user_transactions(g.user.uid, begin, current_app.config['PAGE'])
    return jsonify(transactions)


@api.route('/cancel', methods=['POST'])
@auth.login_required
def cancel_transaction():
    form = TransactionForm().validate_for_api()
    transaction = Transaction().verify_buyer_transaction(g.user.uid, form.transaction_id.data)
    if transaction.state == '0' or transaction.state == '1':
        with db.auto_commit():
            transaction.state = 'a'
    return Success()


@api.route('/confirm', methods=['POST'])
@auth.login_required
def confirm_transaction():
    form = TransactionForm().validate_for_api()
    transaction = Transaction().verify_buyer_transaction(g.user.uid, form.transaction_id.data)
    if transaction.state == '1':
        with db.auto_commit():
            transaction.state = '2'
            transaction.over_time = int(datetime.now().timestamp())
    return Success()


@api.route('/evaluate', methods=['POST'])
@auth.login_required
def evaluate_transaction():
    form = TransactionEvaluateForm().validate_for_api()
    transaction = Transaction().verify_buyer_transaction(g.user.uid, form.transaction_id.data)
    if transaction.state == '2':
        with db.auto_commit():
            transaction.star = form.star.data
            transaction.evaluation = form.evaluation.data
    return Success()