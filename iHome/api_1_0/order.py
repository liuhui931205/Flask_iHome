# coding=utf-8
from datetime import datetime
from flask import request, jsonify, current_app,g

from iHome import db
from iHome.models import House, Order
from iHome.response_code import RET
from iHome.utils.commons import login_required
from . import api


@api.route('/orders', methods=['POST'])
@login_required
def save_order_info():

    req_dict = request.json
    house_id = req_dict.get('house_id')
    start_date = req_dict.get('start_date')
    end_date = req_dict.get('end_date')

    if not all([house_id, start_date, end_date]):
        return jsonify(errno=RET.PARAMERR, errmsg='参数不完整')

    try:
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        end_date = datetime.strptime(end_date, '%Y-%m-%d')
        assert start_date < end_date, Exception('起始时间大于结束时间')
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.PARAMERR, errmsg='参数错误')

    try:
        house = House.query.get(house_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg='查询房屋信息失败')

    if not house:
        return jsonify(errno=RET.NODATA, errmsg='房屋不存在')
    try:
        conflict_orders_count = Order.query.filter(end_date > Order.begin_date, start_date < Order.end_date,
                                                Order.house_id == house_id).count()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg='查询冲突订单失败')

    if conflict_orders_count > 0:
        return jsonify(errno=RET.DATAERR, errmsg='房屋已被预定')
    days = (end_date - start_date).days
    order = Order()
    order.user_id = g.user_id
    order.house_id = house_id
    order.begin_date = start_date
    order.end_date = end_date
    order.days = days
    order.house_price = house.price
    order.amount = house.price * days

    house.order_count += 1
    try:
        db.session.add(order)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg='保存订单信息失败')

    return jsonify(errno=RET.OK, errmsg='ok')