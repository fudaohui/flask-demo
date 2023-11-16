# config.py
import logging
import os

from flask import Flask


class AppConfig:
    # 其他应用配置
    APP_NAME = 'pythonbbs'
    LOG_FILE = f"{APP_NAME}.log"
    LOG_LEVEL = 'INFO'


class NacosConfig:
    """从环境变量获取Nacos的配置信息"""
    NACOS_SERVER = os.environ.get('NACOS_SERVER', '10.5.7.76')
    NACOS_PORT = int(os.environ.get('NACOS_PORT', 8848))
    NACOS_NAMESPACE = os.environ.get('NACOS_NAMESPACE', 'public')
    NACOS_DATA_ID = f"{AppConfig.APP_NAME}.json"
    NACOS_GROUP = os.environ.get('NACOS_GROUP', 'DEFAULT_GROUP')


def configure_logging(app: Flask):
    # 配置日志路径和格式
    logging.basicConfig(filename='app.log', level=logging.INFO)
    handler = logging.StreamHandler()
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    app.logger.addHandler(handler)


def configure_mysql(app: Flask, config):
    # 从配置中获取MySQL数据库配置
    mysql_config = config.get('mysqlDatabase', {})

    # 配置MySQL连接字符串
    mysql_uri = f"mysql+pymysql://{mysql_config['username']}:{mysql_config['password']}@{mysql_config['host']}:{mysql_config['port']}/{mysql_config['dbname']}"

    # 配置Flask应用程序
    app.config['SQLALCHEMY_DATABASE_URI'] = mysql_uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
