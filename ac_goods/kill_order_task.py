import traceback
from ac_goods.celery import cel
from common.chackData import Goods, Order
from common.logg import Logger

logger = Logger()

@cel.task()
def kill_order(order_no):
    try:
        order = Order().order.get(order_no=order_no)
        if not order:
            return 'order is not exist'

        if order.trade_status in (2,3):
            logger.info(order.trade_status)
            return 'order:{} status is {}'.format(order_no, order.trade_status)

        # 过期订单标记删除
        Order().order.delete(order_no=order_no)
        logger.info('kill order {} successfully'.format(order_no))

        # 修改账号状态为未出售
        goods = Goods().account.gets(order__order_no=order_no)
        for good in goods:
            good.isSale = 0
            good.save()
        return 'kill order {} successful'.format(order_no)
    except Exception:
        logger.error(traceback.format_exc())
        return traceback.format_exc()