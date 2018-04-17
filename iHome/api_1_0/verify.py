# coding=utf-8
from flask import request,jsonify,make_response,abort
from iHome.utils.captcha.captcha import captcha
from . import api
from iHome import redis_store,constants
from iHome.response_code import RET

@api.route('/image_code')
def get_image_code():
    cur_id = request.args.get('cur_id')
    if not cur_id:
        abort(403)

    name, text, data = captcha.generate_captcha()
    try:
        redis_store.set('imagecode: %s' %cur_id, text, constants.IMAGE_CODE_REDIS_EXPIRES )
    except Exception as e:
        print e
        return jsonify(errno=RET.DBERR,errmsg='保存图片验证码失败')


    response = make_response(data)
    response.headers['Content-Type'] = 'image/jpg'
    return response

