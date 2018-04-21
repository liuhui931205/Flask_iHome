# coding=utf-8
import re

from flask import request, jsonify, current_app, session

from iHome import redis_store, db
from iHome.models import User
from iHome.response_code import RET
from . import api

@api.route('/session')
def check_user_login():

    username = session.get('username')
    user_id = session.get('user_id')
    return jsonify(errno=RET.OK, errmsg='ok',data={'user_id':user_id,'username':username})


@api.route('/session',methods=['DELETE'])
def logout():
    session.clear()

    return jsonify(errno=RET.OK, errmsg='退出登录成功')

@api.route('/session', methods=['POST'])
def login():
    """
    1.获取参数
    2.判断参数是否有值
    3.判断手机号是否合法
    4.查询数据库用户信息
    5.用户不存在判断
    6.校验密码
    7.使用session保存用户信息
    :return:
    """
    req_dict = request.json
    mobile = req_dict.get('mobile')
    password = req_dict.get('password')

    if not all([mobile, password]):
        return jsonify(errno=RET.PARAMERR, errmsg='参数不完整')

    if not re.match(r'1[3456789]\d{9}', mobile):
        return jsonify(errno=RET.PARAMERR, errmsg='手机格式不对')
    try:
        user = User.query.filter(User.mobile == mobile).first()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg='查询用户失败')

    if not user:
        return jsonify(errno=RET.USERERR, errmsg='用户不存在')

    if not user.check_password(password):
        return jsonify(errno=RET.PWDERR, errmsg='密码错误')

    session['user_id'] = user.id
    session['username'] = user.name
    session['mobile'] = user.mobile

    return jsonify(errno=RET.OK, errmsg='登录成功')


@api.route('/users', methods=['POST'])
def register():
    req_dict = request.json
    mobile = req_dict.get('mobile')
    phonecode = req_dict.get('phonecode')
    password = req_dict.get('password')

    if not all([mobile, phonecode, password]):
        return jsonify(errno=RET.PARAMERR, errmsg='参数不完整')
    try:
        sms_code = redis_store.get('sms_code:%s' % mobile)
    except Exception as e:
        current_app.logging.error(e)
        return jsonify(errno=RET.DBERR, errmsg='查询短信验证码失败')
    if not sms_code:
        return jsonify(errno=RET.NODATA, errmsg='短信验证码已过期')
    if sms_code != phonecode:
        return jsonify(errno=RET.DATAERR, errmsg='短信验证码错误')

    try:
        user = User.query.filter(User.mobile == mobile).first()
    except Exception as e:
        current_app.logger.error(e)

    if user:
        return jsonify(errno=RET.DATAEXIST, errmsg='手机号已被注册')

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
        return jsonify(errno=RET.DBERR, errmsg='保存用户信息失败')

    session['user_id'] = user.id
    session['username'] = user.name
    session['mobile'] = user.mobile

    return jsonify(errno=RET.OK, errmsg='注册成功')
