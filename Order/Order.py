from dataclasses import dataclass
from Order.OrderEnums import OrderType, OrderSide
from datetime import datetime, timezone

@dataclass
class Order:
    _order_type: OrderType
    _order_id: int
    _side: OrderSide
    _price: float
    _initial_quantity: int
    

    def __post_init__(self):
        self._remaining_quantity = self._initial_quantity
        self._timestamp = datetime.now(timezone.utc)
        
    @property
    def order_type(self):
        return self._order_type
    
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
    def timestamp(self):
        return self._timestamp

    @property
    def initial_quantity(self):
        return self._initial_quantity
    
    @property
    def filled_quantity(self):
        return self.initial_quantity() - self.remaining_quantity()
    
    @property
    def remaining_quantity(self):
        return self._remaining_quantity
    
    @order_type.setter
    def order_type(self, order_type: OrderType):
        if not isinstance(order_type, OrderType):
            raise ValueError("order_type must be an instance of OrderType enum")
        self._order_type = order_type
    
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

    @initial_quantity.setter
    def initial_quantity(self, initial_quantity: int):
        if not isinstance(initial_quantity, int):
            raise ValueError("initial_quantity must be an instance of int")
        if initial_quantity < 0:
            raise ValueError("quantity must be positive")
        self._initial_quantity = initial_quantity
    
    @remaining_quantity.setter
    def remaining_quantity(self, quantity: int):
        if not isinstance(quantity, int):
            raise ValueError("filled_quantity must be an instance of int")
        if quantity < 0:
            raise ValueError("quantity must be positive")
        self._remaining_quantity = quantity
    
    @property 
    def filled_quantity(self):
        return self._initial_quantity - self._remaining_quantity
    
    def is_filled(self) -> bool:
        return self._remaining_quantity == 0
        
    def fill_order(self, quantity: int):
        if quantity > self.remaining_quantity:
            raise ValueError(f"Order {self.order_id} cannot be filled for more than its remaining quantity")
        self._remaining_quantity -= quantity
        
    def __repr__(self):
        return (f"Order("
                f"id={self.order_id}, "
                f"type={self.order_type.name}, "
                f"side={self.side.name}, "
                f"price={self.price}, "
                f"qty={self.initial_quantity}, "
                f"remaining={self.remaining_quantity}, "
                f"time={self.timestamp.isoformat()})")

    def __str__(self):
        return (f"[{self.side.name} #{self.order_id}] "
                f"{self.remaining_quantity}/{self.initial_quantity} @ {self.price} "
                f"({self.order_type.name}, {self.timestamp.strftime('%H:%M:%S')})")