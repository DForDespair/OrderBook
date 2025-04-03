from Order.Order import Order
from Order.OrderEnums import OrderSide, OrderType
from Orderbook.Orderbook import OrderBook


if __name__ == "__main__":
    order_book = OrderBook()
    order_id = 1
    order = Order(
        _order_type = OrderType.GoodTillCancel,
        _order_id = order_id,
        _side = OrderSide.BUY,
        _price = 100,
        _initial_quantity = 10
    )
    print(order_book.size())
    print(order_book.add_order(order))
    print(order_book.size())
    print(order_book.get_order_infos())
