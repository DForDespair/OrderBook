from dataclasses import dataclass, field
from enum import Enum
from typing import Deque, List

from Order.Order import Order

@dataclass
class LevelInfo:
    _price: float
    _quantity: int
    
    @property
    def price(self):
        return self._price

    @property
    def quantity(self):
        return self._quantity
    
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
        
    def add_quantity(self, quantity: int):
        self.quantity = self.quantity +quantity
        
    def remove_quantity(self, quantity: int):
        self._quantity = self.quantity - quantity
    
    
    def __str__(self):
        return f"{self.quantity} @ {self.price}"
    
    def __repr__(self):
        return f"LevelInfo({repr(self.price)}, {repr(self.quantity)})"

@dataclass
class LevelInfos:
    levels: List[LevelInfo] = field(default_factory = list) ## without this, each LevelInfos will share the same list
    reverse: bool = False
    
    
    def add(self, level: LevelInfo):
        self.levels.append(level)
        self.sort()
        
    def sort(self):
        self.levels.sort(key= lambda level: level.price, reverse=self.reverse)
        
    
    

class OrderBookLevelInfos:
    def __init__(self, bids: LevelInfos, asks: LevelInfos):
        self._bids = bids
        self._asks = asks
    
    @property
    def bids(self) -> LevelInfos:
        return self._bids

    @property
    def asks(self) -> LevelInfos:
        return self._asks
    
    def __str__(self):
        return f"Bids: {self._bids}\nAsks: {self._asks}"

    def __repr__(self):
        return f"OrderBookLevelInfos(bids={repr(self.bids)}, asks={repr(self.asks)})"
    
class LevelAction(Enum):
    ADD = "add"
    REMOVE = "remove"
    MATCH = "match"
    
@dataclass
class LevelData:
    price: float
    quantity: int
    
    def update(self, qty: float, action: LevelAction):
        if action == LevelAction.ADD:
            self.quantity += qty
            self.count += 1
        elif action == LevelAction.REMOVE:
            self.quantity -= qty
            self.count -= 1
        elif action == LevelAction.MATCH:
            self.quantity -= qty

        return self.quantity > 0 and self.count > 0