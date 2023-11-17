import logging

from flask import Blueprint, request

from ..utils.helpers import generate_response

user_blueprint = Blueprint("user", __name__, url_prefix="/user")


logger = logging.getLogger(__name__)

@user_blueprint.route('/create_user', methods=['POST'])
def add_user():
    json = request.get_json()
    logger.info(f"添加用户，接收的参数为：{json}")
    return generate_response(200, "成功")
