# coding=utf-8
from . import api
from flask import request,jsonify,current_app
from iHome.response_code import RET
from iHome import redis_store,db
from iHome.models import User


@api.route('/users',methods=['POST'])
def register():
    req_dict = request.json
    mobile = req_dict.get('mobile')
    phonecode = req_dict.get('phonecode')
    password = req_dict.get('password')

    if not all([mobile,phonecode,password]):
        return jsonify(errno=RET.PARAMERR,errmsg='参数不完整')
    try:
        sms_code = redis_store.get('sms_code:%s' % mobile)
    except Exception as e:
        current_app.logging.error(e)
        return jsonify(errno=RET.DBERR,errmsg='查询短信验证码失败')
    if not sms_code:
        return jsonify(errno=RET.NODATA,errmsg='短信验证码已过期')
    if sms_code != phonecode:
        return jsonify(errno=RET.DATAERR,errmsg='短信验证码错误')
    user = User()
    user.mobile = mobile
    user.name = mobile
    # todo:注册用户密码加密
    user.password = password
    try:
        db.session.add(user)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        current_app.loggging.error(e)
        return jsonify(errno=RET.DBERR,errmsg='保存用户信息失败')

    return jsonify(errno=RET.OK,errmsg='注册成功')