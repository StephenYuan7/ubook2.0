from flask import jsonify

from app.libs.red_print import Redprint

api = Redprint('client')


@api.route('/create', methods=['POST'])
def create_client():
    return jsonify(1)
