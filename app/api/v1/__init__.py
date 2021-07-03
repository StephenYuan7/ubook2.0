from flask import Blueprint

from app.api.v1 import client, seller, buyer


def create_blueprint_v1():
    bp_v1 = Blueprint('v1', __name__)
    client.api.register(bp_v1)
    seller.api.register(bp_v1)
    buyer.api.register(bp_v1)

    return bp_v1
