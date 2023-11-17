import logging

from app.models.module import Student
from ..extensions import *
from ..utils.helpers import generate_response

logger = logging.getLogger(__name__)

def add_user(student: Student):
    try:
        db.session.add(student)
        # todo pycharm加todo没有快捷键？下面set方法怎么点不出来？debug中文乱码，正常运行没有，如何直接将student序列化？
        redis_client.set('my_key', student.name)
        db.session.commit()
    except Exception as e:
        logger.info(f"添加用户失败，即将回滚：{e}")
        db.session.rollback()
        return generate_response(500, "回滚啦")
