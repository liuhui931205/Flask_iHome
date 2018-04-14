# coding=utf-8
import redis


class Config(object):
    SQLALCHEMY_DATABASE_URI = 'mysql://root:mysql@127.0.0.1:3306/ihome'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    REDIS_HOST = '127.0.0.1'

    REDIS_PORT = 6379

    SECRET_KEY = '8AyevtvqhQCd2ESBa1um7OSaGzW06PvobevQA8tLaOTBAGmnWd0BNknXSizNUNK2EJpYgwSAqRxfkFGNkojltg=='

    SESSION_TYPE = 'redis'

    SESSION_USE_SIGNER = True

    SESSION_REDIS = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT)

    PERMANENT_SESSION_LIFETIME = 86400


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'mysql://root:mysql@127.0.0.1:3306/ihome'


config_dict = {
    'development': DevelopmentConfig,
    'production': ProductionConfig
}
