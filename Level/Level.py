from dataclasses import dataclass
from typing import List

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
    
    def __str__(self):
        return f"{self.quantity} @ {self.price}"
    
    def __repr__(self):
        return f"LevelInfo({repr(self.price)}, {repr(self.quantity)})"

class LevelInfos:
    level_info = List[LevelInfo]
    

class OrderBookLevelInfos:
    def __init__(self, bids: LevelInfo, asks: LevelInfo):
        self.bids = bids
        self.asks = asks
    
    @property
    def bids(self) -> LevelInfos:
        return self._bids

    @property
    def asks(self) -> LevelInfos:
        return self._asks