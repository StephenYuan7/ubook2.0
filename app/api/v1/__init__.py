from flask import Blueprint


def create_blueprint_v1():
    bp_v1 = Blueprint('v1', __name__)
    return bp_v1
