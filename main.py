from Order.Order import Order
from Order.OrderEnums import OrderSide, OrderType
from Orderbook.Orderbook import OrderBook
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

if __name__ == "__main__":
    order_book = OrderBook()
    order_id = 1
    order_id2 = 2
    order_id3 = 3
    order_id4 = 4
    order_buy = Order(
        _order_type = OrderType.GoodTillCancel,
        _order_id = order_id,
        _side = OrderSide.BUY,
        _price = 50,
        _initial_quantity = 100
    )
    order_sell1 = Order(
        _order_type = OrderType.GoodTillCancel,
        _order_id = order_id2,
        _side = OrderSide.SELL,
        _price = 48,
        _initial_quantity = 50
    )
    order_sell2 = Order(
        _order_type = OrderType.GoodTillCancel,
        _order_id = order_id3,
        _side = OrderSide.SELL,
        _price = 49,
        _initial_quantity = 40
    )
    
    order_sell3 = Order(
        _order_type = OrderType.GoodTillCancel,
        _order_id = order_id3,
        _side = OrderSide.SELL,
        _price = 49,
        _initial_quantity = 10
    )
    order_book.add_order(order_sell1)
    order_book.add_order(order_sell2)
    order_book.add_order(order_buy)
    order_book.add_order(order_sell3)