
import random
import time


def make_order_sn():
    # 获取订单号，保证唯一性
    order_sn = ''
    s = '1234567890qwertyuiopZXCVBNM'
    for i in range(20):
        order_sn += random.choice(s)
    order_sn += str(time.time())
    return order_sn
