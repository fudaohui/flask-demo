from flask import jsonify


def generate_response(status, msg, data=None):
    response = {
        'status': status,
        'msg': msg,
        'data': data
    }
    return jsonify(response)
