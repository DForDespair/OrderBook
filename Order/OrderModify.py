
from dataclasses import dataclass
from Order.OrderEnums import OrderSide, OrderType

@dataclass
class OrderModify:
    _order_id: int
    _side: OrderSide
    _price: float
    _quantity: int
    
    @property
    def order_id(self):
        return self._order_id
    
    @property
    def side(self):
        return self._side
    
    @property
    def price(self):
        return self._price

    @property
    def quantity(self):
        return self._quantity
    
    @order_id.setter
    def order_id(self, id: int):
        if not isinstance(id, int):
            raise ValueError("id must be an instance of int")
        self._order_id = id
    
    @side.setter
    def side(self, side: OrderSide):
        if not isinstance(side, OrderSide):
            raise ValueError("side must be an instance of OrderSide enum")
        self._side = side
    
    @price.setter
    def price(self, price: float):
        if not isinstance(price, (float, int)):
            raise ValueError("price must be either an int or a float")
        
        if price < 0:
            raise ValueError("price must be positive")
        self._price = float(price)

    @quantity.setter
    def quantity(self, quantity: int):
        if not isinstance(quantity, int):
            raise ValueError("initial_quantity must be an instance of int")
        if quantity < 0:
            raise ValueError("quantity must be positive")
        self._quantity = quantity
        
    def __repr__(self):
        return (
            f"OrderModify(_order_id={self.order_id}, _side={self.side}, _type={self.order_type}, "
            f"_price={self.price}, _quantity={self.filled_quantity})"
        )