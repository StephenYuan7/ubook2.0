"""
构建各种类型的验证器
"""

from wtforms import StringField, IntegerField, FloatField
from wtforms.validators import DataRequired, length, ValidationError, Regexp, EqualTo, NumberRange, InputRequired

from app.validators.base import BaseForm as Form


class ClientForm(Form):
    real_name = StringField(validators=[DataRequired(message='不允许为空'), length(
        min=1, max=50
    )])
    nickname = StringField(validators=[DataRequired(message='不允许为空'), length(
        min=1, max=30
    )])
    school_id = IntegerField(validators=[DataRequired(message='不允许为空')])
    user_academy = StringField(validators=[DataRequired(message='不允许为空'), length(
        min=1, max=30
    )])
    user_grade = StringField(validators=[DataRequired(message='不允许为空'), length(
        min=1, max=7
    )])
    student_number = StringField(validators=[DataRequired(message='不允许为空'), length(
        min=10, max=10
    )])


class ClientCreateForm(ClientForm):
    password = StringField(validators=[DataRequired(message='不允许为空'), length(
        min=1, max=50
    )])


class TokenForm(Form):
    student_number = StringField(validators=[DataRequired(message='不允许为空'), length(
        min=10, max=10
    )])
    password = StringField(validators=[DataRequired(message='不允许为空'), length(
        min=1, max=50
    )])


class ClientIdentityForm(Form):
    student_number = StringField(validators=[DataRequired(message='不允许为空'), length(
        min=10, max=10
    )])


class ProductUpForm(Form):
    currentPrice = FloatField()
    originalPrice = FloatField()
    title = StringField(validators=[DataRequired(message='不允许为空'), length(
        min=1, max=100)])
    description = StringField(validators=[DataRequired(message='不允许为空'), length(
        min=1, max=1000)])
    address = StringField(validators=[DataRequired(message='不允许为空'), length(
        min=1, max=100)])
    kind = IntegerField(validators=[DataRequired()])
    degree = IntegerField(validators=[DataRequired()])
    state = StringField(validators=[DataRequired(message='不允许为空'), length(
        min=1, max=1)])


class ProductRenewForm(ProductUpForm):
    product_id = IntegerField(validators=[DataRequired(message='不允许为空')])


class ProductDeleteForm(Form):
    product_id = IntegerField(validators=[DataRequired(message='不允许为空')])


class PageForm(Form):
    page = IntegerField(validators=[NumberRange(min=0)])


class ProductSearchForm(Form):
    key = StringField(validators=[length(max=100)])
    kind = IntegerField(validators=[NumberRange(min=0)])
    time = IntegerField(validators=[NumberRange(min=0, max=1)])
    price = IntegerField(validators=[NumberRange(min=0, max=1)])
    page = IntegerField(validators=[NumberRange(min=0)])


class TransactionAddForm(Form):
    product_id = IntegerField(validators=[DataRequired(message='不允许为空')])
    # price = IntegerField()
    # address = StringField(validators=[DataRequired(message='不允许为空'), length(
    #     min=1, max=100)])
    # order_time = StringField(validators=[DataRequired(message='不允许为空'), length(
    #     min=1, max=100)])


class TransactionForm(Form):
    transaction_id = IntegerField(validators=[DataRequired(message='不允许为空')])


class TransactionEvaluateForm(TransactionForm):
    star = IntegerField(validators=[NumberRange(min=1, max=5)])
    evaluation = StringField(validators=[DataRequired(message='不允许为空'), length(
        min=1, max=1000)])


class StoreCreateForm(Form):
    address = StringField(validators=[DataRequired(message='不允许为空'), length(
        min=1, max=100)])
    name = StringField(validators=[DataRequired(message='不允许为空'), length(
        min=1, max=100)])
    phone = StringField(validators=[DataRequired(message='不允许为空'), length(
        min=1, max=10)])
    description = StringField(validators=[DataRequired(message='不允许为空'), length(
        min=1, max=1000)])


class UserIdForm(Form):
    user_id = IntegerField()


class AddressCreateForm(Form):
    address = StringField(validators=[DataRequired(message='不允许为空'), length(
        min=1, max=100)])
    phone = StringField(validators=[DataRequired(message='不允许为空'), length(
        min=1, max=10)])


class AddressDeleteForm(Form):
    address_id = IntegerField()
