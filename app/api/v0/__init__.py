from flask import Blueprint

def create_blueprint_v0():
    bp_v0 = Blueprint('v0', __name__)
    return bp_v0
