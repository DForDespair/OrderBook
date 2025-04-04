
from dataclasses import dataclass
from datetime import datetime, timezone


@dataclass
class TradeInfo:
    _order_id: int
    _price: float
    _quantity: int
    
    @property
    def order_id(self):
        return self._order_id
    
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
            raise ValueError("quantity must be an instance of int")
        if quantity < 0:
            raise ValueError("quantity must be positive")
        self._quantity = quantity
        
    def add_quantity(self, quantity: int):
        self._quantity = self.quantity + quantity
        
    def remove_quantity(self, quantity: int):
        self.quantity = self.quantity - quantity
    

@dataclass   
class Trade:
    _bid_trade: TradeInfo
    _ask_trade: TradeInfo
    
    def __post_init__(self):
        self._timestamp = datetime.now(timezone.utc)
    
    @property
    def bid_trade(self) -> TradeInfo:
        return self._bid_trade
    
    @property
    def ask_trade(self) -> TradeInfo:
        return self._ask_trade
    
    def timezone(self) -> datetime:
        return self._timestamp
    
    def __repr__(self):
        return (f"Trade("
                f"bid={repr(self._bid_trade)}, "
                f"ask={repr(self._ask_trade)}, "
                f"timestamp={self._timestamp.isoformat()})")
    
    def __str__(self):
        return (f"[TRADE] "
                f"{self._bid_trade.quantity} @ {self._bid_trade.price} "
                f"(Buyer: {self._bid_trade.order_id}, Seller: {self._ask_trade.order_id}) "
                f"at {self._timestamp.strftime('%Y-%m-%d %H:%M:%S UTC')}")
