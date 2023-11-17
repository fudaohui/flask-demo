import logging

from app.models.module import Student
from ..extensions import db
from ..utils.helpers import generate_response

logger = logging.getLogger(__name__)

def add_user(student: Student):
    try:
        db.session.add(student)
        db.session.commit()
    except Exception as e:
        logger.info(f"添加用户失败，即将回滚：{e}")
        db.session.rollback()
        return generate_response(500, "回滚啦")
