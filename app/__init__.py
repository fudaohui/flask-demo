import json
import logging

from flask import Flask
from nacos import NacosClient

from app.api.user_api import user_blueprint
from app.config import NacosConfig, configure_mysql, get_filelog_handler, get_consolelog_handler, configure_redis_single
from app.extensions import *


def create_app():
    """初始化项目：创建flak app并配置日志，nacos,mysql"""
    app = Flask(__name__)
    # 清除根日志的处理程序
    for console_handler in logging.root.handlers[:]:
        print(console_handler)
        logging.root.removeHandler(console_handler)

    filelog_handler = get_filelog_handler()
    console_handler = get_consolelog_handler()
    logging.basicConfig(level=logging.INFO, handlers=[filelog_handler, console_handler])
    app.logger.info("测试一下")
    # 加载nacos配置
    client = NacosClient(NacosConfig.NACOS_SERVER, NacosConfig.NACOS_PORT, NacosConfig.NACOS_NAMESPACE)
    nacos_config = client.get_config(NacosConfig.NACOS_DATA_ID, NacosConfig.NACOS_GROUP)
    config = json.loads(nacos_config)
    configure_mysql(app, config)
    configure_redis_single(app,config)
    # 初始化数据库
    db.init_app(app)
    redis_client.init_app(app)

    # 注册蓝图
    app.register_blueprint(user_blueprint)
    return app
