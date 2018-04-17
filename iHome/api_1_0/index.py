# coding=utf-8
from . import api
from iHome import redis_store
import logging
from flask import current_app
#
@api.route('/', methods=['GET', 'POST'])
def index():
    # session['name'] = 'laowang'
    # redis_store.set('name','laowang')
    # logging.fatal('Fatal message')
    # logging.error('Error message')
    # logging.warning('Warning message')
    # logging.info('Info message')
    # logging.debug('Debug message')
    current_app.logger.fatal('Fatal message')
    current_app.logger.error('Error message')
    current_app.logger.warning('Warning message')
    current_app.logger.info('Info message')

    return 'index'
