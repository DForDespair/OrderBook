import time
import random
from Order.Order import Order
from Order.OrderEnums import OrderSide, OrderType
from Orderbook.Orderbook import OrderBook
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

def generate_random_order(order_id: int) -> Order:
    return Order(
        _order_type=OrderType.GoodTillCancel,
        _order_id=order_id,
        _side=random.choice([OrderSide.BUY, OrderSide.SELL]),
        _price=round(random.uniform(95.0, 105.0), 2),
        _initial_quantity=random.randint(1, 10)
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
        print(ob.get_order_infos())
        print("Order book shut down.")


if __name__ == "__main__":
    main()
    