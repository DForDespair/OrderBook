from enum import Enum

class OrderSide(Enum):
    BUY = "buy"
    SELL = "sell"
    
class OrderType(Enum):
    GoodTillCancel = "goodTillCancel"
    FillAndKill = "fillAndKill"
    FillOrKill = "fillOrKill"
    GoodForDay = "goodForDay",
    Market = "market"