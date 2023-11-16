import json

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from nacos import NacosClient
from sqlalchemy import text
from models.module import db

from config import NacosConfig, configure_logging, configure_mysql


def test_database_connection():
    with app.app_context():
        try:
            with db.engine.connect() as conn:
                rs = conn.execute(text("select 1"))
                result = rs.fetchone()
                app.logger.info(f"Database connection successful. Result: {result}")
        except Exception as e:
            app.logger.error(f"Database connection error: {e}")

app = Flask(__name__)
configure_logging(app)
# 加载nacos配置
client = NacosClient(NacosConfig.NACOS_SERVER, NacosConfig.NACOS_PORT, NacosConfig.NACOS_NAMESPACE)
nacos_config = client.get_config(NacosConfig.NACOS_DATA_ID, NacosConfig.NACOS_GROUP)
config = json.loads(nacos_config)
configure_mysql(app, config)
# 初始化数据库
db.init_app(app)
# test_database_connection()


if __name__ == '__main__':
    app.run()
