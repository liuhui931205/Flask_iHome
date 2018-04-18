# coding=utf-8
from flask import request,jsonify,make_response,abort,current_app
from iHome.utils.captcha.captcha import captcha
from . import api
from iHome import redis_store,constants
from iHome.response_code import RET
import json
import re
from iHome.utils.sms import CCP
import random

@api.route('/sms_code',methods=['POST'])
def send_sms_code():
    req_data = request.data
    req_dict = json.loads(req_data)
    mobile = req_dict['mobile']
    image_code = req_dict['image_code']
    image_code_id = req_dict['image_code_id']
    if not all([mobile, image_code, image_code_id]):
        return jsonify(errno=RET.PARAMERR, errmsg='信息不完整')
    if not re.match(r'1[3456789]\d{9}',mobile):
        return jsonify(errno=RET.PARAMERR, errmsg='手机号码格式不对')
    try:
        real_image_code = redis_store.get('imagecode:%s'% image_code_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg='查询图片验证码错误')
    if not real_image_code:
        return jsonify(errno=RET.NODATA, errmsg='图片验证码过期')
    if real_image_code != image_code:
        return jsonify(errno=RET.DATAERR, errmsg='图片验证码错误')
    # todo: 发生短信验证码
    sms_code = '%06d'% random.randint(0,999999)
    current_app.logger.info('短信验证码'+sms_code)
    try:
        redis_store.set('sms_code:%s'%mobile, sms_code,constants.SMS_CODE_REDIS_EXPIRES)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR,errmsg='保存验证码失败')

    res = CCP().send_template_sms(mobile ,[sms_code,constants.SMS_CODE_REDIS_EXPIRES/60], 1)
    if res != 1 :
        return jsonify(errno=RET.THIRDERR,errmsg='发送短信失败')
    return jsonify(errno=RET.OK, errmsg='发送短信验证码成功')

@api.route('/image_code')
def get_image_code():
    cur_id = request.args.get('cur_id')
    if not cur_id:
        abort(403)

    name, text, data = captcha.generate_captcha()
    current_app.logger.info('图片验证码'+text)
    try:
        redis_store.set('imagecode:%s' %cur_id, text, constants.IMAGE_CODE_REDIS_EXPIRES )
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR,errmsg='保存图片验证码失败')


    response = make_response(data)
    response.headers['Content-Type'] = 'image/jpg'
    return response

