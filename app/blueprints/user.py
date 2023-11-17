import logging

from flask import Blueprint, request

from ..utils.helpers import generate_response

user_blueprint = Blueprint("user", __name__, url_prefix="/user")


@user_blueprint.route('/create_user', methods=['POST'])
def add_user():
    json = request.get_json()
    logging.info(f"添加用户，接收的参数为：{json}")
    return generate_response(200, "成功")
