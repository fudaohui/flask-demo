# config.py
import logging
import os
from logging.handlers import RotatingFileHandler

from flask import Flask
from redis import StrictRedis


class AppConfig:
    # 其他应用配置
    APP_NAME = 'pythonbbs'


class NacosConfig:
    """从环境变量获取Nacos的配置信息"""
    NACOS_SERVER = os.environ.get('NACOS_SERVER', '10.5.7.76')
    NACOS_PORT = int(os.environ.get('NACOS_PORT', 8848))
    NACOS_NAMESPACE = os.environ.get('NACOS_NAMESPACE', 'public')
    NACOS_DATA_ID = f"{AppConfig.APP_NAME}.json"
    NACOS_GROUP = os.environ.get('NACOS_GROUP', 'DEFAULT_GROUP')


log_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')


def get_filelog_handler():
    # 创建一个RotatingFileHandler对象
    file_handler = RotatingFileHandler('app.log', maxBytes=163840, backupCount=20, encoding='utf-8')
    # 设置handler级别为INFO
    file_handler.setLevel(logging.INFO)
    # 将日志格式对象添加到handler中
    file_handler.setFormatter(log_formatter)
    return file_handler


def get_consolelog_handler():
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(log_formatter)
    return console_handler


def configure_mysql(app: Flask, config):
    """mysql单机配置
    :param app flask app
    :param config nacos配置
    """
    mysql_config = config.get('mysqlDatabase', {})
    # 配置MySQL连接字符串
    mysql_uri = f"mysql+pymysql://{mysql_config['username']}:{mysql_config['password']}@{mysql_config['host']}:{mysql_config['port']}/{mysql_config['dbname']}"
    # 配置Flask应用程序
    app.config['SQLALCHEMY_DATABASE_URI'] = mysql_uri
    # 禁用Flask - SQLAlchemy的跟踪修改功能
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


def configure_redis_single(app: Flask, config):
    """单机版redis配置
    :parameter app flask app
    :parameter config nacos配置
    """
    redis_config = config.get('redisDataBase', {})
    # 配置 Redis 单机连接
    redis_host = redis_config.get('host', 'localhost')
    redis_port = redis_config.get('port', 6379)
    redis_db = redis_config.get('db', 0)
    redis_password = redis_config.get('password', None)
    # 创建 Redis 连接对象
    app.config['REDIS_URL'] = f'redis://:{redis_password}@{redis_host}:{redis_port}/{redis_db}'
