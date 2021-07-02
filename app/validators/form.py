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
