import logging

from flask import Blueprint, request

from ..models.module import Student
from ..utils.helpers import generate_response
from ..services import user_api_service

user_blueprint = Blueprint("user", __name__, url_prefix="/user")

logger = logging.getLogger(__name__)


@user_blueprint.route('/create_user', methods=['POST'])
def add_user():
    json = request.get_json()
    logger.info(f"添加用户，接收的参数为：{json}")
    name = json.get('name')
    if not name:
        return generate_response(500, "用户名为空")
    student = Student(name=name)
    user_api_service.add_user(student)
    return generate_response(200, "成功")
