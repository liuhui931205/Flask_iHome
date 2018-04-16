# coding=utf-8
import redis
from flask import Flask
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect

from config import config_dict


db = SQLAlchemy()
redis_store = None

def create_app(config_name):
    app = Flask(__name__)
    config_cls = config_dict[config_name]
    app.config.from_object(config_cls)
    db.init_app(app)

    global redis_store
    redis_store = redis.StrictRedis(host=config_cls.REDIS_HOST,port=config_cls.REDIS_PORT)

    CSRFProtect(app)
    Session(app)

    from iHome.api_1_0 import api
    app.register_blueprint(api,url_prefix='/api/v1.0')
    return app