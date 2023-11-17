import json
import logging

from flask import Flask
from nacos import NacosClient

from app.blueprints.user import user_blueprint
from app.config import NacosConfig, configure_mysql
from app.extensions import db


def create_app():
    """初始化项目：创建flak app并配置日志，nacos,mysql"""
    app = Flask(__name__)
    # 移除默认的 Flask 处理程序
    app.logger.handlers = []
    # 配置通用日志打印
    logging.basicConfig(filename='app.log', level=logging.INFO,
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    # 加载nacos配置
    client = NacosClient(NacosConfig.NACOS_SERVER, NacosConfig.NACOS_PORT, NacosConfig.NACOS_NAMESPACE)
    nacos_config = client.get_config(NacosConfig.NACOS_DATA_ID, NacosConfig.NACOS_GROUP)
    config = json.loads(nacos_config)
    configure_mysql(app, config)
    # 初始化数据库
    db.init_app(app)
    # 注册蓝图
    app.register_blueprint(user_blueprint)
    return app
