from .celery import cel
from common.chackData import Goods, Order
import traceback
from common.logg import Logger

logger = Logger()

@cel.task()
def kill_order(order_no):
    try:
        order = Order().order.get(order_no=order_no)
        if order and order.trade_status not in [2,3]:
            return False

        # 过期订单标记删除
        order = Order().order.gets(order_no=order_no)
        if order.exists():
            Order().order.delete(order_no=order_no)
            logger.info('kill order {} successful'.format(order_no))

        # 修改账号状态为未出售
        goods = Goods().account.gets(order__order_no=order_no)
        for good in goods:
            good.isSale = 0
            good.save()
        return True
    except Exception:
        logger.error(traceback.format_exc())
        return False