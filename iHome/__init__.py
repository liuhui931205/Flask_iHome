# coding=utf-8
from flask import Flask,session
from flask_sqlalchemy import SQLAlchemy
import redis
from flask_wtf.csrf import CSRFProtect
from flask_session import Session
from config import config_dict
db = SQLAlchemy()

def create_app(config_name):
    app = Flask(__name__)
    config_cls = config_dict[config_name]
    app.config.from_object(config_cls)
    db.init_app(app)
    redis_store = redis.StrictRedis(host=config_cls.REDIS_HOST,port=config_cls.REDIS_PORT)
    CSRFProtect(app)
    Session(app)
    return app