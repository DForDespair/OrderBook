import time
import random
from Order.Order import Order
from Order.OrderEnums import OrderSide, OrderType
from Orderbook.Orderbook import OrderBook
import logging

from Plotting.LevelsPlot import LevelsPlot

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

def generate_random_order(order_id: int) -> Order:
    base_price = 100.0
    side = OrderSide.BUY if order_id % 2 == 0 else OrderSide.SELL

    if side == OrderSide.BUY:
        price = base_price - (order_id % 10) * 0.5
    else:
        price = base_price + (order_id % 10) * 0.5

    return Order(
        _order_type=OrderType.GoodTillCancel,
        _order_id=order_id,
        _side=side,
        _price=price,
        _initial_quantity=random.randint(5, 20)
    )

def main():
    ob = OrderBook(use_threads=True)
    order_id = 1

    try:
        while True:
            order = generate_random_order(order_id)
            ob.submit_add_order(order)
            order_id += 1
            time.sleep(0.01)

    except KeyboardInterrupt:
        print("Shutting Down...")

    finally:
        ob.shutdown()
        LevelsPlot(ob.get_order_infos()).plot_order_book_depth()
        print("Order book shut down.")


if __name__ == "__main__":
    main()
    