# coding=utf-8
from flask import session,current_app,jsonify

from iHome.models import User
from iHome.response_code import RET
from . import api

@api.route('/user')
def get_user_info():
    # 用户先登录
    user_id = session.get('user_id')
    try:
        user = User.query.get(user_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR,errmsg='查询用户信息失败')
    if not user:
        return jsonify(errno=RET.USERERR,errmsg='用户不存在')

    resp = {
        'user_id':user_id,
        'username':user.name,
        'avatar_url': user.avatar_url
    }

    return jsonify(errno=RET.OK, errmsg='ok',data=resp)
